import api from '../../../config/api';

/**
 * Recipe API Service
 * Mapeamento completo das rotas do backend
 */

export const recipesApi = {
  /**
   * GET /api/recipes
   * Retorna todas as receitas ou busca por nome
   */
  getAllRecipes: async (name = null) => {
    const params = name ? { name } : {};
    const response = await api.get('/api/recipes', { params });
    return response.data;
  },

  /**
   * GET /api/recipes/:id
   * Retorna uma receita específica por ID
   */
  getRecipeById: async (id) => {
    const response = await api.get(`/api/recipes/${id}`);
    return response.data;
  },

  /**
   * POST /api/recipes
   * Cria uma nova receita
   */
  createRecipe: async (recipeData) => {
    const response = await api.post('/api/recipes', recipeData);
    return response.data;
  },

  /**
   * PUT /api/recipes/:id
   * Atualiza uma receita existente
   */
  updateRecipe: async (id, recipeData) => {
    const response = await api.put(`/api/recipes/${id}`, recipeData);
    return response.data;
  },

  /**
   * DELETE /api/recipes/:id
   * Remove uma receita
   */
  deleteRecipe: async (id) => {
    const response = await api.delete(`/api/recipes/${id}`);
    return response.data;
  },

  /**
   * GET /recipes/costs
   * Retorna todas as receitas com seus custos calculados
   */
  getAllRecipesCosts: async () => {
    const response = await api.get('/recipes/costs');
    return response.data;
  },

  /**
   * GET /recipes/cost/:recipe_id
   * Retorna o custo de uma receita específica com detalhes dos ingredientes
   */
  getRecipeCost: async (recipeId) => {
    const response = await api.get(`/recipes/cost/${recipeId}`);
    return response.data;
  },

  /**
   * GET /recipes/feasible
   * Retorna receitas que podem ser feitas com o estoque atual
   */
  getFeasibleRecipes: async () => {
    const response = await api.get('/recipes/feasible');
    return response.data;
  },

  /**
   * GET /recipes/popular-ingredients/:limit
   * Retorna os ingredientes mais utilizados em receitas
   */
  getMostUsedIngredients: async (limit = 10) => {
    const response = await api.get(`/recipes/popular-ingredients/${limit}`);
    return response.data;
  },
};
