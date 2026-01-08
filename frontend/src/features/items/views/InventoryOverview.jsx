import { useState, useEffect } from 'react';
import { MetricCard } from '../../../components/MetricCard';
import { ItemsTable } from '../components/ItemsTable';
import { ItemFormModal } from '../components/ItemFormModal';
import { ConfirmDeleteModal } from '../components/ConfirmDeleteModal';
import { useItems, useInventorySummary } from '../hooks/useItems';
import './InventoryOverview.css';

/**
 * Tela Principal do Inventory Overview
 */
export const InventoryOverview = () => {
  const { items, loading, fetchItems, deleteItem, createItem, updateItem } = useItems();
  const { summary, fetchSummary } = useInventorySummary();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      await Promise.all([
        fetchItems(),
        fetchSummary()
      ]);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    }
  };

  const handleSearch = async (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    // Busca após 500ms de inatividade
    setTimeout(() => {
      if (value === searchTerm) {
        fetchItems(value || null);
      }
    }, 500);
  };

  const handleDelete = async (id) => {
    const item = items.find(i => i.id === id);
    if (item) {
      setItemToDelete(item);
      setIsDeleteModalOpen(true);
    }
  };

  const handleConfirmDelete = async () => {
    if (!itemToDelete) return;
    
    try {
      await deleteItem(itemToDelete.id);
      await fetchSummary(); // Atualiza resumo após deletar
      setIsDeleteModalOpen(false);
      setItemToDelete(null);
    } catch (error) {
      alert('Erro ao deletar item');
    }
  };

  const handleCloseDeleteModal = () => {
    setIsDeleteModalOpen(false);
    setItemToDelete(null);
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setIsModalOpen(true);
  };

  const handleAddItem = () => {
    setEditingItem(null);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingItem(null);
  };

  const handleSubmitForm = async (formData) => {
    try {
      if (editingItem) {
        // Atualizar item existente
        await updateItem(editingItem.id, formData);
      } else {
        // Criar novo item
        await createItem(formData);
      }
      
      // Recarrega dados
      await loadData();
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro ao salvar item');
      throw error;
    }
  };

  const handleExport = () => {
    // TODO: Implementar exportação
    console.log('Exportar dados');
  };

  const filteredItems = items.filter(item => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'low-stock') return item.amount <= 5;
    if (activeFilter === 'expired') {
      if (!item.expiration_date) return false;
      return new Date(item.expiration_date) < new Date();
    }
    return true;
  });

  return (
    <div className="inventory-overview">
      {/* Header */}
      <div className="inventory-header">
        <div className="inventory-header__content">
          <h1>Inventory Overview</h1>
          <p>Manage and monitor your inventory items</p>
        </div>
        <div className="inventory-header__search">
          <input
            type="text"
            placeholder="Search items..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
          <div className="notification-icon">
            🔔
            <span className="notification-badge">3</span>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        <MetricCard
          icon="$"
          title="Total Inventory Value"
          value={`R$ ${(summary?.total_value || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          trend="up"
          trendValue="+8.5%"
          type="success"
        />
        <MetricCard
          icon="📦"
          title="Total Items"
          value={summary?.total_items || 0}
          subtitle={`${summary?.total_items || 0} items`}
          type="info"
        />
        <MetricCard
          icon="⚠️"
          title="Out of Stock"
          value={summary?.out_of_stock_count || 0}
          subtitle="Critical"
          type="danger"
        />
        <MetricCard
          icon="⏰"
          title="Expiring Soon"
          value={summary?.expiring_soon_count || 0}
          subtitle="Warning"
          type="warning"
        />
      </div>

      {/* Inventory Items Section */}
      <div className="inventory-items">
        <div className="inventory-items__header">
          <h2>Inventory Items</h2>
          <div className="inventory-items__tabs">
            <button 
              className={`tab ${activeFilter === 'all' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('all')}
            >
              All Items
            </button>
            <button 
              className={`tab ${activeFilter === 'low-stock' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('low-stock')}
            >
              Low Stock
            </button>
            <button 
              className={`tab ${activeFilter === 'expired' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('expired')}
            >
              Expired
            </button>
          </div>
        </div>

        <div className="inventory-items__actions">
          <button className="btn btn--secondary" onClick={handleExport}>
            ⬇️ Export
          </button>
          <button className="btn btn--primary" onClick={handleAddItem}>
            + Add New Item
          </button>
        </div>

        <ItemsTable
          items={filteredItems}
          onEdit={handleEdit}
          onDelete={handleDelete}
          loading={loading}
        />

        {/* Pagination */}
        {filteredItems.length > 0 && (
          <div className="pagination">
            <span className="pagination__info">
              Showing {filteredItems.length} of {summary?.total_items || 0} items
            </span>
            <div className="pagination__controls">
              <button className="pagination__btn">Previous</button>
              <button className="pagination__btn pagination__btn--active">1</button>
              <button className="pagination__btn">2</button>
              <button className="pagination__btn">3</button>
              <button className="pagination__btn">Next</button>
            </div>
          </div>
        )}
      </div>

      {/* Modal de Formulário */}
      <ItemFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSubmitForm}
        item={editingItem}
        loading={loading}
      />

      {/* Modal de Confirmação de Exclusão */}
      <ConfirmDeleteModal
        isOpen={isDeleteModalOpen}
        onClose={handleCloseDeleteModal}
        onConfirm={handleConfirmDelete}
        itemName={itemToDelete?.name || ''}
        loading={loading}
      />
    </div>
  );
};
