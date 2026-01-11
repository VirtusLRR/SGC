/**
 * @typedef {Object} Recipe
 * @property {number} id
 * @property {string} title
 * @property {string} steps
 * @property {string|null} description
 */

/**
 * @typedef {Object} RecipeRequest
 * @property {string} title
 * @property {string} steps
 * @property {string|null} description
 */

/**
 * @typedef {Object} RecipeIngredient
 * @property {number} item_id
 * @property {string} item_name
 * @property {number} required_amount
 * @property {string} measure_unity
 * @property {number} unit_price
 * @property {string} price_reference
 * @property {number} total_cost
 */

/**
 * @typedef {Object} RecipeCost
 * @property {number} recipe_id
 * @property {string} recipe_title
 * @property {number} total_cost
 * @property {RecipeIngredient[]} ingredients
 */

/**
 * @typedef {Object} FeasibleRecipe
 * @property {number} recipe_id
 * @property {string} recipe_title
 * @property {number} total_cost
 */

/**
 * @typedef {Object} MostUsedIngredient
 * @property {number} item_id
 * @property {string} item_name
 * @property {number} recipe_count
 * @property {number} total_amount_used
 */

/**
 * @typedef {Object} RecipeStatus
 * @property {'Feasible' | 'Missing Items' | 'In Stock'} status
 * @property {string} color
 */

export const RecipeStatus = {
  FEASIBLE: 'Feasible',
  MISSING_ITEMS: 'Missing Items',
  IN_STOCK: 'In Stock'
};

export const StatusColors = {
  [RecipeStatus.FEASIBLE]: 'green',
  [RecipeStatus.MISSING_ITEMS]: 'red',
  [RecipeStatus.IN_STOCK]: 'blue'
};
