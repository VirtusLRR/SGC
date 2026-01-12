import PropTypes from 'prop-types';
import { useState } from 'react';
import './ConsumptionTable.css';

/**
 * Tabela de taxa de consumo por item
 * @param {Object} props
 * @param {Array} props.data - Dados de consumo
 * @param {boolean} props.loading - Estado de carregamento
 */
export const ConsumptionTable = ({ data = [], loading = false }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = [...data].sort((a, b) => {
    if (!sortConfig.key) return 0;

    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    if (aValue === null) return 1;
    if (bValue === null) return -1;

    if (aValue < bValue) {
      return sortConfig.direction === 'asc' ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortConfig.direction === 'asc' ? 1 : -1;
    }
    return 0;
  });

  const getStatusClass = (diasParaEsgotamento) => {
    if (diasParaEsgotamento === null) return 'normal';
    if (diasParaEsgotamento < 7) return 'critico';
    if (diasParaEsgotamento < 14) return 'alerta';
    return 'normal';
  };

  const getStatusLabel = (diasParaEsgotamento) => {
    if (diasParaEsgotamento === null) return 'Estável';
    if (diasParaEsgotamento < 7) return `${diasParaEsgotamento} dias`;
    if (diasParaEsgotamento < 14) return `${diasParaEsgotamento} dias`;
    return `${diasParaEsgotamento} dias`;
  };

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) return '⇅';
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  if (loading) {
    return (
      <div className="consumption-table">
        <h3 className="consumption-table__title">Taxa de Consumo por Item</h3>
        <div className="consumption-table__loading">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="consumption-table__skeleton-row"></div>
          ))}
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="consumption-table">
        <h3 className="consumption-table__title">Taxa de Consumo por Item</h3>
        <div className="consumption-table__empty">
          <span className="consumption-table__empty-icon">📦</span>
          <p className="consumption-table__empty-text">Nenhum dado de consumo disponível</p>
        </div>
      </div>
    );
  }

  return (
    <div className="consumption-table">
      <h3 className="consumption-table__title">Taxa de Consumo por Item</h3>
      <div className="consumption-table__wrapper">
        <table className="consumption-table__table">
          <thead>
            <tr>
              <th onClick={() => handleSort('item_name')}>
                Item {getSortIcon('item_name')}
              </th>
              <th onClick={() => handleSort('total_consumido')}>
                Total Consumido {getSortIcon('total_consumido')}
              </th>
              <th onClick={() => handleSort('taxa_diaria')}>
                Taxa Diária {getSortIcon('taxa_diaria')}
              </th>
              <th onClick={() => handleSort('estoque_atual')}>
                Estoque Atual {getSortIcon('estoque_atual')}
              </th>
              <th onClick={() => handleSort('dias_para_esgotamento')}>
                Dias p/ Esgotamento {getSortIcon('dias_para_esgotamento')}
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((item) => (
              <tr
                key={item.item_id}
                className={`consumption-table__row consumption-table__row--${getStatusClass(
                  item.dias_para_esgotamento
                )}`}
              >
                <td className="consumption-table__cell--name">{item.item_name || 'N/A'}</td>
                <td className="consumption-table__cell--number">
                  {item.total_consumido ? item.total_consumido.toFixed(2) : '0.00'}
                </td>
                <td className="consumption-table__cell--number">
                  {item.taxa_diaria ? item.taxa_diaria.toFixed(2) : '0.00'}/dia
                </td>
                <td className="consumption-table__cell--number">{item.estoque_atual ?? 0}</td>
                <td className="consumption-table__cell--status">
                  <span
                    className={`consumption-table__status consumption-table__status--${getStatusClass(
                      item.dias_para_esgotamento
                    )}`}
                  >
                    {getStatusLabel(item.dias_para_esgotamento)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

ConsumptionTable.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      item_id: PropTypes.number.isRequired,
      item_name: PropTypes.string.isRequired,
      total_consumido: PropTypes.number.isRequired,
      taxa_diaria: PropTypes.number.isRequired,
      estoque_atual: PropTypes.number.isRequired,
      dias_para_esgotamento: PropTypes.number,
      status: PropTypes.string,
    })
  ),
  loading: PropTypes.bool,
};

