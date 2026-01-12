import { useState, useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Send, Image, Mic, Square, X, Trash2 } from 'lucide-react';
import { Button } from '../../../../components/Button';
import './ChatbotInput.css';

/**
 * Componente de input para envio de mensagens no chat
 */
export const ChatbotInput = ({ onSend, onSendImage, onSendAudio, disabled, placeholder = 'Digite sua mensagem...' }) => {
    const [message, setMessage] = useState('');
    const [imagePreview, setImagePreview] = useState(null);
    const [imageFile, setImageFile] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [recordingTime, setRecordingTime] = useState(0);
    const [savedRecordingTime, setSavedRecordingTime] = useState(0);
    const textareaRef = useRef(null);
    const fileInputRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const timerIntervalRef = useRef(null);
    const startTimeRef = useRef(null);
    const secondsRef = useRef(0); // ✅ REF para manter o valor do contador

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

    // Handler para seleção de imagem
    const handleImageSelect = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Validar tipo de arquivo
        if (!file.type.startsWith('image/')) {
            alert('Por favor, selecione apenas arquivos de imagem.');
            return;
        }

        // Validar tamanho (máx 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            alert('A imagem deve ter no máximo 5MB.');
            return;
        }

        setImageFile(file);

        // Limpa o texto quando imagem é selecionada
        setMessage('');

        // Criar preview
        const reader = new FileReader();
        reader.onloadend = () => {
            setImagePreview(reader.result);
        };
        reader.readAsDataURL(file);
    };

    // Handler para remover imagem selecionada
    const handleRemoveImage = () => {
        setImageFile(null);
        setImagePreview(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    // Handler para abrir seletor de arquivo
    const handleAttachClick = () => {
        fileInputRef.current?.click();
    };

    // Handler para envio da mensagem
    const handleSend = async () => {
        const trimmedMessage = message.trim();

        if (disabled) {
            return;
        }

        // Se tem áudio, envia como mensagem de áudio
        if (audioBlob && onSendAudio) {
            const reader = new FileReader();
            reader.onloadend = async () => {
                await onSendAudio('Áudio enviado', reader.result);
                handleRemoveAudio();
            };
            reader.readAsDataURL(audioBlob);
            return;
        }

        // Se tem imagem, envia como mensagem de imagem
        if (imageFile && onSendImage) {
            await onSendImage(trimmedMessage || 'Imagem enviada', imagePreview);
            setMessage('');
            handleRemoveImage();

            // Reset da altura do textarea
            if (textareaRef.current) {
                textareaRef.current.style.height = 'auto';
            }
            return;
        }

        // Senão, envia mensagem de texto normal
        if (!trimmedMessage) {
            return;
        }

        onSend(trimmedMessage);
        setMessage('');

        // Reset da altura do textarea
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    // Handler para iniciar gravação de áudio
    const handleStartRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            audioChunksRef.current = [];

            mediaRecorder.onstart = () => {
                startTimeRef.current = Date.now();
                secondsRef.current = 0;
                setRecordingTime(0);

                // Inicia o contador visual
                timerIntervalRef.current = setInterval(() => {
                    secondsRef.current++;
                    setRecordingTime(secondsRef.current);
                }, 1000);
            };

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });

                // Calcula tempo REAL usando Date.now()
                const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
                setSavedRecordingTime(elapsed);
                setAudioBlob(audioBlob);

                // Para o stream
                stream.getTracks().forEach(track => track.stop());

                // Para o timer
                if (timerIntervalRef.current) {
                    clearInterval(timerIntervalRef.current);
                    timerIntervalRef.current = null;
                }

                setIsRecording(false);
                setRecordingTime(0);
                secondsRef.current = 0;
            };

            mediaRecorder.onerror = (event) => {
                console.error('Erro no MediaRecorder:', event.error);
                alert('Erro ao gravar áudio: ' + event.error.message);

                // Limpa o timer em caso de erro
                if (timerIntervalRef.current) {
                    clearInterval(timerIntervalRef.current);
                    timerIntervalRef.current = null;
                }
            };

            // Limpa mensagem de texto e imagem quando inicia gravação
            setMessage('');
            handleRemoveImage();

            // Reseta o contador ANTES de iniciar
            secondsRef.current = 0;
            setRecordingTime(0);
            setIsRecording(true);

            // Inicia a gravação (o timer será iniciado no evento onstart)
            mediaRecorder.start(100);

        } catch (error) {
            console.error('Erro ao acessar microfone:', error);
            if (error.name === 'NotAllowedError') {
                alert('Permissão negada. Por favor, permita o acesso ao microfone nas configurações do navegador.');
            } else if (error.name === 'NotFoundError') {
                alert('Nenhum microfone encontrado. Verifique se há um microfone conectado.');
            } else {
                alert('Não foi possível acessar o microfone. Erro: ' + error.message);
            }
            setIsRecording(false);
        }
    };

    // Handler para parar gravação
    const handleStopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
        }
    };

    // Handler para remover áudio gravado
    const handleRemoveAudio = () => {
        setAudioBlob(null);
        setRecordingTime(0);
        setSavedRecordingTime(0);
        secondsRef.current = 0;
        startTimeRef.current = null;
        if (timerIntervalRef.current) {
            clearInterval(timerIntervalRef.current);
            timerIntervalRef.current = null;
        }
    };

    // Limpar ao desmontar componente
    useEffect(() => {
        return () => {
            if (timerIntervalRef.current) {
                clearInterval(timerIntervalRef.current);
            }
            if (mediaRecorderRef.current && isRecording) {
                mediaRecorderRef.current.stop();
            }
        };
    }, [isRecording]);

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
            {/* Preview da imagem */}
            {imagePreview && (
                <div className="chat-input__image-preview">
                    <img
                        src={imagePreview}
                        alt="Preview"
                        className="chat-input__preview-img"
                    />
                    <button
                        onClick={handleRemoveImage}
                        className="chat-input__remove-image"
                        aria-label="Remover imagem"
                        type="button"
                    >
                        <X size={16} />
                    </button>
                </div>
            )}

            {/* Preview/Status do áudio */}
            {(isRecording || audioBlob) && (
                <div className="chat-input__audio-preview">
                    {isRecording ? (
                        <>
                            <div className="chat-input__recording-indicator">
                                <span className="chat-input__recording-dot"></span>
                                <span className="chat-input__recording-text">Gravando...</span>
                            </div>
                            <span className="chat-input__recording-time">
                {Math.floor(recordingTime / 60)}:{(recordingTime % 60).toString().padStart(2, '0')}
              </span>
                        </>
                    ) : (
                        <>
                            <div className="chat-input__audio-ready">
                                <span className="chat-input__audio-icon">
                                    <Mic size={20} />
                                </span>
                                <span className="chat-input__audio-info">
                  <span className="chat-input__audio-label">Áudio gravado</span>
                  <span className="chat-input__audio-duration">{savedRecordingTime}s</span>
                </span>
                            </div>
                            <button
                                onClick={handleRemoveAudio}
                                className="chat-input__remove-audio"
                                aria-label="Remover áudio"
                                type="button"
                            >
                                <Trash2 size={18} />
                            </button>
                        </>
                    )}
                </div>
            )}

            <div className="chat-input__container">
                {/* Input de arquivo (hidden) */}
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="chat-input__file-input"
                    aria-label="Selecionar imagem"
                />

                {/* Botão de anexo de imagem */}
                <button
                    onClick={handleAttachClick}
                    disabled={disabled || isRecording || audioBlob !== null}
                    className="chat-input__attach-button"
                    aria-label="Anexar imagem"
                    title="Anexar imagem"
                    type="button"
                >
                    <Image size={20} />
                </button>

                {/* Botão de microfone */}
                {!isRecording && !audioBlob ? (
                    <button
                        onClick={handleStartRecording}
                        disabled={disabled || imagePreview !== null}
                        className="chat-input__mic-button"
                        aria-label="Gravar áudio"
                        title="Gravar áudio"
                        type="button"
                    >
                        <Mic size={20} />
                    </button>
                ) : isRecording ? (
                    <button
                        onClick={handleStopRecording}
                        className="chat-input__mic-button chat-input__mic-button--recording"
                        aria-label="Parar gravação"
                        title="Parar gravação"
                        type="button"
                    >
                        <Square size={20} />
                    </button>
                ) : null}

                <textarea
                    ref={textareaRef}
                    className="chat-input__textarea"
                    value={message}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder={
                        imagePreview ? 'Imagem selecionada (texto será ignorado)' :
                            isRecording ? 'Gravando áudio...' :
                                audioBlob ? 'Áudio pronto para enviar' :
                                    placeholder
                    }
                    disabled={disabled || imagePreview !== null || isRecording || audioBlob !== null}
                    rows={1}
                    aria-label="Campo de mensagem"
                />

                <Button
                    onClick={handleSend}
                    disabled={disabled || (!message.trim() && !imageFile && !audioBlob)}
                    variant="primary"
                    size="small"
                    className="chat-input__button"
                    aria-label="Enviar mensagem"
                    loading={disabled}
                >
                    <Send size={20} />
                </Button>
            </div>

            <div className="chat-input__hint">
                {isRecording ? 'Gravando... Clique no quadrado para parar' :
                    audioBlob ? 'Áudio pronto para enviar' :
                        'Pressione Enter para enviar, Shift+Enter para quebrar linha'}
            </div>
        </div>
    );
};

ChatbotInput.propTypes = {
    onSend: PropTypes.func.isRequired,
    onSendImage: PropTypes.func,
    onSendAudio: PropTypes.func,
    disabled: PropTypes.bool,
    placeholder: PropTypes.string,
};

ChatbotInput.defaultProps = {
    onSendImage: null,
    onSendAudio: null,
    disabled: false,
    placeholder: 'Digite sua mensagem...',
};