import PropTypes from 'prop-types';
import { User, Bot, AudioLines } from 'lucide-react';
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

    /**
     * Formata o texto com suporte a blocos de código e markdown básico
     */
    const formatMessageText = (text) => {
        if (!text) return null;

        const parts = [];
        let currentIndex = 0;

        // Regex para encontrar blocos de código com ``` ou ```yaml/json/etc
        const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
        let match;

        while ((match = codeBlockRegex.exec(text)) !== null) {
            // Adiciona texto antes do bloco de código
            if (match.index > currentIndex) {
                const beforeText = text.substring(currentIndex, match.index);
                parts.push(
                    <span key={`text-${currentIndex}`}>
                        {formatInlineMarkdown(beforeText)}
                    </span>
                );
            }

            // Adiciona o bloco de código
            const language = match[1] || '';
            const code = match[2];
            parts.push(
                <div key={`code-${match.index}`} className="chat-message__code-block">
                    {language && (
                        <div className="chat-message__code-language">{language}</div>
                    )}
                    <pre className="chat-message__code">
                        <code>{code}</code>
                    </pre>
                </div>
            );

            currentIndex = match.index + match[0].length;
        }

        // Adiciona o texto restante
        if (currentIndex < text.length) {
            const remainingText = text.substring(currentIndex);
            parts.push(
                <span key={`text-${currentIndex}`}>
                    {formatInlineMarkdown(remainingText)}
                </span>
            );
        }

        return parts.length > 0 ? parts : formatInlineMarkdown(text);
    };

    /**
     * Formata markdown inline (negrito, itálico, listas)
     */
    const formatInlineMarkdown = (text) => {
        if (!text) return null;

        // Separa por linhas para processar listas
        const lines = text.split('\n');
        const elements = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // Lista com asterisco ou travessão
            if (line.trim().match(/^[\*\-]\s+/)) {
                elements.push(
                    <div key={`line-${i}`} className="chat-message__list-item">
                        • {formatTextStyle(line.replace(/^[\*\-]\s+/, ''))}
                    </div>
                );
            }
            // Lista numerada
            else if (line.trim().match(/^\d+\.\s+/)) {
                elements.push(
                    <div key={`line-${i}`} className="chat-message__list-item">
                        {formatTextStyle(line)}
                    </div>
                );
            }
            // Linha normal
            else if (line.trim()) {
                elements.push(
                    <span key={`line-${i}`}>
                        {formatTextStyle(line)}
                        {i < lines.length - 1 && <br />}
                    </span>
                );
            }
            // Linha vazia
            else if (i < lines.length - 1) {
                elements.push(<br key={`br-${i}`} />);
            }
        }

        return elements;
    };

    /**
     * Formata negrito (**text**) e itálico (*text*)
     */
    const formatTextStyle = (text) => {
        // Negrito **texto**
        text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        // Itálico *texto*
        text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');

        return <span dangerouslySetInnerHTML={{ __html: text }} />;
    };

    // Determina qual texto exibir (mensagem do usuário ou do bot)
    const messageText = isUser ? message.user_message : message.ai_message;
    const imageData = message.image_base64;
    const audioData = message.audio_base64;

    return (
        <div className={`chat-message ${isUser ? 'chat-message--user' : 'chat-message--bot'}`}>
            {/* Avatar */}
            <div className="chat-message__avatar">
                {isUser ? (
                    <div className="chat-message__avatar-icon chat-message__avatar-icon--user">
                        <User size={20} />
                    </div>
                ) : (
                    <div className="chat-message__avatar-icon chat-message__avatar-icon--bot">
                        <Bot size={20} />
                    </div>
                )}
            </div>

            {/* Conteúdo da mensagem */}
            <div className="chat-message__content">
                <div className="chat-message__bubble">
                    {/* Imagem (se existir) */}
                    {imageData && (
                        <div className="chat-message__image-container">
                            <img
                                src={imageData}
                                alt="Imagem enviada"
                                className="chat-message__image"
                            />
                        </div>
                    )}
                    {/* Áudio (se existir) */}
                    {audioData && (
                        <div className="chat-message__audio-container">
                            <div className="chat-message__audio-wrapper">
                                <span className="chat-message__audio-icon">
                                    <AudioLines size={20} />
                                </span>
                                <audio
                                    controls
                                    className="chat-message__audio"
                                    preload="metadata"
                                >
                                    <source src={audioData} type="audio/webm" />
                                    <source src={audioData} type="audio/mpeg" />
                                    Seu navegador não suporta o elemento de áudio.
                                </audio>
                            </div>
                        </div>
                    )}
                    {/* Texto da mensagem */}
                    {messageText && (
                        <div className="chat-message__text">
                            {formatMessageText(messageText)}
                        </div>
                    )}
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
        image_base64: PropTypes.string,
        audio_base64: PropTypes.string,
    }).isRequired,
    timestamp: PropTypes.string,
    isUser: PropTypes.bool.isRequired,
};

ChatbotMessage.defaultProps = {
    timestamp: null,
};

