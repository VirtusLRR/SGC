import api from '../../../config/api';

/**
 * Item API Service
 * Mapeamento completo das rotas do backend
 */

export const itemsApi = {
  /**
   * GET /api/items
   * Retorna todos os itens ou busca por nome
   */
  getAllItems: async (name = null) => {
    const params = name ? { name } : {};
    const response = await api.get('/api/items', { params });
    return response.data;
  },

  /**
   * GET /api/items/:id
   * Retorna um item específico por ID
   */
  getItemById: async (id) => {
    const response = await api.get(`/api/items/${id}`);
    return response.data;
  },

  /**
   * POST /api/items
   * Cria um novo item
   */
  createItem: async (itemData) => {
    const response = await api.post('/api/items', itemData);
    return response.data;
  },

  /**
   * PUT /api/items/:id
   * Atualiza um item existente
   */
  updateItem: async (id, itemData) => {
    const response = await api.put(`/api/items/${id}`, itemData);
    return response.data;
  },

  /**
   * DELETE /api/items/:id
   * Remove um item
   */
  deleteItem: async (id) => {
    const response = await api.delete(`/api/items/${id}`);
    return response.data;
  },

  /**
   * GET /items/summary
   * Retorna resumo do inventário
   */
  getInventorySummary: async () => {
    const response = await api.get('/items/summary');
    return response.data;
  },

  /**
   * GET /items/low-stock/:threshold
   * Retorna itens com estoque baixo
   */
  getLowStockItems: async (threshold = 5) => {
    const response = await api.get(`/items/low-stock/${threshold}`);
    return response.data;
  },

  /**
   * GET /items/expiring/:days_ahead
   * Retorna itens próximos do vencimento
   */
  getExpiringItems: async (daysAhead = 7) => {
    const response = await api.get(`/items/expiring/${daysAhead}`);
    return response.data;
  },

  /**
   * GET /items/top-value/:top_n
   * Retorna itens ordenados por valor total
   */
  getTopValueItems: async (topN = 5) => {
    const response = await api.get(`/items/top-value/${topN}`);
    return response.data;
  },

  /**
   * GET /items/total-value/:id
   * Retorna o valor total de estoque de um item específico (preço × quantidade)
   */
  getTotalItemValue: async (id) => {
    const response = await api.get(`/items/total-value/${id}`);
    return response.data;
  },
};

/**
 * Dashboard API Service
 */
export const dashboardApi = {
  /**
   * GET /dashboard
   * Retorna dados consolidados para o dashboard
   */
  getDashboardData: async () => {
    const response = await api.get('/dashboard');
    return response.data;
  },
};
