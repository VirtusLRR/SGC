import { useMemo, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { RecipeStatus, StatusColors } from '../types/recipe.types';
import { recipesApi } from '../api/recipesApi';
import { RecipeViewModal } from './RecipeViewModal';
import './RecipesTable.css';

/**
 * Componente de Tabela de Receitas
 */
export const RecipesTable = ({ 
  recipes, 
  onEdit, 
  onDelete, 
  loading = false 
}) => {
  /**
   * Estado para armazenar custos das receitas
   */
  const [recipeCosts, setRecipeCosts] = useState({});
  const [feasibleRecipes, setFeasibleRecipes] = useState([]);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  /**
   * Busca custos e receitas viáveis
   */
  useEffect(() => {
    const fetchRecipeData = async () => {
      try {
        const [costs, feasible] = await Promise.all([
          recipesApi.getAllRecipesCosts(),
          recipesApi.getFeasibleRecipes()
        ]);
        
        // Converte array de custos em objeto indexado por recipe_id
        const costsMap = {};
        costs.forEach(cost => {
          costsMap[cost.recipe_id] = cost;
        });
        setRecipeCosts(costsMap);
        
        // Array de IDs de receitas viáveis
        const feasibleIds = feasible.map(r => r.recipe_id);
        setFeasibleRecipes(feasibleIds);
      } catch (error) {
        console.error('Erro ao buscar dados das receitas:', error);
      }
    };

    if (recipes && recipes.length > 0) {
      fetchRecipeData();
    }
  }, [recipes]);

  /**
   * Determina o status de uma receita
   */
  const getRecipeStatus = (recipe) => {
    if (feasibleRecipes.includes(recipe.id)) {
      return RecipeStatus.FEASIBLE;
    }
    return RecipeStatus.MISSING_ITEMS;
  };

  /**
   * Formata o valor em moeda
   */
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  /**
   * Obtém o custo da receita
   */
  const getRecipeCost = (recipe) => {
    const costData = recipeCosts[recipe.id];
    return costData ? costData.total_cost : 0;
  };

  /**
   * Abre o modal de visualização da receita
   */
  const handleViewRecipe = async (recipe) => {
    try {
      // Busca detalhes completos da receita incluindo itens associados
      const fullRecipe = await recipesApi.getRecipeById(recipe.id);
      
      // Busca também os detalhes de custo que podem conter informações dos itens
      try {
        const costData = await recipesApi.getRecipeCost(recipe.id);
        
        // Se costData tem informações de itens, mescla com fullRecipe
        if (costData && costData.items) {
          fullRecipe.recipe_itens_with_details = costData.items;
        }
      } catch (costError) {
        console.log('Custo não disponível:', costError);
      }
      
      setSelectedRecipe(fullRecipe);
      setIsViewModalOpen(true);
    } catch (error) {
      console.error('Erro ao carregar detalhes da receita:', error);
    }
  };

  /**
   * Fecha o modal de visualização
   */
  const handleCloseViewModal = () => {
    setIsViewModalOpen(false);
    setSelectedRecipe(null);
  };

  const processedRecipes = useMemo(() => {
    return recipes.map(recipe => ({
      ...recipe,
      status: getRecipeStatus(recipe),
      totalCost: getRecipeCost(recipe),
    }));
  }, [recipes, recipeCosts, feasibleRecipes]);

  if (loading) {
    return (
      <div className="recipes-table-loading">
        <div className="spinner"></div>
        <p>Carregando receitas...</p>
      </div>
    );
  }

  if (!recipes || recipes.length === 0) {
    return (
      <div className="recipes-table-empty">
        <p>Nenhuma receita encontrada</p>
      </div>
    );
  }

  return (
    <div className="recipes-table-container">
      <table className="recipes-table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" />
            </th>
            <th>Título da Receita</th>
            <th>Descrição</th>
            <th>Valor Total</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {processedRecipes.map((recipe) => (
            <tr key={recipe.id}>
              <td>
                <input type="checkbox" />
              </td>
              <td>
                <div className="recipe-name-cell">
                  <div className={`recipe-icon recipe-icon--${recipe.title.charAt(0).toLowerCase()}`}>
                    {recipe.title.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="recipe-name">{recipe.title}</div>
                  </div>
                </div>
              </td>
              <td>
                <span className="recipe-description">
                  {recipe.description || '-'}
                </span>
              </td>
              <td>{formatCurrency(recipe.totalCost)}</td>
              <td>
                <span className={`status-badge status-badge--${StatusColors[recipe.status]}`}>
                  {recipe.status}
                </span>
              </td>
              <td>
                <div className="action-buttons">
                  <button
                    className="action-btn action-btn--view"
                    onClick={() => handleViewRecipe(recipe)}
                    title="Visualizar"
                  >
                    👁️
                  </button>
                  <button
                    className="action-btn action-btn--edit"
                    onClick={() => onEdit(recipe)}
                    title="Editar"
                  >
                    ✏️
                  </button>
                  <button
                    className="action-btn action-btn--delete"
                    onClick={() => onDelete(recipe.id)}
                    title="Deletar"
                  >
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal de Visualização */}
      <RecipeViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        recipe={selectedRecipe}
      />
    </div>
  );
};

RecipesTable.propTypes = {
  recipes: PropTypes.array.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};
