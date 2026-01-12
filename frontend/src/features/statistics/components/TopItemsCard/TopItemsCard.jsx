import PropTypes from 'prop-types';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';
import './TopItemsCard.css';

/**
 * Card com ranking dos itens mais transacionados
 * @param {Object} props
 * @param {Array} props.items - Lista de itens
 * @param {string} props.type - 'entrada', 'saida' ou 'all'
 * @param {number} props.limit - Limite de itens (padrão: 10)
 * @param {boolean} props.loading - Estado de carregamento
 */
export const TopItemsCard = ({ items = [], type = 'all', limit = 10, loading = false }) => {
  const getTypeLabel = () => {
    switch (type) {
      case 'entrada':
        return 'Entradas';
      case 'saida':
        return 'Saídas';
      default:
        return 'Transações';
    }
  };

  const getTypeIcon = () => {
    switch (type) {
      case 'entrada':
        return <TrendingUp size={20} />;
      case 'saida':
        return <TrendingDown size={20} />;
      default:
        return <BarChart3 size={20} />;
    }
  };

  const getTypeColor = () => {
    switch (type) {
      case 'entrada':
        return '#4caf50';
      case 'saida':
        return '#f44336';
      default:
        return '#2196f3';
    }
  };

  /**
   * Formata a quantidade com unidade apropriada
   */
  const formatQuantity = (quantity) => {
    if (quantity >= 1000) {
      // Provavelmente gramas ou ml, converter para kg/L
      return `${(quantity / 1000).toFixed(1)} kg`;
    } else if (quantity >= 10) {
      return `${quantity.toFixed(1)} un`;
    } else {
      return `${quantity.toFixed(2)} un`;
    }
  };

  const limitedItems = items.slice(0, limit);
  const maxQuantity = limitedItems.length > 0 ? Math.max(...limitedItems.map(i => i.total_quantity)) : 0;

  if (loading) {
    return (
      <div className="top-items-card">
        <div className="top-items-card__header">
          <h3 className="top-items-card__title">
            {getTypeIcon()} Top Itens - {getTypeLabel()}
          </h3>
        </div>
        <div className="top-items-card__loading">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="top-items-card__skeleton-item"></div>
          ))}
        </div>
      </div>
    );
  }

  if (limitedItems.length === 0) {
    return (
      <div className="top-items-card">
        <div className="top-items-card__header">
          <h3 className="top-items-card__title">
            {getTypeIcon()} Top Itens - {getTypeLabel()}
          </h3>
        </div>
        <div className="top-items-card__empty">
          <span className="top-items-card__empty-icon">
            <BarChart3 size={48} />
          </span>
          <p className="top-items-card__empty-text">Nenhum item encontrado</p>
        </div>
      </div>
    );
  }

  return (
    <div className="top-items-card">
      <div className="top-items-card__header">
        <h3 className="top-items-card__title">
          {getTypeIcon()} Top Itens - {getTypeLabel()}
        </h3>
      </div>

      <div className="top-items-card__list">
        {limitedItems.map((item, index) => {
          const percentage = maxQuantity > 0 ? ((item.total_quantity || 0) / maxQuantity) * 100 : 0;

          return (
            <div key={item.item_id} className="top-items-card__item">
              <div className="top-items-card__item-header">
                <span className="top-items-card__rank">#{index + 1}</span>
                <span className="top-items-card__item-name">{item.item_name || 'N/A'}</span>
              </div>

              <div className="top-items-card__item-details">
                <div className="top-items-card__bar-container">
                  <div
                    className="top-items-card__bar"
                    style={{
                      width: `${percentage}%`,
                      backgroundColor: getTypeColor(),
                    }}
                  ></div>
                </div>
                <div className="top-items-card__item-values">
                  <span className="top-items-card__item-quantity">
                    {formatQuantity(item.total_quantity || 0)}
                  </span>
                  {item.valor_total && (
                    <span className="top-items-card__item-money">
                      R$ {item.valor_total.toFixed(2)}
                    </span>
                  )}
                </div>
              </div>

              <div className="top-items-card__item-footer">
                <span className="top-items-card__item-info">
                  {item.total_transactions || 0} transações
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

TopItemsCard.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      item_id: PropTypes.number.isRequired,
      item_name: PropTypes.string.isRequired,
      total_quantity: PropTypes.number.isRequired,
      total_entradas: PropTypes.number,
      total_saidas: PropTypes.number,
      total_transactions: PropTypes.number.isRequired,
      valor_total: PropTypes.number,
    })
  ),
  type: PropTypes.oneOf(['entrada', 'saida', 'all']),
  limit: PropTypes.number,
  loading: PropTypes.bool,
};

