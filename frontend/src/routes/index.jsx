import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '../components/index.js';
import { InventoryOverview } from '../features/items/views/InventoryOverview';
import { RecipesOverview } from '../features/recipes/views/RecipesOverview';
import { StatisticsOverview } from '../features/statistics';

/**
 * Configuração de rotas da aplicação com React Router v6
 */
export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/items" replace />
      },
      {
        path: 'items',
        element: <InventoryOverview/>
      },
      {
        path: 'recipes',
        element: <RecipesOverview/>
      },
      {
        path: 'statistics',
        element: <StatisticsOverview/>
      },
      {
        path: '*',
        element: <Navigate to="/items" replace />
      }
    ]
  }
]);
