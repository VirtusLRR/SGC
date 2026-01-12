import PropTypes from 'prop-types';
import { PERIOD_OPTIONS } from '../../types/statistics.types';
import './PeriodSelector.css';

/**
 * Componente seletor de período para filtrar estatísticas
 * @param {Object} props
 * @param {number} props.selectedPeriod - Período selecionado em dias
 * @param {Function} props.onPeriodChange - Callback quando o período muda
 * @param {Array} props.periods - Array de opções de período (opcional)
 */
export const PeriodSelector = ({
  selectedPeriod,
  onPeriodChange,
  periods = PERIOD_OPTIONS
}) => {
  return (
    <div className="period-selector">
      <span className="period-selector__label">Período:</span>
      <div className="period-selector__buttons">
        {periods.map((period) => (
          <button
            key={period.key}
            className={`period-selector__button ${
              selectedPeriod === period.value ? 'period-selector__button--active' : ''
            }`}
            onClick={() => onPeriodChange(period.value)}
            type="button"
          >
            {period.label}
          </button>
        ))}
      </div>
    </div>
  );
};

PeriodSelector.propTypes = {
  selectedPeriod: PropTypes.number.isRequired,
  onPeriodChange: PropTypes.func.isRequired,
  periods: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
      key: PropTypes.string.isRequired,
    })
  ),
};
