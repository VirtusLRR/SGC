import { useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { MessageCircle, X, History, Trash2, Hand, AlertTriangle, Bot } from 'lucide-react';
import { useChatbot } from '../../hooks/useChatbot';
import { ChatbotMessage } from '../chatbot-message/ChatbotMessage';
import { ChatbotInput } from '../chatbot-input/ChatbotInput';
import { ChatbotHistoryModal } from '../chatbot-history-modal/ChatbotHistoryModal';
import './ChatbotWidget.css';

/**
 * Widget principal do chatbot - Componente flutuante de canto de página
 * @param {Function} onResponseReceived - Callback executado após receber resposta da API do chatbot
 */
export const ChatbotWidget = ({ onResponseReceived }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  const {
    messages,
    loading,
    error,
    sendMessage,
    sendImageMessage,
    sendAudioMessage,
    clearChat,
    fetchHistory,
  } = useChatbot(onResponseReceived);

  // Auto-scroll para a última mensagem
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll quando novas mensagens chegarem
  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  // Handler para alternar visibilidade
  const toggleChat = () => {
    setIsOpen(prev => !prev);
  };

  // Handler para enviar mensagem
  const handleSendMessage = async (message) => {
    try {
      await sendMessage(message);
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err);
    }
  };

  // Handler para enviar imagem
  const handleSendImage = async (message, imageBase64) => {
    try {
      await sendImageMessage(message, imageBase64);
    } catch (err) {
      console.error('Erro ao enviar imagem:', err);
    }
  };

  // Handler para enviar áudio
  const handleSendAudio = async (message, audioBase64) => {
    try {
      await sendAudioMessage(message, audioBase64);
    } catch (err) {
      console.error('Erro ao enviar áudio:', err);
    }
  };

  // Handler para limpar chat
  const handleClearChat = () => {
    if (window.confirm('Deseja limpar toda a conversa e iniciar uma nova?')) {
      clearChat();
    }
  };

  // Handler para abrir histórico
  const handleOpenHistory = () => {
    setIsHistoryOpen(true);
  };

  // Handler para fechar histórico
  const handleCloseHistory = () => {
    setIsHistoryOpen(false);
  };

  // Handler para carregar histórico
  const handleLoadHistory = async () => {
    return await fetchHistory();
  };

  // Previne scroll do body quando chat está aberto (mobile)
  useEffect(() => {
    if (isOpen && window.innerWidth <= 768) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    <div className="chatbot-widget">
      {/* Botão flutuante para abrir/fechar */}
      <button
        className={`chatbot-widget__toggle ${isOpen ? 'chatbot-widget__toggle--active' : ''}`}
        onClick={toggleChat}
        aria-label={isOpen ? 'Fechar chat' : 'Abrir chat'}
      >
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>

      {/* Janela do chat */}
      {isOpen && (
        <div className="chatbot-widget__window">
          {/* Header */}
          <div className="chatbot-widget__header">
            <div className="chatbot-widget__header-info">
              <div className="chatbot-widget__avatar">
                <Bot size={24} />
              </div>
              <div className="chatbot-widget__header-text">
                <h3 className="chatbot-widget__title">Assistente de Estoque</h3>
                <span className="chatbot-widget__status">Online</span>
              </div>
            </div>

            <div className="chatbot-widget__header-actions">
              <button
                className="chatbot-widget__action-button"
                onClick={handleOpenHistory}
                aria-label="Ver histórico"
                title="Ver histórico"
              >
                <History size={18} />
              </button>
              <button
                className="chatbot-widget__action-button"
                onClick={handleClearChat}
                aria-label="Limpar conversa"
                title="Nova conversa"
              >
                <Trash2 size={18} />
              </button>
              <button
                className="chatbot-widget__action-button chatbot-widget__action-button--close"
                onClick={toggleChat}
                aria-label="Fechar chat"
                title="Fechar"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Messages Container */}
          <div
            className="chatbot-widget__messages"
            ref={messagesContainerRef}
          >
            {messages.length === 0 ? (
              <div className="chatbot-widget__welcome">
                <div className="chatbot-widget__welcome-icon">
                  <Hand size={48} />
                </div>
                <h4 className="chatbot-widget__welcome-title">
                  Olá! Como posso ajudar?
                </h4>
                <p className="chatbot-widget__welcome-text">
                  Envie uma mensagem para começar a conversa.
                </p>
              </div>
            ) : (
              messages.map((msg) => (
                <ChatbotMessage
                  key={msg.id}
                  message={msg}
                  timestamp={msg.create_at}
                  isUser={msg.isUser}
                />
              ))
            )}

            {/* Elemento para scroll automático */}
            <div ref={messagesEndRef} />
          </div>

          {/* Error Message */}
          {error && (
            <div className="chatbot-widget__error">
              <span className="chatbot-widget__error-icon">
                <AlertTriangle size={20} />
              </span>
              <span className="chatbot-widget__error-text">{error}</span>
            </div>
          )}

          {/* Input Area */}
          <ChatbotInput
            onSend={handleSendMessage}
            onSendImage={handleSendImage}
            onSendAudio={handleSendAudio}
            disabled={loading}
            placeholder="Digite sua mensagem..."
          />
        </div>
      )}

      {/* History Modal */}
      <ChatbotHistoryModal
        isOpen={isHistoryOpen}
        onClose={handleCloseHistory}
        onLoadHistory={handleLoadHistory}
      />
    </div>
  );
};

ChatbotWidget.propTypes = {
  onResponseReceived: PropTypes.func,
};

ChatbotWidget.defaultProps = {
  onResponseReceived: null,
};

