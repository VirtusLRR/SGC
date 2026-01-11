import PropTypes from 'prop-types';
import { Modal } from '../../../components/Modal';
import './ConfirmDeleteModal.css';

/**
 * Modal de confirmação de exclusão de receita
 */
export const ConfirmDeleteModal = ({ 
  isOpen, 
  onClose, 
  onConfirm, 
  recipeName,
  loading = false 
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Confirmar Exclusão"
      size="small"
    >
      <div className="confirm-delete">
        <div className="confirm-delete__icon">
          ⚠️
        </div>
        <p className="confirm-delete__message">
          Tem certeza que deseja excluir a receita <strong>{recipeName}</strong>?
        </p>
        <p className="confirm-delete__warning">
          Esta ação não pode ser desfeita.
        </p>
        
        <div className="confirm-delete__actions">
          <button
            type="button"
            onClick={onClose}
            className="btn btn--secondary"
            disabled={loading}
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="btn btn--danger"
            disabled={loading}
          >
            {loading ? 'Excluindo...' : 'Sim, Excluir'}
          </button>
        </div>
      </div>
    </Modal>
  );
};

ConfirmDeleteModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onConfirm: PropTypes.func.isRequired,
  recipeName: PropTypes.string.isRequired,
  loading: PropTypes.bool,
};
