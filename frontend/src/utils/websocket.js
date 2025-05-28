import { io } from 'socket.io-client';
import { useToast } from 'vue-toastification';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.toast = useToast();
    this.notificationCallbacks = [];
    this.recentNotifications = new Set(); // Para evitar duplicatas
    this.notificationDebounceTime = 1000; // 1 segundo
  }

  connect(token = null) {
    try {
      // Evitar múltiplas conexões
      if (this.socket && this.socket.connected) {
        console.log('WebSocket já conectado, ignorando nova tentativa de conexão');
        return;
      }
      
      // Desconectar socket anterior se existir
      if (this.socket) {
        console.log('Desconectando socket anterior...');
        this.socket.disconnect();
        this.socket = null;
      }
      
      // Obter token automaticamente se não fornecido
      if (!token) {
        token = localStorage.getItem('access_token');
      }
      
      // URL do servidor WebSocket
      const serverUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000';
      
      console.log('=== DEBUG WEBSOCKET ===');
      console.log('URL do servidor:', serverUrl);
      console.log('Token presente:', token ? 'Sim' : 'Não');
      console.log('Token (primeiros 20 chars):', token ? token.substring(0, 20) + '...' : 'N/A');
      
      // Configurações de conexão
      const options = {
        transports: ['websocket', 'polling'],
        timeout: 20000,
        forceNew: true,
        auth: token ? { token } : {}
      };

      console.log('Opções de conexão:', options);
      console.log('Conectando ao WebSocket...', serverUrl);
      
      this.socket = io(serverUrl, options);

      // Event listeners
      this.socket.on('connect', () => {
        console.log('WebSocket conectado:', this.socket.id);
        this.isConnected = true;
        this.reconnectAttempts = 0;
        
        this.toast.success('Conectado ao sistema de notificações', {
          timeout: 3000,
          position: 'top-right'
        });
      });

      this.socket.on('disconnect', (reason) => {
        console.log('WebSocket desconectado:', reason);
        this.isConnected = false;
        
        if (reason === 'io server disconnect') {
          // Servidor desconectou - tentar reconectar
          this.reconnect();
        }
      });

      this.socket.on('connect_error', (error) => {
        console.error('Erro de conexão WebSocket:', error);
        this.isConnected = false;
        this.reconnect();
      });

      this.socket.on('connection_established', (data) => {
        console.log('Conexão estabelecida:', data);
      });

      // Listener para notificações
      this.socket.on('notification', (data) => {
        console.log('Notificação recebida:', data);
        this.handleNotification(data);
      });

    } catch (error) {
      console.error('Erro ao conectar WebSocket:', error);
    }
  }

  disconnect() {
    if (this.socket) {
      console.log('Desconectando WebSocket...');
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Tentativa de reconexão ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
      
      setTimeout(() => {
        if (!this.isConnected) {
          this.connect();
        }
      }, 2000 * this.reconnectAttempts); // Delay progressivo
    } else {
      console.error('Máximo de tentativas de reconexão atingido');
      this.toast.error('Falha na conexão com o sistema de notificações', {
        timeout: 5000,
        position: 'top-right'
      });
    }
  }

  handleNotification(data) {
    try {
      // Criar ID único para a notificação para evitar duplicatas
      const notificationId = `${data.type}_${data.data?.pedido?.id || 'unknown'}_${data.timestamp}`;
      
      // Verificar se já processamos esta notificação recentemente
      if (this.recentNotifications.has(notificationId)) {
        console.log('Notificação duplicada ignorada:', notificationId);
        return;
      }
      
      // Adicionar à lista de notificações recentes
      this.recentNotifications.add(notificationId);
      
      // Remover da lista após o tempo de debounce
      setTimeout(() => {
        this.recentNotifications.delete(notificationId);
      }, this.notificationDebounceTime);
      
      // Obter informações do usuário para filtrar notificações
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const userSetor = user.setor || 'Escritório';
      const userType = user.tipo_usuario || 'comum';
      
      // Verificar se a notificação é relevante para o usuário
      let shouldShowNotification = false;
      
      // Admins e gestores veem todas as notificações
      if (userType === 'admin' || userType === 'gestor') {
        shouldShowNotification = true;
      }
      // Usuários comuns só veem notificações do seu setor
      else if (data.data && data.data.pedido && data.data.pedido.setor === userSetor) {
        shouldShowNotification = true;
      }
      // Se a notificação tem campo setor, verificar se é do setor do usuário
      else if (data.setor && data.setor === userSetor) {
        shouldShowNotification = true;
      }
      
      if (!shouldShowNotification) {
        console.log('Notificação filtrada - não é do setor do usuário:', data);
        return;
      }
      
      console.log('Processando notificação:', notificationId, data);
      
      // Exibir toast baseado no tipo de notificação
      switch (data.type) {
        case 'novo_pedido':
          this.toast.info(data.data.message || data.message, {
            timeout: 8000,
            position: 'top-right',
            onClick: () => {
              // Abrir modal de impressão se possível
              if (data.data.pedido && data.data.pedido.id) {
                window.dispatchEvent(new CustomEvent('open-print-modal', {
                  detail: { pedidoId: data.data.pedido.id }
                }));
              }
            }
          });
          break;
        
        case 'pedido_atualizado':
          this.toast.warning(data.data.message || data.message, {
            timeout: 6000,
            position: 'top-right'
          });
          break;
        
        case 'pedido_concluido':
          this.toast.success(data.data.message || data.message, {
            timeout: 6000,
            position: 'top-right'
          });
          break;
        
        case 'teste':
          this.toast.info(`🔔 ${data.data.message || data.message}`, {
            timeout: 5000,
            position: 'top-right'
          });
          break;
        
        default:
          this.toast.info(data.data.message || data.message || 'Nova notificação', {
            timeout: 5000,
            position: 'top-right'
          });
      }

      // Chamar callbacks registrados
      this.notificationCallbacks.forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Erro ao executar callback de notificação:', error);
        }
      });

    } catch (error) {
      console.error('Erro ao processar notificação:', error);
    }
  }

  // Registrar callback para notificações
  onNotification(callback) {
    if (typeof callback === 'function') {
      this.notificationCallbacks.push(callback);
    }
  }

  // Remover callback
  offNotification(callback) {
    const index = this.notificationCallbacks.indexOf(callback);
    if (index > -1) {
      this.notificationCallbacks.splice(index, 1);
    }
  }

  // Enviar evento personalizado
  emit(event, data) {
    if (this.socket && this.isConnected) {
      this.socket.emit(event, data);
    } else {
      console.warn('WebSocket não conectado. Não é possível enviar evento:', event);
    }
  }

  // Verificar status da conexão
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      socketId: this.socket ? this.socket.id : null,
      reconnectAttempts: this.reconnectAttempts
    };
  }

  // Método para verificar se está conectado
  checkConnection() {
    return this.isConnected && this.socket && this.socket.connected;
  }

  // Método para testar notificações
  async sendNotification() {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.VUE_APP_API_URL}/test/websocket-notification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Teste de notificação enviado:', result);
        this.toast.success('Teste de notificação enviado com sucesso!');
      } else {
        console.error('Erro ao enviar teste de notificação:', response.status);
        this.toast.error('Erro ao enviar teste de notificação');
      }
    } catch (error) {
      console.error('Erro ao testar notificação:', error);
      this.toast.error('Erro ao testar notificação');
    }
  }
}

// Instância singleton
const websocketService = new WebSocketService();

export default websocketService; 