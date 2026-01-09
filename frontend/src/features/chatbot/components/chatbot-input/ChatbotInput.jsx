import { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Button } from '../../../../components/Button';
import './ChatbotInput.css';

/**
 * Componente de input para envio de mensagens no chat
 */
export const ChatbotInput = ({ onSend, disabled, placeholder = 'Digite sua mensagem...' }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize do textarea baseado no conteúdo
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  // Handler para mudanças no input
  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  // Handler para envio da mensagem
  const handleSend = () => {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || disabled) {
      return;
    }

    onSend(trimmedMessage);
    setMessage('');

    // Reset da altura do textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  // Handler para teclas pressionadas
  const handleKeyDown = (e) => {
    // Enter sem Shift envia a mensagem
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
    // Shift + Enter adiciona quebra de linha (comportamento padrão do textarea)
  };

  return (
    <div className="chat-input">
      <div className="chat-input__container">
        <textarea
          ref={textareaRef}
          className="chat-input__textarea"
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          aria-label="Campo de mensagem"
        />

        <Button
          onClick={handleSend}
          disabled={disabled || !message.trim()}
          variant="primary"
          size="small"
          className="chat-input__button"
          aria-label="Enviar mensagem"
          loading={disabled}
        >
          {disabled ? '⏳' : '➤'}
        </Button>
      </div>

      <div className="chat-input__hint">
        Pressione Enter para enviar, Shift+Enter para quebrar linha
      </div>
    </div>
  );
};

ChatbotInput.propTypes = {
  onSend: PropTypes.func.isRequired,
  disabled: PropTypes.bool,
  placeholder: PropTypes.string,
};

ChatbotInput.defaultProps = {
  disabled: false,
  placeholder: 'Digite sua mensagem...',
};

