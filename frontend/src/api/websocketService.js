import { io } from 'socket.io-client';
import authService from './authService';
import { useToast } from 'vue-toastification';

// Definir a URL base da API (a mesma usada em authService.js)
const API_URL = process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000; // 3 segundos
    this.listeners = new Map();
    this.pendingNotifications = [];
    this.toast = useToast();
  }

  /**
   * Inicia a conexão WebSocket
   */
  connect() {
    if (this.socket) {
      console.log('WebSocket já está conectado ou tentando conectar.');
      return;
    }

    try {
      console.log('Iniciando conexão WebSocket...');
      
      // Obter o token JWT para autenticação
      const token = authService.getAuthToken();
      if (!token) {
        console.warn('Tentativa de conexão WebSocket sem token. Continuando sem WebSocket.');
        // Em desenvolvimento, continuamos mesmo sem o token
        return;
      }

      // Criar instância do Socket.IO
      this.socket = io(`${API_URL}/ws`, {
        transports: ['websocket', 'polling'],  // Adiciona polling como fallback
        auth: { token },
        reconnection: true,
        reconnectionAttempts: this.maxReconnectAttempts,
        reconnectionDelay: this.reconnectDelay,
        timeout: 20000,  // Aumenta o timeout para 20 segundos
        forceNew: true,  // Força uma nova conexão
        autoConnect: true,
        query: { token }  // Adiciona o token como parte da query também
      });
      
      // Notificar tentativa de conexão
      console.log('Socket.IO configurado. Tentando conectar...');

      // Configurar handlers para eventos do Socket.IO
      this.socket.on('connect', () => {
        console.log('WebSocket conectado com sucesso!');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.processQueuedNotifications();
      });

      this.socket.on('connect_error', (error) => {
        console.error('Erro de conexão WebSocket:', error);
        this.reconnectAttempts++;
        
        // Mostrar uma mensagem mais amigável
        if (this.reconnectAttempts === 1) {
          console.log('Tentando reconectar ao servidor...');
        }
        
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          console.error('Número máximo de tentativas de reconexão alcançado.');
          this.disconnect();
          // Continuar sem WebSocket em vez de mostrar erro
          console.log('Continuando sem WebSocket. Algumas atualizações em tempo real podem não estar disponíveis.');
        }
      });

      this.socket.on('disconnect', (reason) => {
        console.log(`WebSocket desconectado: ${reason}`);
        this.isConnected = false;
      });

      // Evento para notificações
      this.socket.on('notification', (data) => {
        this.handleNotification(data);
      });

      // Eventos para atualizações de pedidos
      this.socket.on('pedido_criado', (data) => {
        this.notifyEvent('pedido_criado', data);
        this.showToast('success', `Novo pedido criado: ${data.descricao}`, data);
      });

      this.socket.on('pedido_concluido', (data) => {
        this.notifyEvent('pedido_concluido', data);
        this.showToast('success', `Pedido #${data.id} concluído`, data);
      });

      this.socket.on('pedido_cancelado', (data) => {
        this.notifyEvent('pedido_cancelado', data);
        this.showToast('error', `Pedido #${data.id} cancelado`, data);
      });
    } catch (error) {
      console.error('Erro ao configurar WebSocket:', error);
      // Continuar sem WebSocket em caso de erro
      console.log('Continuando sem WebSocket devido a um erro de configuração.');
    }
  }

  /**
   * Encerra a conexão WebSocket
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      console.log('WebSocket desconectado manualmente.');
    }
  }

  /**
   * Registra um ouvinte para um evento específico
   * @param {string} event - Nome do evento
   * @param {Function} callback - Função de callback
   * @param {Object} context - Contexto para o callback (opcional)
   * @returns {string} ID do ouvinte (para remoção posterior)
   */
  addEventListener(event, callback, context = null) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }

    const id = this.generateId();
    this.listeners.get(event).push({
      id,
      callback,
      context
    });

    return id;
  }

  /**
   * Remove um ouvinte específico
   * @param {string} event - Nome do evento
   * @param {string} id - ID do ouvinte
   * @returns {boolean} Se a remoção foi bem-sucedida
   */
  removeEventListener(event, id) {
    if (!this.listeners.has(event)) {
      return false;
    }

    const eventListeners = this.listeners.get(event);
    const index = eventListeners.findIndex(listener => listener.id === id);
    
    if (index !== -1) {
      eventListeners.splice(index, 1);
      return true;
    }
    
    return false;
  }

  /**
   * Notifica os ouvintes registrados para um evento
   * @param {string} event - Nome do evento
   * @param {any} data - Dados do evento
   */
  notifyEvent(event, data) {
    if (!this.listeners.has(event)) {
      return;
    }

    const eventListeners = this.listeners.get(event);
    eventListeners.forEach(listener => {
      try {
        if (listener.context) {
          listener.callback.call(listener.context, data);
        } else {
          listener.callback(data);
        }
      } catch (error) {
        console.error(`Erro ao processar evento ${event}:`, error);
      }
    });
  }

  /**
   * Processa notificações que foram recebidas enquanto desconectado
   */
  processQueuedNotifications() {
    if (this.pendingNotifications.length > 0) {
      console.log(`Processando ${this.pendingNotifications.length} notificações em fila.`);
      
      this.pendingNotifications.forEach(notification => {
        this.handleNotification(notification);
      });
      
      this.pendingNotifications = [];
    }
  }

  /**
   * Processa uma notificação recebida
   * @param {Object} notification - Objeto de notificação
   */
  handleNotification(notification) {
    if (!this.isConnected) {
      // Se não estiver conectado, coloca a notificação na fila
      this.pendingNotifications.push(notification);
      return;
    }

    const { type, data } = notification;
    
    // Notificar os ouvintes registrados
    this.notifyEvent(type, data);
    
    // Mostrar toast com a notificação
    this.showNotificationToast(type, data);
  }

  /**
   * Exibe um toast com a notificação
   * @param {string} type - Tipo da notificação
   * @param {Object} data - Dados da notificação
   */
  showNotificationToast(type, data) {
    let title = '';
    let message = '';
    let toastType = 'info';

    switch (type) {
      case 'pedido_criado':
        title = 'Novo Pedido';
        message = `${data.usuario_nome} criou um novo pedido: ${data.descricao}`;
        toastType = 'info';
        break;
      case 'pedido_concluido':
        title = 'Pedido Concluído';
        message = `Pedido #${data.id} foi concluído por ${data.usuario_conclusao}`;
        toastType = 'success';
        break;
      case 'pedido_cancelado':
        title = 'Pedido Cancelado';
        message = `Pedido #${data.id} foi cancelado por ${data.usuario_cancelamento}`;
        toastType = 'error';
        break;
      default:
        title = 'Notificação';
        message = JSON.stringify(data);
        break;
    }

    this.showToast(toastType, `${title}: ${message}`, data);
  }

  /**
   * Exibe um toast personalizado
   * @param {string} type - Tipo do toast (success, error, info, warning)
   * @param {string} message - Mensagem a ser exibida
   * @param {Object} data - Dados adicionais para o toast
   */
  showToast(type, message, data = {}) {
    try {
      this.toast[type](message, {
        toastClassName: `custom-toast-${type}`,
        bodyClassName: "custom-toast-body",
        closeButtonClassName: "custom-toast-close",
        onClick: () => {
          // Ação ao clicar no toast (opcional)
          if (type === 'pedido_criado' || type === 'pedido_concluido' || type === 'pedido_cancelado') {
            // Pode redirecionar para detalhes do pedido, por exemplo
            console.log('Toast clicado:', data);
          }
        }
      });
    } catch (error) {
      console.error('Erro ao exibir toast:', error);
    }
  }

  /**
   * Gera um ID único para ouvintes
   * @returns {string} ID único
   */
  generateId() {
    return `listener_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Singleton para garantir uma única instância do serviço WebSocket
const websocketService = new WebSocketService();

export default websocketService; 