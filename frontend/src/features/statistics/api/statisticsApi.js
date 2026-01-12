import api from '../../../config/api';

/**
 * Statistics API Service
 * Mapeamento completo das rotas de transactions e dashboard do backend
 */

export const statisticsApi = {
  /**
   * GET /api/transactions
   * Retorna todas as transações ou filtra por item_id
   * @param {number|null} itemId - ID do item para filtrar (opcional)
   * @param {number|null} limit - Limite de resultados (opcional)
   */
  getTransactions: async (itemId = null, limit = null) => {
    const params = {};
    if (itemId) params.item_id = itemId;
    if (limit) params.limit = limit;

    const response = await api.get('/api/transactions', { params });
    const data = response.data || [];

    // Mapear campos do backend para o frontend
    return data.map(transaction => ({
      id: transaction.id,
      item_id: transaction.item_id,
      item_name: transaction.item_name || `Item #${transaction.item_id}`, // Fallback se não houver nome
      type: transaction.order_type, // Backend: order_type → Frontend: type
      order_type: transaction.order_type, // Manter também para compatibilidade
      quantity: transaction.amount || 0, // Backend: amount → Frontend: quantity
      amount: transaction.amount, // Manter também
      price: transaction.price || 0,
      total_value: transaction.price && transaction.amount ? transaction.price * transaction.amount : 0,
      description: transaction.description || '',
      date: transaction.create_at, // Backend: create_at → Frontend: date
      created_at: transaction.create_at, // Manter também
      create_at: transaction.create_at, // Manter original
    }));
  },

  /**
   * GET /api/transactions/:id
   * Retorna detalhes de uma transação específica
   * @param {number} id - ID da transação
   */
  getTransactionById: async (id) => {
    const response = await api.get(`/api/transactions/${id}`);
    return response.data;
  },

  /**
   * POST /api/transactions
   * Cria uma nova transação
   * @param {Object} transactionData - Dados da transação
   */
  createTransaction: async (transactionData) => {
    const response = await api.post('/api/transactions', transactionData);
    return response.data;
  },

  /**
   * PUT /api/transactions/:id
   * Atualiza uma transação existente
   * @param {number} id - ID da transação
   * @param {Object} transactionData - Dados atualizados
   */
  updateTransaction: async (id, transactionData) => {
    const response = await api.put(`/api/transactions/${id}`, transactionData);
    return response.data;
  },

  /**
   * DELETE /api/transactions/:id
   * Remove uma transação
   * @param {number} id - ID da transação
   */
  deleteTransaction: async (id) => {
    const response = await api.delete(`/api/transactions/${id}`);
    return response.data;
  },

  /**
   * GET /transactions/summary/:days
   * Retorna resumo de transações por período
   * @param {number} days - Número de dias para análise (padrão: 30)
   * @returns {Object} Resumo com total de transações, valores, etc.
   */
  getTransactionSummary: async (days = 30) => {
    const response = await api.get(`/transactions/summary/${days}`);
    const data = response.data;

    // Mapear dados do backend para o formato esperado pelo frontend
    return {
      period: data.period,
      total_transactions: (data.entries?.count || 0) + (data.exits?.count || 0),
      total_value: (data.entries?.total_value || 0) + (data.exits?.total_value || 0),
      total_entries: data.entries?.count || 0,
      total_exits: data.exits?.count || 0,
      value_entries: data.entries?.total_value || 0,
      value_exits: data.exits?.total_value || 0,
      balance: data.balance,
      // Manter dados originais também
      entries: data.entries,
      exits: data.exits,
    };
  },

  /**
   * GET /transactions/most-transacted/:limit/:order_type
   * Retorna os itens mais transacionados

   * @param {string} orderType - Tipo: 'entrada', 'saida', null para todos (padrão: null)
   * @param {number} limit - Quantidade de itens (padrão: 10)
   * @returns {Array} Lista de itens mais transacionados
   */
  getMostTransactedItems: async (orderType = null, limit = 10) => {
    // Se orderType for 'all', converter para 'none' para o backend não filtrar
    const type = (orderType === 'all' || !orderType) ? 'none' : orderType;
    const url = `/transactions/most-transacted/${limit}/${type}`;

    const response = await api.get(url);

    // Mapear dados do backend para o formato esperado pelo frontend
    const data = response.data || [];

    const mapped = data.map(item => ({
      item_id: item.item_id,
      item_name: item.item_name,
      total_transactions: item.transaction_count || 0,
      total_quantity: item.total_amount || 0,
      valor_total: item.total_value || 0,
    }));

    return mapped;
  },

  /**
   * GET /transactions/daily/:days
   * Retorna transações agrupadas por dia
   * @param {number} days - Número de dias para análise (padrão: 30)
   * @returns {Array} Transações diárias com contagem de entradas/saídas
   */
  getDailyTransactions: async (days = 30) => {
    const response = await api.get(`/transactions/daily/${days}`);
    const data = response.data || [];

    // Agrupar por data (backend retorna uma linha por tipo)
    const grouped = {};

    data.forEach(item => {
      const date = item.date;
      if (!grouped[date]) {
        grouped[date] = { date, entrada: 0, saida: 0 };
      }

      // Normalizar tipo (pode vir como 'entrada', 'saída', 'sada', etc)
      const type = item.order_type?.toLowerCase();
      if (type === 'entrada') {
        grouped[date].entrada = item.count || 0;
      } else if (type === 'saida' || type === 'saída') {
        grouped[date].saida = item.count || 0;
      }
    });

    // Converter objeto para array e ordenar por data
    return Object.values(grouped).sort((a, b) =>
      new Date(a.date) - new Date(b.date)
    );
  },

  /**
   * GET /transactions/consumption-rate/:days
   * Retorna taxa de consumo por item
   * @param {number} days - Número de dias para análise (padrão: 30)
   * @returns {Array} Taxa de consumo de cada item com previsão de esgotamento
   */
  getConsumptionRate: async (days = 30) => {
    const response = await api.get(`/transactions/consumption-rate/${days}`);
    const data = response.data || [];

    // Mapear campos do backend para o frontend
    return data.map(item => ({
      item_id: item.item_id,
      item_name: item.item_name,
      estoque_atual: item.current_stock || 0,
      total_consumido: item.total_consumed || 0,
      taxa_diaria: item.daily_average || 0,
      dias_para_esgotamento: item.days_until_stockout,
    }));
  },

  /**
   * GET /transactions/price-analysis
   * Retorna análise de preços médios por item
   * @returns {Array} Análise de preços com média, min, max, variação
   */
  getPriceAnalysis: async () => {
    const response = await api.get('/transactions/price-analysis');
    return response.data;
  },

  /**
   * GET /dashboard
   * Retorna dados consolidados do dashboard
   * @returns {Object} Dados completos: inventário, transações, alertas, etc.
   */
  getDashboardData: async () => {
    const response = await api.get('/dashboard');
    return response.data;
  },

  /**
   * GET /transactions/monthly-expenses
   * Retorna gastos mensais (entradas/compras) com comparação entre meses
   * @param {number} months - Número de meses para análise (padrão: 6)
   * @returns {Array} Gastos mensais com diferença e percentual vs mês anterior
   */
  getMonthlyExpenses: async (months = 6) => {
    const response = await api.get(`/transactions/monthly-expenses`, { params: { months } });
    return response.data;
  },

  /**
   * Método auxiliar para buscar múltiplos dados de uma vez
   * @param {number} days - Período para análise
   * @returns {Object} Objeto com todos os dados necessários para o dashboard
   */
  /**
   * Método auxiliar para buscar múltiplos dados de uma vez
   * Agora com tratamento individual de erros para evitar que uma falha bloqueie tudo
   * @param {number} days - Período para análise
   * @returns {Object} Objeto com todos os dados necessários para o dashboard
   */
  getAllStatisticsData: async (days = 30) => {
    // Helper para capturar erros sem parar o Promise.all
    const safeCall = async (fn, fallback = null, label = 'Chamada') => {
      try {
        const result = await fn();
        return result;
      } catch (error) {
        console.error(`❌ ${label} falhou:`, error.message);
        return fallback;
      }
    };

    const [
      summary,
      dailyTransactions,
      mostTransacted,
      consumptionRate,
      priceAnalysis,
      dashboardData,
      recentTransactions
    ] = await Promise.all([
      safeCall(() => statisticsApi.getTransactionSummary(days), null, 'Summary'),
      safeCall(() => statisticsApi.getDailyTransactions(days), [], 'Daily Transactions'),
      safeCall(() => statisticsApi.getMostTransactedItems(null, 10), [], 'Most Transacted'),
      safeCall(() => statisticsApi.getConsumptionRate(days), [], 'Consumption Rate'),
      safeCall(() => statisticsApi.getPriceAnalysis(), [], 'Price Analysis'),
      safeCall(() => statisticsApi.getDashboardData(), null, 'Dashboard Data'),
      safeCall(() => statisticsApi.getTransactions(null, 10), [], 'Recent Transactions')
    ]);


    return {
      summary,
      dailyTransactions,
      mostTransacted,
      consumptionRate,
      priceAnalysis,
      dashboardData,
      recentTransactions
    };
  }
};

export default statisticsApi;

