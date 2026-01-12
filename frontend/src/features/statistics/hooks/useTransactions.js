import { useState } from 'react';
import { statisticsApi } from '../api/statisticsApi';

/**
 * Custom Hook para gerenciar operações de transações
 * Fornece estado e métodos para CRUD de transações
 */
export const useTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Busca todas as transações ou filtra por item_id
   * @param {number|null} itemId - ID do item para filtrar
   * @param {number|null} limit - Limite de resultados
   */
  const fetchTransactions = async (itemId = null, limit = null) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getTransactions(itemId, limit);
      setTransactions(data);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar transações';
      setError(errorMsg);
      console.error('Erro ao buscar transações:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Busca uma transação específica por ID
   * @param {number} id - ID da transação
   */
  const fetchTransactionById = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const data = await statisticsApi.getTransactionById(id);
      return data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao buscar transação';
      setError(errorMsg);
      console.error('Erro ao buscar transação:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cria uma nova transação
   * @param {Object} transactionData - Dados da transação
   */
  const createTransaction = async (transactionData) => {
    setLoading(true);
    setError(null);
    try {
      const newTransaction = await statisticsApi.createTransaction(transactionData);
      setTransactions(prev => [newTransaction, ...prev]);
      return newTransaction;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao criar transação';
      setError(errorMsg);
      console.error('Erro ao criar transação:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Atualiza uma transação existente
   * @param {number} id - ID da transação
   * @param {Object} transactionData - Dados atualizados
   */
  const updateTransaction = async (id, transactionData) => {
    setLoading(true);
    setError(null);
    try {
      const updatedTransaction = await statisticsApi.updateTransaction(id, transactionData);
      setTransactions(prev =>
        prev.map(transaction =>
          transaction.id === id ? updatedTransaction : transaction
        )
      );
      return updatedTransaction;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao atualizar transação';
      setError(errorMsg);
      console.error('Erro ao atualizar transação:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Remove uma transação
   * @param {number} id - ID da transação
   */
  const deleteTransaction = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await statisticsApi.deleteTransaction(id);
      setTransactions(prev => prev.filter(transaction => transaction.id !== id));
      return true;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Erro ao deletar transação';
      setError(errorMsg);
      console.error('Erro ao deletar transação:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Limpa o estado de erro
   */
  const clearError = () => {
    setError(null);
  };

  /**
   * Reseta o estado do hook
   */
  const reset = () => {
    setTransactions([]);
    setError(null);
    setLoading(false);
  };

  return {
    transactions,
    loading,
    error,
    fetchTransactions,
    fetchTransactionById,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    clearError,
    reset
  };
};

export default useTransactions;

