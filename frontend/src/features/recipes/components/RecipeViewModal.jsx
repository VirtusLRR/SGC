import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Modal } from '../../../components/Modal';
import { itemsApi } from '../../items/api/itemsApi';
import './RecipeViewModal.css';

/**
 * Modal para visualizar detalhes de uma receita
 */
export const RecipeViewModal = ({ 
  isOpen, 
  onClose, 
  recipe 
}) => {
  const [itemsDetails, setItemsDetails] = useState({});
  const [loadingItems, setLoadingItems] = useState(false);

  /**
   * Busca os detalhes dos itens usando os item_ids
   */
  useEffect(() => {
    const fetchItemsDetails = async () => {
      if (!recipe?.recipe_itens || recipe.recipe_itens.length === 0) return;

      setLoadingItems(true);
      try {
        const itemsMap = {};
        
        // Busca detalhes de cada item e seu custo para a quantidade da receita
        await Promise.all(
          recipe.recipe_itens.map(async (recipeItem) => {
            try {
              const [item, totalValueData] = await Promise.all([
                itemsApi.getItemById(recipeItem.item_id),
                itemsApi.getTotalItemValue(recipeItem.item_id)
              ]);
              
              // Calcula o custo proporcional para a quantidade usada na receita
              const itemUnitCost = item.amount > 0 ? totalValueData.total_value / item.amount : 0;
              const recipeCost = itemUnitCost * recipeItem.amount;
              
              itemsMap[recipeItem.item_id] = {
                ...item,
                recipeCost: recipeCost
              };
            } catch (error) {
              console.error(`Erro ao buscar item ${recipeItem.item_id}:`, error);
            }
          })
        );
        
        setItemsDetails(itemsMap);
      } catch (error) {
        console.error('Erro ao buscar detalhes dos itens:', error);
      } finally {
        setLoadingItems(false);
      }
    };

    if (isOpen && recipe) {
      fetchItemsDetails();
    }
  }, [isOpen, recipe]);

  /**
   * Formata o valor em moeda
   */
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value || 0);
  };

  if (!recipe) return null;

  const recipeItems = recipe.recipe_itens || [];
  
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={recipe.title}
      size="large"
    >
      <div className="recipe-view-content">
        {/* Descrição */}
        {recipe.description && (
          <div className="recipe-view-section">
            <h3 className="recipe-view-section-title">Descrição</h3>
            <p className="recipe-view-description">{recipe.description}</p>
          </div>
        )}

        {/* Modo de Preparo */}
        <div className="recipe-view-section">
          <h3 className="recipe-view-section-title">Modo de Preparo</h3>
          <div className="recipe-view-steps">
            {recipe.steps}
          </div>
        </div>

        {/* Itens Associados */}
        {recipeItems && recipeItems.length > 0 ? (
          <div className="recipe-view-section">
            <h3 className="recipe-view-section-title">Itens da Receita</h3>
            {loadingItems ? (
              <div className="recipe-items-loading">Carregando detalhes dos itens...</div>
            ) : (
              <div className="recipe-items-grid">
                {recipeItems.map((recipeItem, index) => {
                  
                  // Busca os detalhes do item usando o item_id
                  const item = itemsDetails[recipeItem.item_id];
                  const itemName = item?.name || 'Item não encontrado';
                  const itemDescription = item?.description || '';
                  const amount = recipeItem.amount || 0;
                  const measureUnity = item?.measure_unity || '';
                  const availableAmount = item?.amount;
                  
                  // Usa o custo calculado pela API
                  const itemCost = item?.recipeCost || 0;

                return (
                  <div key={index} className="recipe-item-card">
                    <div className="recipe-item-header">
                      <div className={`item-icon item-icon--${itemName.charAt(0).toLowerCase()}`}>
                        {itemName.charAt(0).toUpperCase()}
                      </div>
                      <div className="recipe-item-info">
                        <div className="recipe-item-name">{itemName}</div>
                        {itemDescription && (
                          <div className="recipe-item-description">{itemDescription}</div>
                        )}
                      </div>
                    </div>
                    
                    <div className="recipe-item-details">
                      <div className="recipe-item-detail">
                        <span className="detail-label">Quantidade:</span>
                        <span className="detail-value">
                          {amount} {measureUnity}
                        </span>
                      </div>
                      
                      {availableAmount !== undefined && availableAmount !== null && (
                        <div className="recipe-item-detail">
                          <span className="detail-label">Disponível:</span>
                          <span className={`detail-value ${availableAmount >= amount ? 'detail-value--success' : 'detail-value--danger'}`}>
                            {availableAmount} {measureUnity}
                          </span>
                        </div>
                      )}
                      
                      {itemCost > 0 && (
                        <div className="recipe-item-detail">
                          <span className="detail-label">Custo:</span>
                          <span className="detail-value detail-value--cost">
                            {formatCurrency(itemCost)}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
              </div>
            )}
          </div>
        ) : (
          <div className="recipe-view-section">
            <h3 className="recipe-view-section-title">Itens da Receita</h3>
            <div className="recipe-items-empty">
              Nenhum item associado a esta receita.
            </div>
          </div>
        )}

        {/* Botão de Fechar */}
        <div className="recipe-view-actions">
          <button
            type="button"
            onClick={onClose}
            className="btn btn--primary"
          >
            Fechar
          </button>
        </div>
      </div>
    </Modal>
  );
};

RecipeViewModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  recipe: PropTypes.shape({
    id: PropTypes.number,
    title: PropTypes.string,
    description: PropTypes.string,
    steps: PropTypes.string,
    recipe_itens: PropTypes.arrayOf(PropTypes.shape({
      amount: PropTypes.number,
      item: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        description: PropTypes.string,
        measure_unity: PropTypes.string,
        amount: PropTypes.number,
        price: PropTypes.number,
        price_unit: PropTypes.string,
      })
    }))
  }),
};
