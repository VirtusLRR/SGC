/**
 * @typedef {Object} Item
 * @property {number} id
 * @property {string} name
 * @property {string} measure_unity
 * @property {number} amount
 * @property {string|null} description
 * @property {number} price
 * @property {string|null} expiration_date
 * @property {string} create_at
 * @property {string|null} update_at
 */

/**
 * @typedef {Object} ItemRequest
 * @property {string} name
 * @property {string} measure_unity
 * @property {number} amount
 * @property {string|null} description
 * @property {number} price
 * @property {string|null} expiration_date
 */

/**
 * @typedef {Object} InventorySummary
 * @property {number} total_value
 * @property {number} total_items
 * @property {number} out_of_stock_count
 * @property {number} low_stock_count
 * @property {number} expiring_soon_count
 * @property {number} expired_count
 */

/**
 * @typedef {Object} ItemStatus
 * @property {'In Stock' | 'Low Stock' | 'Out of Stock' | 'Expiring Soon' | 'Expired'} status
 * @property {string} color
 */

export const ItemStatus = {
  IN_STOCK: 'In Stock',
  LOW_STOCK: 'Low Stock',
  OUT_OF_STOCK: 'Out of Stock',
  EXPIRING_SOON: 'Expiring Soon',
  EXPIRED: 'Expired'
};

export const StatusColors = {
  [ItemStatus.IN_STOCK]: 'green',
  [ItemStatus.LOW_STOCK]: 'yellow',
  [ItemStatus.OUT_OF_STOCK]: 'red',
  [ItemStatus.EXPIRING_SOON]: 'orange',
  [ItemStatus.EXPIRED]: 'red'
};
