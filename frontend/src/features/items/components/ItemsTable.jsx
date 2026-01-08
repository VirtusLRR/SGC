import { useMemo } from 'react';
import PropTypes from 'prop-types';
import { ItemStatus, StatusColors } from '../types/item.types';
import './ItemsTable.css';

/**
 * Componente de Tabela de Itens
 */
export const ItemsTable = ({ 
  items, 
  onEdit, 
  onDelete, 
  loading = false 
}) => {
  /**
   * Determina o status de um item baseado em sua quantidade e data de vencimento
   */
  const getItemStatus = (item) => {
    if (!item.expiration_date) {
      if (item.amount === 0) return ItemStatus.OUT_OF_STOCK;
      if (item.amount <= 5) return ItemStatus.LOW_STOCK;
      return ItemStatus.IN_STOCK;
    }

    const expirationDate = new Date(item.expiration_date);
    const today = new Date();
    const daysUntilExpiration = Math.ceil((expirationDate - today) / (1000 * 60 * 60 * 24));

    if (daysUntilExpiration < 0) return ItemStatus.EXPIRED;
    if (daysUntilExpiration <= 7) return ItemStatus.EXPIRING_SOON;
    if (item.amount === 0) return ItemStatus.OUT_OF_STOCK;
    if (item.amount <= 5) return ItemStatus.LOW_STOCK;
    
    return ItemStatus.IN_STOCK;
  };

  /**
   * Formata a data de vencimento
   */
  const formatExpirationDate = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
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
   * Calcula o valor total do item
   */
  const getTotalValue = (item) => {
    return item.amount * (item.price || 0);
  };

  const processedItems = useMemo(() => {
    return items.map(item => ({
      ...item,
      status: getItemStatus(item),
      totalValue: getTotalValue(item),
    }));
  }, [items]);

  if (loading) {
    return (
      <div className="items-table-loading">
        <div className="spinner"></div>
        <p>Carregando itens...</p>
      </div>
    );
  }

  if (!items || items.length === 0) {
    return (
      <div className="items-table-empty">
        <p>Nenhum item encontrado</p>
      </div>
    );
  }

  return (
    <div className="items-table-container">
      <table className="items-table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" />
            </th>
            <th>Item Name</th>
            <th>Unit</th>
            <th>Quantity</th>
            <th>Unit Price</th>
            <th>Total Value</th>
            <th>Expiry Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {processedItems.map((item) => (
            <tr key={item.id}>
              <td>
                <input type="checkbox" />
              </td>
              <td>
                <div className="item-name-cell">
                  <div className={`item-icon item-icon--${item.name.charAt(0).toLowerCase()}`}>
                    {item.name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="item-name">{item.name}</div>
                    {item.description && (
                      <div className="item-sku">SKU: {item.description}</div>
                    )}
                  </div>
                </div>
              </td>
              <td>{item.measure_unity}</td>
              <td>{item.amount.toLocaleString('pt-BR')}</td>
              <td>{formatCurrency(item.price || 0)}</td>
              <td className="total-value">{formatCurrency(item.totalValue)}</td>
              <td>{formatExpirationDate(item.expiration_date)}</td>
              <td>
                <span className={`status-badge status-badge--${StatusColors[item.status]}`}>
                  {item.status}
                </span>
              </td>
              <td>
                <div className="action-buttons">
                  <button
                    className="action-btn action-btn--edit"
                    onClick={() => onEdit(item)}
                    title="Editar"
                  >
                    ✏️
                  </button>
                  <button
                    className="action-btn action-btn--delete"
                    onClick={() => onDelete(item.id)}
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
    </div>
  );
};

ItemsTable.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      measure_unity: PropTypes.string.isRequired,
      amount: PropTypes.number.isRequired,
      price: PropTypes.number,
      description: PropTypes.string,
      expiration_date: PropTypes.string,
    })
  ).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};
