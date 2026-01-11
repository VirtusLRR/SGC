import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '../components/index.js';
import { InventoryOverview } from '../features/items/views/InventoryOverview';

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
        element: (
          <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>📝 Receitas</h1>
            <p>Em Desenvolvimento...</p>
          </div>
        )
      },
      {
        path: 'statistics',
        element: (
          <div style={{ padding: '40px', textAlign: 'center' }}>
            <h1>📊 Estatísticas</h1>
            <p>Em Desenvolvimento...</p>
          </div>
        )
      },
      {
        path: '*',
        element: <Navigate to="/items" replace />
      }
    ]
  }
]);
