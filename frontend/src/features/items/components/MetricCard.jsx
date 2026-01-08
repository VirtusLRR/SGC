import PropTypes from 'prop-types';
import './MetricCard.css';

/**
 * Componente de Card de Métrica
 */
export const MetricCard = ({ icon, title, value, subtitle, trend, trendValue, type = 'default' }) => {
  const getCardClass = () => {
    const baseClass = 'metric-card';
    return `${baseClass} ${baseClass}--${type}`;
  };

  return (
    <div className={getCardClass()}>
      <div className="metric-card__header">
        <div className="metric-card__icon">{icon}</div>
        {trend && (
          <div className={`metric-card__trend metric-card__trend--${trend}`}>
            {trend === 'up' ? '↑' : '↓'} {trendValue}
          </div>
        )}
      </div>
      
      <div className="metric-card__content">
        <h3 className="metric-card__title">{title}</h3>
        <div className="metric-card__value">{value}</div>
        {subtitle && <p className="metric-card__subtitle">{subtitle}</p>}
      </div>
    </div>
  );
};

MetricCard.propTypes = {
  icon: PropTypes.node.isRequired,
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  subtitle: PropTypes.string,
  trend: PropTypes.oneOf(['up', 'down']),
  trendValue: PropTypes.string,
  type: PropTypes.oneOf(['default', 'success', 'warning', 'danger', 'info']),
};
