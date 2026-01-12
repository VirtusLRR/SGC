import { useState, useCallback, useEffect } from 'react';
import { statisticsApi } from '../api/statisticsApi';

/**
 * Custom Hook para gerenciar dados de estatísticas e dashboard
 * Fornece estado e métodos para buscar e atualizar estatísticas
 */
export const useStatistics = (initialPeriod = 30, autoLoad = true) => {
  const [period, setPeriod] = useState(initialPeriod);
  const [summary, setSummary] = useState(null);
  const [dailyTransactions, setDailyTransactions] = useState([]);
  const [mostTransacted, setMostTransacted] = useState([]);
  const [consumptionRate, setConsumptionRate] = useState([]);
  const [priceAnalysis, setPriceAnalysis] = useState([]);
  const [dashboardData, setDashboardData] = useState(null);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [monthlyExpenses, setMonthlyExpenses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Busca resumo de transações do período
   */
  const fetchSummary = useCallback(async (days = period) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getTransactionSummary(days);
      setSummary(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar resumo';
      setError(errorMsg);
      console.error('Erro ao buscar resumo:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [period]);

  /**
   * Busca transações diárias do período
   */
  const fetchDailyTransactions = useCallback(async (days = period) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getDailyTransactions(days);
      setDailyTransactions(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar transações diárias';
      setError(errorMsg);
      console.error('Erro ao buscar transações diárias:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [period]);

  /**
   * Busca itens mais transacionados
   * @param {string} orderType - 'entrada', 'saida' ou 'all'
   * @param {number} limit - Quantidade de itens
   */
  const fetchMostTransacted = useCallback(async (orderType = 'all', limit = 10) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getMostTransactedItems(orderType, limit);
      setMostTransacted(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar itens mais transacionados';
      setError(errorMsg);
      console.error('Erro ao buscar itens mais transacionados:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Busca taxa de consumo por item
   */
  const fetchConsumptionRate = useCallback(async (days = period) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getConsumptionRate(days);
      setConsumptionRate(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar taxa de consumo';
      setError(errorMsg);
      console.error('Erro ao buscar taxa de consumo:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [period]);

  /**
   * Busca análise de preços
   */
  const fetchPriceAnalysis = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getPriceAnalysis();
      setPriceAnalysis(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar análise de preços';
      setError(errorMsg);
      console.error('Erro ao buscar análise de preços:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Busca dados do dashboard
   */
  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getDashboardData();
      setDashboardData(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar dados do dashboard';
      setError(errorMsg);
      console.error('Erro ao buscar dados do dashboard:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Busca transações recentes
   * @param {number} limit - Quantidade de transações
   */
  const fetchRecentTransactions = useCallback(async (limit = 10) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getTransactions(null, limit);
      setRecentTransactions(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar transações recentes';
      setError(errorMsg);
      console.error('Erro ao buscar transações recentes:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Busca gastos mensais
   * @param {number} months - Número de meses
   */
  const fetchMonthlyExpenses = useCallback(async (months = 6) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getMonthlyExpenses(months);
      setMonthlyExpenses(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar gastos mensais';
      setError(errorMsg);
      console.error('Erro ao buscar gastos mensais:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Busca todos os dados de estatísticas de uma vez (otimizado com Promise.all)
   */
  const fetchAllStatistics = useCallback(async (days = period) => {
    console.log('🔄 Buscando estatísticas para período:', days, 'dias');
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getAllStatisticsData(days);

      console.log('✅ Dados recebidos para', days, 'dias:', data);

      // Atualiza todos os estados de uma vez
      setSummary(data.summary);
      setDailyTransactions(data.dailyTransactions);
      setMostTransacted(data.mostTransacted);
      setConsumptionRate(data.consumptionRate);
      setPriceAnalysis(data.priceAnalysis);
      setDashboardData(data.dashboardData);
      setRecentTransactions(data.recentTransactions);

      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao carregar estatísticas';
      setError(errorMsg);
      console.error('❌ Erro ao carregar estatísticas:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [period]);

  /**
   * Atualiza o período e recarrega os dados
   * @param {number} newPeriod - Novo período em dias
   */
  const changePeriod = useCallback(async (newPeriod) => {
    console.log('🔄 Mudando período de', period, 'para', newPeriod, 'dias');
    setPeriod(newPeriod);
    // Os dados serão recarregados automaticamente pelo useEffect
  }, [period]);

  /**
   * Limpa o estado de erro
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  /**
   * Reseta todos os estados
   */
  const reset = useCallback(() => {
    setSummary(null);
    setDailyTransactions([]);
    setMostTransacted([]);
    setConsumptionRate([]);
    setPriceAnalysis([]);
    setDashboardData(null);
    setRecentTransactions([]);
    setError(null);
    setLoading(false);
  }, []);

  /**
   * Carrega os dados inicialmente se autoLoad estiver ativo
   */
  useEffect(() => {
    console.log('📡 useEffect disparado! Period:', period, 'AutoLoad:', autoLoad);
    if (autoLoad) {
      fetchAllStatistics(period);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [period, autoLoad]);

  return {
    // Estados
    period,
    summary,
    dailyTransactions,
    mostTransacted,
    consumptionRate,
    priceAnalysis,
    dashboardData,
    recentTransactions,
    monthlyExpenses,
    loading,
    error,

    // Métodos individuais
    fetchSummary,
    fetchDailyTransactions,
    fetchMostTransacted,
    fetchConsumptionRate,
    fetchPriceAnalysis,
    fetchDashboardData,
    fetchRecentTransactions,
    fetchMonthlyExpenses,

    // Métodos principais
    fetchAllStatistics,
    changePeriod,
    setPeriod,

    // Utilidades
    clearError,
    reset
  };
};

export default useStatistics;

