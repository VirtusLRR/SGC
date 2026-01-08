import { InventoryOverview } from '../features/items/views/InventoryOverview';

/**
 * Configuração de rotas da aplicação
 */
export const routes = [
  {
    path: '/items',
    element: <InventoryOverview />,
    name: 'Inventory Overview'
  },
  // Adicione mais rotas aqui conforme necessário
];
