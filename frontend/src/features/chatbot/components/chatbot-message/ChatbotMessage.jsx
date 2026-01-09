import PropTypes from 'prop-types';
import './ChatbotMessage.css';

/**
 * Componente para exibir uma mensagem individual do chat
 */
export const ChatbotMessage = ({ message, timestamp, isUser }) => {
    // Formata o timestamp para exibição
    const formatTimestamp = (date) => {
        if (!date) return '';

        const messageDate = new Date(date);
        const now = new Date();
        const isToday = messageDate.toDateString() === now.toDateString();

        const timeFormat = new Intl.DateTimeFormat('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        if (isToday) {
            return timeFormat.format(messageDate);
        }

        // Se não for hoje, mostra data + hora
        const dateTimeFormat = new Intl.DateTimeFormat('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });

        return dateTimeFormat.format(messageDate);
    };

    // Determina qual texto exibir (mensagem do usuário ou do bot)
    const messageText = isUser ? message.user_message : message.ai_message;

    return (
        <div className={`chat-message ${isUser ? 'chat-message--user' : 'chat-message--bot'}`}>
            {/* Avatar */}
            <div className="chat-message__avatar">
                {isUser ? (
                    <div className="chat-message__avatar-icon chat-message__avatar-icon--user">
                        👤
                    </div>
                ) : (
                    <div className="chat-message__avatar-icon chat-message__avatar-icon--bot">
                        🤖
                    </div>
                )}
            </div>

            {/* Conteúdo da mensagem */}
            <div className="chat-message__content">
                <div className="chat-message__bubble">
                    <p className="chat-message__text">{messageText}</p>
                </div>
                {timestamp && (
                    <span className="chat-message__timestamp">
            {formatTimestamp(timestamp)}
          </span>
                )}
            </div>
        </div>
    );
};

ChatbotMessage.propTypes = {
    message: PropTypes.shape({
        user_message: PropTypes.string,
        ai_message: PropTypes.string,
    }).isRequired,
    timestamp: PropTypes.string,
    isUser: PropTypes.bool.isRequired,
};

ChatbotMessage.defaultProps = {
    timestamp: null,
};

