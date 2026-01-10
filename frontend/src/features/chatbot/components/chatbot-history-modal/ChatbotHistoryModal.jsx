import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ChatbotHistoryModal.css';

/**
 * Modal para exibir o histórico completo de conversas do chatbot
 */
export const ChatbotHistoryModal = ({ isOpen, onClose, onLoadHistory }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [groupedHistory, setGroupedHistory] = useState({});

  // Busca o histórico quando o modal abre
  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  // Agrupa histórico por thread_id
  useEffect(() => {
    if (history.length > 0) {
      const grouped = history.reduce((acc, item) => {
        const thread = item.thread_id || 'sem-thread';
        if (!acc[thread]) {
          acc[thread] = [];
        }
        acc[thread].push(item);
        return acc;
      }, {});
      setGroupedHistory(grouped);
    }
  }, [history]);

  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await onLoadHistory();
      setHistory(data);
    } catch (err) {
      setError('Erro ao carregar histórico');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  // Filtra histórico baseado no termo de busca
  const filteredGroupedHistory = Object.entries(groupedHistory).reduce((acc, [threadId, items]) => {
    const filtered = items.filter(item =>
      item.user_message?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.ai_message?.toLowerCase().includes(searchTerm.toLowerCase())
    );
    if (filtered.length > 0) {
      acc[threadId] = filtered;
    }
    return acc;
  }, {});

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getConversationTitle = (threadId, items) => {
    const firstMessage = items[0]?.user_message || 'Conversa';
    return firstMessage.length > 40 ? firstMessage.substring(0, 40) + '...' : firstMessage;
  };

  if (!isOpen) return null;

  return (
    <div className="chatbot-history-modal-overlay" onClick={onClose}>
      <div
        className="chatbot-history-modal"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="chatbot-history-modal__header">
          <h2 className="chatbot-history-modal__title">
            📜 Histórico de Conversas
          </h2>
          <button
            className="chatbot-history-modal__close"
            onClick={onClose}
            aria-label="Fechar histórico"
          >
            ✕
          </button>
        </div>

        {/* Search Bar */}
        <div className="chatbot-history-modal__search">
          <input
            type="text"
            className="chatbot-history-modal__search-input"
            placeholder="🔍 Buscar nas conversas..."
            value={searchTerm}
            onChange={handleSearchChange}
          />
        </div>

        {/* Content */}
        <div className="chatbot-history-modal__content">
          {loading && (
            <div className="chatbot-history-modal__loading">
              <div className="chatbot-history-modal__spinner"></div>
              <p>Carregando histórico...</p>
            </div>
          )}

          {error && (
            <div className="chatbot-history-modal__error">
              <span className="chatbot-history-modal__error-icon">⚠️</span>
              <p>{error}</p>
              <button
                className="chatbot-history-modal__retry"
                onClick={loadHistory}
              >
                Tentar novamente
              </button>
            </div>
          )}

          {!loading && !error && history.length === 0 && (
            <div className="chatbot-history-modal__empty">
              <div className="chatbot-history-modal__empty-icon">💬</div>
              <p className="chatbot-history-modal__empty-text">
                Nenhuma conversa encontrada
              </p>
            </div>
          )}

          {!loading && !error && Object.keys(filteredGroupedHistory).length > 0 && (
            <div className="chatbot-history-modal__conversations">
              {Object.entries(filteredGroupedHistory).map(([threadId, items]) => (
                <div
                  key={threadId}
                  className="chatbot-history-modal__conversation"
                >
                  <div className="chatbot-history-modal__conversation-header">
                    <h3 className="chatbot-history-modal__conversation-title">
                      {getConversationTitle(threadId, items)}
                    </h3>
                    <span className="chatbot-history-modal__conversation-count">
                      {items.length} {items.length === 1 ? 'mensagem' : 'mensagens'}
                    </span>
                  </div>

                  <div className="chatbot-history-modal__messages">
                    {items.map((item, index) => (
                      <div
                        key={`${item.id}-${index}`}
                        className="chatbot-history-modal__message-pair"
                      >
                        {/* User Message */}
                        <div className="chatbot-history-modal__message chatbot-history-modal__message--user">
                          <div className="chatbot-history-modal__message-header">
                            <span className="chatbot-history-modal__message-sender">
                              👤 Você
                            </span>
                            <span className="chatbot-history-modal__message-time">
                              {formatDate(item.create_at)}
                            </span>
                          </div>
                          <div className="chatbot-history-modal__message-text">
                            {item.user_message}
                          </div>
                        </div>

                        {/* AI Message */}
                        <div className="chatbot-history-modal__message chatbot-history-modal__message--ai">
                          <div className="chatbot-history-modal__message-header">
                            <span className="chatbot-history-modal__message-sender">
                              🤖 Assistente
                            </span>
                          </div>
                          <div className="chatbot-history-modal__message-text">
                            {item.ai_message}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && !error && searchTerm && Object.keys(filteredGroupedHistory).length === 0 && (
            <div className="chatbot-history-modal__empty">
              <div className="chatbot-history-modal__empty-icon">🔍</div>
              <p className="chatbot-history-modal__empty-text">
                Nenhuma conversa encontrada para "{searchTerm}"
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="chatbot-history-modal__footer">
          <button
            className="chatbot-history-modal__button chatbot-history-modal__button--secondary"
            onClick={onClose}
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};

ChatbotHistoryModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onLoadHistory: PropTypes.func.isRequired,
};

