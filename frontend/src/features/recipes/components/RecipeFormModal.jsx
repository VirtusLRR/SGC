import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useNavigate } from 'react-router-dom';
import { Modal } from '../../../components/Modal';
import { itemsApi } from '../../items/api/itemsApi';
import './RecipeFormModal.css';

/**
 * Modal de formulário para criar/editar receita
 */
export const RecipeFormModal = ({ 
  isOpen, 
  onClose, 
  onSubmit, 
  recipe = null,
  loading = false 
}) => {
  const isEditMode = !!recipe;
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    steps: '',
    recipe_itens: [], // Array de { item_id, amount }
  });

  const [errors, setErrors] = useState({});
  const [availableItems, setAvailableItems] = useState([]);
  const [loadingItems, setLoadingItems] = useState(false);

  // Carrega itens disponíveis quando o modal abre
  useEffect(() => {
    if (isOpen) {
      loadAvailableItems();
    }
  }, [isOpen]);

  useEffect(() => {
    if (recipe) {
      setFormData({
        title: recipe.title || '',
        description: recipe.description || '',
        steps: recipe.steps || '',
        recipe_itens: recipe.recipe_itens?.map(ri => ({
          item_id: ri.item_id || ri.item?.id,
          amount: ri.amount,
          item: ri.item
        })) || [],
      });
    } else {
      resetForm();
    }
  }, [recipe, isOpen]);

  const loadAvailableItems = async () => {
    try {
      setLoadingItems(true);
      const items = await itemsApi.getAllItems();
      setAvailableItems(items);
    } catch (error) {
      console.error('Erro ao carregar itens:', error);
    } finally {
      setLoadingItems(false);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      steps: '',
      recipe_itens: [],
    });
    setErrors({});
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Remove erro do campo ao editar
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Título é obrigatório';
    }

    if (!formData.steps.trim()) {
      newErrors.steps = 'Passos são obrigatórios';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddRecipeItem = () => {
    setFormData(prev => ({
      ...prev,
      recipe_itens: [...prev.recipe_itens, { item_id: '', amount: '' }]
    }));
  };

  const handleRemoveRecipeItem = (index) => {
    setFormData(prev => ({
      ...prev,
      recipe_itens: prev.recipe_itens.filter((_, i) => i !== index)
    }));
  };

  const handleRecipeItemChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      recipe_itens: prev.recipe_itens.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const handleNavigateToItems = () => {
    handleClose();
    navigate('/items');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      const submitData = {
        title: formData.title,
        description: formData.description || null,
        steps: formData.steps,
        recipe_itens: formData.recipe_itens
          .filter(ri => ri.item_id && ri.amount)
          .map(ri => {
            const recipeItem = {
              item_id: parseInt(ri.item_id),
              amount: parseFloat(ri.amount)
            };
            
            // Se estiver editando, inclui o recipe_id
            if (isEditMode && recipe?.id) {
              recipeItem.recipe_id = recipe.id;
            }
            
            return recipeItem;
          })
      };

      await onSubmit(submitData);
      resetForm();
      onClose();
    } catch (error) {
      console.error('Erro ao salvar receita:', error);
    }
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title={isEditMode ? 'Editar Receita' : 'Adicionar Nova Receita'}
      size="medium"
    >
      <form onSubmit={handleSubmit} className="recipe-form">
        <div className="form-row">
          <div className="form-group form-group--full">
            <label htmlFor="title" className="form-label">
              Título da Receita <span className="required">*</span>
            </label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              className={`form-input ${errors.title ? 'form-input--error' : ''}`}
              placeholder="Ex: Pasta Primavera"
              disabled={loading}
            />
            {errors.title && <span className="form-error">{errors.title}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group form-group--full">
            <label htmlFor="description" className="form-label">
              Descrição
            </label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="form-input"
              placeholder="Ex: Classic spring vegetables pasta"
              disabled={loading}
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group form-group--full">
            <label htmlFor="steps" className="form-label">
              Modo de Preparo <span className="required">*</span>
            </label>
            <textarea
              id="steps"
              name="steps"
              value={formData.steps}
              onChange={handleChange}
              className={`form-textarea ${errors.steps ? 'form-input--error' : ''}`}
              placeholder="Descreva os passos do preparo..."
              rows="6"
              disabled={loading}
            />
            {errors.steps && <span className="form-error">{errors.steps}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group form-group--full">
            <div className="recipe-items-header">
              <label className="form-label">Itens da Receita</label>
              <div className="recipe-items-actions">
                <button
                  type="button"
                  onClick={handleNavigateToItems}
                  className="btn btn--link"
                  disabled={loading}
                >
                  + Adicionar Novo Item
                </button>
                <button
                  type="button"
                  onClick={handleAddRecipeItem}
                  className="btn btn--secondary btn--sm"
                  disabled={loading || loadingItems}
                >
                  + Associar Item
                </button>
              </div>
            </div>
            
            {loadingItems ? (
              <div className="recipe-items-loading">Carregando itens...</div>
            ) : (
              <div className="recipe-items-list">
                {formData.recipe_itens.map((recipeItem, index) => {
                  const selectedItem = availableItems.find(item => item.id === parseInt(recipeItem.item_id));
                  
                  return (
                    <div key={index} className="recipe-item-row">
                      <div className="recipe-item-select">
                        <select
                          value={recipeItem.item_id}
                          onChange={(e) => handleRecipeItemChange(index, 'item_id', e.target.value)}
                          className="form-input"
                          disabled={loading}
                        >
                          <option value="">Selecione um item...</option>
                          {availableItems.map(item => (
                            <option key={item.id} value={item.id}>
                              {item.name} ({item.amount} {item.measure_unity} disponível)
                            </option>
                          ))}
                        </select>
                      </div>
                      
                      <div className="recipe-item-amount">
                        <input
                          type="number"
                          value={recipeItem.amount}
                          onChange={(e) => handleRecipeItemChange(index, 'amount', e.target.value)}
                          placeholder="Quantidade"
                          className="form-input"
                          min="0"
                          step="0.01"
                          disabled={loading}
                        />
                        {selectedItem && (
                          <span className="recipe-item-unit">{selectedItem.measure_unity}</span>
                        )}
                      </div>
                      
                      <button
                        type="button"
                        onClick={() => handleRemoveRecipeItem(index)}
                        className="btn btn--danger btn--icon"
                        disabled={loading}
                        title="Remover item"
                      >
                        ✕
                      </button>
                    </div>
                  );
                })}
                
                {formData.recipe_itens.length === 0 && (
                  <div className="recipe-items-empty">
                    Nenhum item associado. Clique em "Associar Item" para adicionar.
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={handleClose}
            className="btn btn--secondary"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn btn--primary"
            disabled={loading}
          >
            {loading ? 'Salvando...' : (isEditMode ? 'Salvar Alterações' : 'Adicionar Receita')}
          </button>
        </div>
      </form>
    </Modal>
  );
};

RecipeFormModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  recipe: PropTypes.shape({
    id: PropTypes.number,
    title: PropTypes.string,
    description: PropTypes.string,
    steps: PropTypes.string,
    recipe_itens: PropTypes.arrayOf(PropTypes.shape({
      item_id: PropTypes.number,
      amount: PropTypes.number,
      item: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        measure_unity: PropTypes.string,
      })
    }))
  }),
  loading: PropTypes.bool,
};
