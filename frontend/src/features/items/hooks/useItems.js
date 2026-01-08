import { useState } from 'react';
import { itemsApi } from '../api/itemsApi';

/**
 * Custom Hook para gerenciar operações de itens
 */
export const useItems = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchItems = async (name = null) => {
    setLoading(true);
    setError(null);
    try {
      const data = await itemsApi.getAllItems(name);
      setItems(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar itens');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const createItem = async (itemData) => {
    setLoading(true);
    setError(null);
    try {
      const newItem = await itemsApi.createItem(itemData);
      setItems(prev => [...prev, newItem]);
      return newItem;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateItem = async (id, itemData) => {
    setLoading(true);
    setError(null);
    try {
      const updatedItem = await itemsApi.updateItem(id, itemData);
      setItems(prev => prev.map(item => item.id === id ? updatedItem : item));
      return updatedItem;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao atualizar item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await itemsApi.deleteItem(id);
      setItems(prev => prev.filter(item => item.id !== id));
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao deletar item');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    items,
    loading,
    error,
    fetchItems,
    createItem,
    updateItem,
    deleteItem,
  };
};

/**
 * Custom Hook para gerenciar resumo do inventário
 */
export const useInventorySummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await itemsApi.getInventorySummary();
      setSummary(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar resumo');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    summary,
    loading,
    error,
    fetchSummary,
  };
};
