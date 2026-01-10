import { useState, useEffect, useCallback } from 'react';
import { chatbotApi } from '../api/chatbotApi';

/**
 * Custom Hook para gerenciar operações do chatbot
 * @param {Function} onResponseReceived - Callback executado após receber resposta da API
 */
export const useChatbot = (onResponseReceived) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [threadId, setThreadId] = useState(null);

  // Inicializa o thread_id do localStorage quando o componente montar
  useEffect(() => {
    const savedThreadId = localStorage.getItem('chatbot_thread_id');
    if (savedThreadId) {
      setThreadId(savedThreadId);
    }
  }, []);

  /**
   * Gera um novo UUID para thread_id
   */
  const generateThreadId = useCallback(() => {
    const newThreadId = crypto.randomUUID();
    setThreadId(newThreadId);
    localStorage.setItem('chatbot_thread_id', newThreadId);
    return newThreadId;
  }, []);

  /**
   * Envia uma mensagem para o chatbot
   * @param {string} userMessage - Mensagem do usuário
   */
  const sendMessage = async (userMessage) => {
    if (!userMessage.trim()) {
      setError('Mensagem não pode estar vazia');
      return;
    }

    setLoading(true);
    setError(null);

    // Se não tem thread_id, gera um novo
    const currentThreadId = threadId || generateThreadId();

    // Adiciona a mensagem do usuário imediatamente na UI
    const tempUserMessage = {
      id: Date.now(),
      user_message: userMessage,
      ai_message: null,
      create_at: new Date().toISOString(),
      isUser: true,
      isTemp: true
    };

    setMessages(prev => [...prev, tempUserMessage]);

    try {
      const data = await chatbotApi.sendMessage({
        user_message: userMessage,
        thread_id: currentThreadId
      });

      // Remove a mensagem temporária e adiciona a resposta real do backend
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.isTemp);
        return [
          ...filtered,
          {
            id: data.id,
            user_message: data.user_message,
            ai_message: null,
            create_at: data.create_at,
            isUser: true
          },
          {
            id: data.id + '_ai',
            user_message: null,
            ai_message: data.ai_message,
            create_at: data.create_at,
            isUser: false
          }
        ];
      });

      return data;
    } catch (err) {
      // Remove a mensagem temporária em caso de erro
      setMessages(prev => prev.filter(msg => !msg.isTemp));
      setError(err.response?.data?.detail || 'Erro ao enviar mensagem');
      throw err;
    } finally {
      setLoading(false);
      // Executa callback após resposta da API
      if (onResponseReceived && typeof onResponseReceived === 'function') {
        onResponseReceived();
      }
    }
  };

  /**
   * Envia uma mensagem com imagem para o chatbot
   * @param {string} userMessage - Mensagem do usuário
   * @param {string} imageBase64 - Imagem em base64 (data URL)
   */
  const sendImageMessage = async (userMessage, imageBase64) => {
    if (!imageBase64) {
      setError('Imagem não pode estar vazia');
      return;
    }

    setLoading(true);
    setError(null);

    // Se não tem thread_id, gera um novo
    const currentThreadId = threadId || generateThreadId();

    // Extrai apenas o base64 puro (remove 'data:image/png;base64,' prefix)
    const base64Pure = imageBase64.includes(',')
      ? imageBase64.split(',')[1]
      : imageBase64;

    // Adiciona a mensagem do usuário imediatamente na UI
    const tempUserMessage = {
      id: Date.now(),
      user_message: null, // Não mostra texto quando envia imagem
      ai_message: null,
      image_base64: imageBase64, // Mantém o data URL completo para exibição
      create_at: new Date().toISOString(),
      isUser: true,
      isTemp: true
    };

    setMessages(prev => [...prev, tempUserMessage]);

    try {
      const data = await chatbotApi.sendImageMessage({
        user_message: userMessage || '',
        thread_id: currentThreadId,
        image_b64: base64Pure // Envia apenas base64 puro
      });

      // Remove a mensagem temporária e adiciona a resposta real do backend
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.isTemp);
        return [
          ...filtered,
          {
            id: data.id,
            user_message: null, // Não mostra texto, apenas imagem
            ai_message: null,
            image_base64: imageBase64,
            create_at: data.create_at,
            isUser: true
          },
          {
            id: data.id + '_ai',
            user_message: null,
            ai_message: data.ai_message,
            create_at: data.create_at,
            isUser: false
          }
        ];
      });

      return data;
    } catch (err) {
      // Remove a mensagem temporária em caso de erro
      setMessages(prev => prev.filter(msg => !msg.isTemp));
      setError(err.response?.data?.detail || 'Erro ao enviar imagem');
      throw err;
    } finally {
      setLoading(false);
      // Executa callback após resposta da API
      if (onResponseReceived && typeof onResponseReceived === 'function') {
        onResponseReceived();
      }
    }
  };

  /**
   * Envia uma mensagem com áudio para o chatbot
   * @param {string} userMessage - Mensagem do usuário (não será exibida)
   * @param {string} audioBase64 - Áudio em base64 (data URL)
   */
  const sendAudioMessage = async (userMessage, audioBase64) => {
    if (!audioBase64) {
      setError('Áudio não pode estar vazio');
      return;
    }

    setLoading(true);
    setError(null);

    // Se não tem thread_id, gera um novo
    const currentThreadId = threadId || generateThreadId();

    // Extrai apenas o base64 puro (remove 'data:audio/...;base64,' prefix)
    const base64Pure = audioBase64.includes(',')
      ? audioBase64.split(',')[1]
      : audioBase64;


    // Adiciona a mensagem do usuário imediatamente na UI (SÓ ÍCONE, SEM TEXTO)
    const tempUserMessage = {
      id: Date.now(),
      user_message: null, // Não mostra texto
      ai_message: null,
      audio_base64: audioBase64, // Mantém o data URL completo para exibição
      create_at: new Date().toISOString(),
      isUser: true,
      isTemp: true
    };

    setMessages(prev => [...prev, tempUserMessage]);

    try {
      const data = await chatbotApi.sendAudioMessage({
        user_message: userMessage || '',
        thread_id: currentThreadId,
        audio_b64: base64Pure // Envia apenas base64 puro
      });

      // Remove a mensagem temporária e adiciona a resposta real do backend
      setMessages(prev => {
        const filtered = prev.filter(msg => !msg.isTemp);
        return [
          ...filtered,
          {
            id: data.id,
            user_message: null, // Não mostra texto, apenas áudio
            ai_message: null,
            audio_base64: audioBase64, // Mantém o áudio da UI local
            create_at: data.create_at,
            isUser: true
          },
          {
            id: data.id + '_ai',
            user_message: null,
            ai_message: data.ai_message,
            create_at: data.create_at,
            isUser: false
          }
        ];
      });

      return data;
    } catch (err) {
      // Remove a mensagem temporária em caso de erro
      setMessages(prev => prev.filter(msg => !msg.isTemp));
      setError(err.response?.data?.detail || 'Erro ao enviar áudio');
      throw err;
    } finally {
      setLoading(false);
      // Executa callback após resposta da API
      if (onResponseReceived && typeof onResponseReceived === 'function') {
        onResponseReceived();
      }
    }
  };

  /**
   * Busca o histórico de conversas
   */
  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await chatbotApi.getChatHistory();

      // Converte o histórico para o formato de mensagens
      const formattedMessages = [];
      data.forEach(item => {
        // Adiciona mensagem do usuário
        formattedMessages.push({
          id: item.id,
          user_message: item.user_message,
          ai_message: null,
          create_at: item.create_at,
          isUser: true
        });
        // Adiciona resposta do bot
        formattedMessages.push({
          id: item.id + '_ai',
          user_message: null,
          ai_message: item.ai_message,
          create_at: item.create_at,
          isUser: false
        });
      });

      setMessages(formattedMessages);
      return data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar histórico');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Limpa a conversa atual e inicia uma nova
   */
  const clearChat = useCallback(() => {
    setMessages([]);
    generateThreadId();
    setError(null);
  }, [generateThreadId]);

  /**
   * Limpa apenas as mensagens (mantém o thread_id)
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    loading,
    error,
    threadId,
    sendMessage,
    sendImageMessage,
    sendAudioMessage,
    fetchHistory,
    clearChat,
    clearMessages,
  };
};

