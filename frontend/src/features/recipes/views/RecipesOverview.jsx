import { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { useOutletContext } from 'react-router-dom';
import { MetricCard } from '../../../components/MetricCard';
import { RecipesTable } from '../components/RecipesTable';
import { RecipeFormModal } from '../components/RecipeFormModal';
import { ConfirmDeleteModal } from '../components/ConfirmDeleteModal';
import { useRecipes, useRecipesSummary } from '../hooks/useRecipes';
import './RecipesOverview.css';

/**
 * Tela Principal do Recipes Overview
 */
export const RecipesOverview = forwardRef((props, ref) => {
  // Recebe o contexto do Outlet (inventoryRef do AppLayout)
  const outletContext = useOutletContext();
  const inventoryRef = outletContext?.inventoryRef;
  const { recipes, loading, fetchRecipes, deleteRecipe, createRecipe, updateRecipe } = useRecipes();
  const { summary, fetchSummary } = useRecipesSummary();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRecipe, setEditingRecipe] = useState(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [recipeToDelete, setRecipeToDelete] = useState(null);
  const searchTimeoutRef = useRef(null);

  const loadData = async () => {
    try {
      await Promise.all([
        fetchRecipes(),
        fetchSummary()
      ]);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Expõe o método loadData para componentes pais via ref
  useImperativeHandle(ref, () => ({
    loadData
  }));

  // Conecta a ref do AppLayout com o método loadData
  useImperativeHandle(inventoryRef, () => ({
    loadData
  }));

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    // Cancela o timeout anterior se existir (debounce)
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    // Busca após 500ms de inatividade
    searchTimeoutRef.current = setTimeout(() => {
      fetchRecipes(value || null);
    }, 500);
  };

  // Limpa o timeout quando o componente desmontar
  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  const handleDelete = async (id) => {
    const recipe = recipes.find(r => r.id === id);
    if (recipe) {
      setRecipeToDelete(recipe);
      setIsDeleteModalOpen(true);
    }
  };

  const handleConfirmDelete = async () => {
    if (!recipeToDelete) return;
    
    try {
      await deleteRecipe(recipeToDelete.id);
      await fetchSummary(); // Atualiza resumo após deletar
      setIsDeleteModalOpen(false);
      setRecipeToDelete(null);
    } catch (error) {
      alert('Erro ao deletar receita');
    }
  };

  const handleCloseDeleteModal = () => {
    setIsDeleteModalOpen(false);
    setRecipeToDelete(null);
  };

  const handleEdit = (recipe) => {
    setEditingRecipe(recipe);
    setIsModalOpen(true);
  };

  const handleAddRecipe = () => {
    setEditingRecipe(null);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingRecipe(null);
  };

  const handleSubmitForm = async (formData) => {
    try {
      if (editingRecipe) {
        // Atualizar receita existente
        await updateRecipe(editingRecipe.id, formData);
      } else {
        // Criar nova receita
        await createRecipe(formData);
      }
      
      // Recarrega dados
      await loadData();
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro ao salvar receita');
      throw error;
    }
  };

  const filteredRecipes = recipes.filter(recipe => {
    if (activeFilter === 'all') return true;
    // Adicione filtros adicionais conforme necessário
    return true;
  });

  return (
    <div className="recipes-overview">
      {/* Header */}
      <div className="recipes-header">
        <div className="recipes-header__content">
          <h1>Recipes Overview</h1>
          <p>Manage and monitor your recipes</p>
        </div>
        <div className="recipes-header__search">
          <input
            type="text"
            placeholder="Search recipes..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
          <div className="notification-icon">
            🔔
            <span className="notification-badge">3</span>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        <MetricCard
          icon="🍳"
          title="Total Recipes"
          value={summary?.total_recipes || 0}
          type="info"
        />
        <MetricCard
          icon="✅"
          title="Feasible Recipes"
          value={summary?.feasible_recipes || 0}
          trend="up"
          trendValue={`+${summary?.feasible_percentage || 0}%`}
          type="success"
        />
      </div>

      {/* Recipe Items Section */}
      <div className="recipes-items">
        <div className="recipes-items__header">
          <h2>Recipe Title</h2>
        </div>

        <div className="recipes-items__actions">
          <button className="btn-action btn-action--primary" onClick={handleAddRecipe}>
            + Add New Recipe
          </button>
        </div>

        <RecipesTable
          recipes={filteredRecipes}
          onEdit={handleEdit}
          onDelete={handleDelete}
          loading={loading}
        />

        {filteredRecipes.length > 0 && (
          <div className="pagination">
            <span className="pagination__info">
              Showing {filteredRecipes.length} of {summary?.total_recipes || 0} items
            </span>
          </div>
        )}
      </div>

      {/* Most Used Ingredients Section */}
      {summary?.most_used_ingredients && summary.most_used_ingredients.length > 0 && (
        <div className="most-used-ingredients">
          <h2>Most Used Ingredients</h2>
          <div className="ingredients-chart">
            {summary.most_used_ingredients.slice(0, 4).map((ingredient, index) => {
              const maxCount = summary.most_used_ingredients[0].recipe_count;
              const percentage = (ingredient.recipe_count / maxCount) * 100;
              
              return (
                <div key={ingredient.item_id} className="ingredient-bar">
                  <div 
                    className="ingredient-bar__fill" 
                    style={{ width: `${percentage}%` }}
                  >
                    <span className="ingredient-bar__label">
                      {ingredient.item_name}
                    </span>
                  </div>
                  <span className="ingredient-bar__count">
                    {ingredient.recipe_count}
                  </span>
                </div>
              );
            })}
          </div>
          <p className="showing-text">Showing 1-4 of {summary.most_used_ingredients.length} items</p>
        </div>
      )}

      {/* Modal de Formulário */}
      <RecipeFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSubmitForm}
        recipe={editingRecipe}
        loading={loading}
      />

      {/* Modal de Confirmação de Exclusão */}
      <ConfirmDeleteModal
        isOpen={isDeleteModalOpen}
        onClose={handleCloseDeleteModal}
        onConfirm={handleConfirmDelete}
        recipeName={recipeToDelete?.title || ''}
        loading={loading}
      />
    </div>
  );
});

RecipesOverview.displayName = 'RecipesOverview';
