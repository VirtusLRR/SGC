import { NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';
import './Sidebar.css';

/**
 * Componente Sidebar - Navegação lateral da aplicação
 */
export const Sidebar = ({ items, isCollapsed, onToggle }) => {
  return (
    <aside className={`sidebar ${isCollapsed ? 'sidebar--collapsed' : ''}`}>
      <div className="sidebar__header">
        <button
          className="sidebar__toggle"
          onClick={onToggle}
          aria-label={isCollapsed ? 'Expandir sidebar' : 'Colapsar sidebar'}
          title={isCollapsed ? 'Expandir' : 'Colapsar'}
        >
          {isCollapsed ? '☰' : '×'}
        </button>
        {!isCollapsed && (
          <div className="sidebar__logo">
            <span className="sidebar__logo-text">SGC</span>
          </div>
        )}
      </div>

      <nav className="sidebar__nav" aria-label="Navegação principal">
        <ul className="sidebar__nav-list">
          {items.map((item) => (
            <li key={item.path} className="sidebar__nav-list-item">
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `sidebar__nav-item ${isActive ? 'sidebar__nav-item--active' : ''}`
                }
                title={isCollapsed ? item.label : ''}
              >
                <span className="sidebar__icon" aria-hidden="true">
                  {item.icon}
                </span>
                {!isCollapsed && (
                  <span className="sidebar__label">{item.label}</span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

Sidebar.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      path: PropTypes.string.isRequired,
      icon: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
    })
  ).isRequired,
  isCollapsed: PropTypes.bool.isRequired,
  onToggle: PropTypes.func.isRequired,
};

