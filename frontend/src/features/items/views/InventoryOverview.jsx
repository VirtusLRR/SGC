import { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { useOutletContext } from 'react-router-dom';
import { Package, AlertTriangle, Clock, DollarSign, Bell } from 'lucide-react';
import { MetricCard } from '../../../components/MetricCard';
import { ItemsTable } from '../components/ItemsTable';
import { ItemFormModal } from '../components/ItemFormModal';
import { ConfirmDeleteModal } from '../components/ConfirmDeleteModal';
import { useItems, useInventorySummary } from '../hooks/useItems';
import './InventoryOverview.css';

/**
 * Tela Principal do Inventory Overview
 */
export const InventoryOverview = forwardRef((props, ref) => {
  // Recebe o contexto do Outlet (inventoryRef do AppLayout)
  const outletContext = useOutletContext();
  const inventoryRef = outletContext?.inventoryRef;
  const { items, loading, fetchItems, deleteItem, createItem, updateItem } = useItems();
  const { summary, fetchSummary } = useInventorySummary();
  const [searchTerm, setSearchTerm] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState(null);
  const searchTimeoutRef = useRef(null);

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

  useEffect(() => {
    loadData();
  }, []);

  // Expõe o método loadData para componentes pais via ref
  useImperativeHandle(ref, () => ({
    loadData
  }));

  // Conecta a ref do AppLayout com o método loadData
  useImperativeHandle(inventoryRef, () => ({
    loadData
  }));

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    
    // Cancela o timeout anterior se existir (debounce)
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    // Busca após 500ms de inatividade
    searchTimeoutRef.current = setTimeout(() => {
      fetchItems(value || null);
    }, 500);
  };

  // Limpa o timeout quando o componente desmontar
  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

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
          <h1>Visão Geral do Inventário</h1>
          <p>Gerencie e monitore seus itens do inventário</p>
        </div>
        <div className="inventory-header__search">
          <input
            type="text"
            placeholder="Buscar itens..."
            value={searchTerm}
            onChange={handleSearch}
            className="search-input"
          />
          <div className="notification-icon">
            <Bell size={20} />
            <span className="notification-badge">3</span>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="metrics-grid">
        <MetricCard
          icon={<DollarSign size={32} />}
          title="Valor Total do Inventário"
          value={`R$ ${(summary?.total_inventory_value || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          trend="up"
          trendValue="+8.5%"
          type="success"
        />
        <MetricCard
          icon={<Package size={32} />}
          title="Total de Itens"
          value={summary?.total_items || 0}
          subtitle={`${summary?.total_items || 0} itens`}
          type="info"
        />
        <MetricCard
          icon={<AlertTriangle size={32} />}
          title="Fora de Estoque"
          value={summary?.items_out_of_stock || 0}
          subtitle="Crítico"
          type="danger"
        />
        <MetricCard
          icon={<Clock size={32} />}
          title="Expirando em Breve"
          value={summary?.expiring_soon_count || 0}
          subtitle="Aviso"
          type="warning"
        />
      </div>

      {/* Inventory Items Section */}
      <div className="inventory-items">
        <div className="inventory-items__header">
          <h2>Itens do Inventário</h2>
          <div className="inventory-items__tabs">
            <button 
              className={`tab ${activeFilter === 'all' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('all')}
            >
              Todos os Itens
            </button>
            <button 
              className={`tab ${activeFilter === 'low-stock' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('low-stock')}
            >
              Estoque Baixo
            </button>
            <button 
              className={`tab ${activeFilter === 'expired' ? 'tab--active' : ''}`}
              onClick={() => setActiveFilter('expired')}
            >
              Expirados
            </button>
          </div>
        </div>

        <div className="inventory-items__actions">
          <button className="btn btn--primary" onClick={handleAddItem}>
            + Adicionar Novo Item
          </button>
        </div>

        <ItemsTable
          items={filteredItems}
          onEdit={handleEdit}
          onDelete={handleDelete}
          loading={loading}
        />

        {filteredItems.length > 0 && (
          <div className="pagination">
            <span className="pagination__info">
              Mostrando {filteredItems.length} de {summary?.total_items || 0} itens
            </span>
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
});

InventoryOverview.displayName = 'InventoryOverview';

