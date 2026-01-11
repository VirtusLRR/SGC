import { useState } from 'react';
import { recipesApi } from '../api/recipesApi';

/**
 * Custom Hook para gerenciar operações de receitas
 */
export const useRecipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecipes = async (name = null) => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipesApi.getAllRecipes(name);
      setRecipes(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar receitas');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const createRecipe = async (recipeData) => {
    setLoading(true);
    setError(null);
    try {
      const newRecipe = await recipesApi.createRecipe(recipeData);
      setRecipes(prev => [...prev, newRecipe]);
      return newRecipe;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar receita');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const updateRecipe = async (id, recipeData) => {
    setLoading(true);
    setError(null);
    try {
      const updatedRecipe = await recipesApi.updateRecipe(id, recipeData);
      setRecipes(prev => prev.map(recipe => recipe.id === id ? updatedRecipe : recipe));
      return updatedRecipe;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao atualizar receita');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteRecipe = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await recipesApi.deleteRecipe(id);
      setRecipes(prev => prev.filter(recipe => recipe.id !== id));
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao deletar receita');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    recipes,
    loading,
    error,
    fetchRecipes,
    createRecipe,
    updateRecipe,
    deleteRecipe,
  };
};

/**
 * Custom Hook para gerenciar resumo de receitas
 */
export const useRecipesSummary = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      const [allRecipes, feasibleRecipes, mostUsedIngredients] = await Promise.all([
        recipesApi.getAllRecipes(),
        recipesApi.getFeasibleRecipes(),
        recipesApi.getMostUsedIngredients(10)
      ]);
      
      const summary = {
        total_recipes: allRecipes.length,
        feasible_recipes: feasibleRecipes.length,
        feasible_percentage: allRecipes.length > 0 
          ? ((feasibleRecipes.length / allRecipes.length) * 100).toFixed(1)
          : 0,
        most_used_ingredients: mostUsedIngredients,
      };
      
      setSummary(summary);
      return summary;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar resumo de receitas');
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

/**
 * Custom Hook para gerenciar custos de receitas
 */
export const useRecipeCosts = () => {
  const [recipeCosts, setRecipeCosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecipeCosts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipesApi.getAllRecipesCosts();
      setRecipeCosts(data);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar custos de receitas');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const fetchRecipeCost = async (recipeId) => {
    setLoading(true);
    setError(null);
    try {
      const data = await recipesApi.getRecipeCost(recipeId);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar custo da receita');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    recipeCosts,
    loading,
    error,
    fetchRecipeCosts,
    fetchRecipeCost,
  };
};
