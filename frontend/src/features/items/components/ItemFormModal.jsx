import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Modal } from '../../../components/Modal';
import './ItemFormModal.css';

/**
 * Modal de formulário para criar/editar item
 */
export const ItemFormModal = ({ 
  isOpen, 
  onClose, 
  onSubmit, 
  item = null,
  loading = false 
}) => {
  const isEditMode = !!item;
  
  const [formData, setFormData] = useState({
    name: '',
    measure_unity: '',
    amount: 0,
    description: '',
    price: 0,
    expiration_date: '',
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (item) {
      setFormData({
        name: item.name || '',
        measure_unity: item.measure_unity || '',
        amount: item.amount || 0,
        description: item.description || '',
        price: item.price || 0,
        expiration_date: item.expiration_date 
          ? new Date(item.expiration_date).toISOString().split('T')[0] 
          : '',
      });
    } else {
      resetForm();
    }
  }, [item, isOpen]);

  const resetForm = () => {
    setFormData({
      name: '',
      measure_unity: '',
      amount: 0,
      description: '',
      price: 0,
      expiration_date: '',
    });
    setErrors({});
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Remove erro do campo ao editar
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    }

    if (!formData.measure_unity.trim()) {
      newErrors.measure_unity = 'Unidade de medida é obrigatória';
    }

    if (formData.amount < 0) {
      newErrors.amount = 'Quantidade não pode ser negativa';
    }

    if (formData.price < 0) {
      newErrors.price = 'Preço não pode ser negativo';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      const submitData = {
        ...formData,
        amount: Number(formData.amount),
        price: Number(formData.price),
        expiration_date: formData.expiration_date || null,
      };

      await onSubmit(submitData);
      resetForm();
      onClose();
    } catch (error) {
      console.error('Erro ao salvar item:', error);
    }
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title={isEditMode ? 'Editar Item' : 'Adicionar Novo Item'}
      size="medium"
    >
      <form onSubmit={handleSubmit} className="item-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="name" className="form-label">
              Nome do Item <span className="required">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={`form-input ${errors.name ? 'form-input--error' : ''}`}
              placeholder="Ex: Parafuso M8"
              disabled={loading}
            />
            {errors.name && <span className="form-error">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="measure_unity" className="form-label">
              Unidade de Medida <span className="required">*</span>
            </label>
            <select
              id="measure_unity"
              name="measure_unity"
              value={formData.measure_unity}
              onChange={handleChange}
              className={`form-input ${errors.measure_unity ? 'form-input--error' : ''}`}
              disabled={loading}
            >
              <option value="">Selecione...</option>
              <option value="UN">Unidade (UN)</option>
              <option value="KG">Quilograma (KG)</option>
              <option value="LT">Litro (LT)</option>
              <option value="M">Metro (M)</option>
              <option value="M²">Metro Quadrado (M²)</option>
              <option value="M³">Metro Cúbico (M³)</option>
              <option value="CX">Caixa (CX)</option>
              <option value="PC">Peça (PC)</option>
            </select>
            {errors.measure_unity && <span className="form-error">{errors.measure_unity}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="amount" className="form-label">
              Quantidade <span className="required">*</span>
            </label>
            <input
              type="number"
              id="amount"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              className={`form-input ${errors.amount ? 'form-input--error' : ''}`}
              placeholder="0"
              step="0.01"
              min="0"
              disabled={loading}
            />
            {errors.amount && <span className="form-error">{errors.amount}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="price" className="form-label">
              Preço Unitário <span className="required">*</span>
            </label>
            <input
              type="number"
              id="price"
              name="price"
              value={formData.price}
              onChange={handleChange}
              className={`form-input ${errors.price ? 'form-input--error' : ''}`}
              placeholder="0.00"
              step="0.01"
              min="0"
              disabled={loading}
            />
            {errors.price && <span className="form-error">{errors.price}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="expiration_date" className="form-label">
              Data de Validade
            </label>
            <input
              type="date"
              id="expiration_date"
              name="expiration_date"
              value={formData.expiration_date}
              onChange={handleChange}
              className="form-input"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="description" className="form-label">
              SKU / Descrição
            </label>
            <input
              type="text"
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="form-input"
              placeholder="Ex: REF-MB-001"
              disabled={loading}
            />
          </div>
        </div>

        <div className="form-summary">
          <div className="summary-item">
            <span className="summary-label">Valor Total:</span>
            <span className="summary-value">
              {new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL',
              }).format(formData.amount * formData.price)}
            </span>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={handleClose}
            className="btn btn--secondary"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="btn btn--primary"
            disabled={loading}
          >
            {loading ? 'Salvando...' : (isEditMode ? 'Salvar Alterações' : 'Adicionar Item')}
          </button>
        </div>
      </form>
    </Modal>
  );
};

ItemFormModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  item: PropTypes.shape({
    id: PropTypes.number,
    name: PropTypes.string,
    measure_unity: PropTypes.string,
    amount: PropTypes.number,
    description: PropTypes.string,
    price: PropTypes.number,
    expiration_date: PropTypes.string,
  }),
  loading: PropTypes.bool,
};
