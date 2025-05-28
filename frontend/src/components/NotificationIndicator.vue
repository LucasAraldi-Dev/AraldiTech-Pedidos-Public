<template>
  <div class="notification-indicator" v-if="showIndicator">
    <div class="notification-icon" @click="toggleNotifications" :class="{ 'has-notifications': unreadCount > 0 }">
      <i class="material-icons">notifications</i>
      <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
    </div>
    
    <!-- Modal de notificações seguindo padrão do sistema -->
    <div v-if="showDropdown" class="modal-overlay" @click.self="closeNotifications">
      <div class="order-form" @click.stop>
        <!-- Header padrão do sistema -->
        <div class="form-header">
          <h2>CENTRAL DE NOTIFICAÇÕES</h2>
          <div class="notification-summary">
            <span class="notification-count">{{ notifications.length }} notificação{{ notifications.length !== 1 ? 's' : '' }}</span>
            <span v-if="unreadCount > 0" class="unread-count">{{ unreadCount }} não lida{{ unreadCount !== 1 ? 's' : '' }}</span>
          </div>
        </div>

        <!-- Ações do header -->
        <div class="notification-actions-header">
          <div class="action-buttons">
            <button v-if="notifications.length > 0" @click="markAllAsRead" class="action-btn secondary" :disabled="unreadCount === 0">
              <i class="material-icons">done_all</i>
              <span class="btn-text">Marcar todas como lidas</span>
            </button>
            <button @click="clearAllNotifications" class="action-btn danger" v-if="notifications.length > 0">
              <i class="material-icons">clear_all</i>
              <span class="btn-text">Limpar todas</span>
            </button>
          </div>
        </div>
        
        <!-- Filtros rápidos -->
        <div v-if="notifications.length > 0" class="notification-filters">
          <div class="filter-tabs">
            <button 
              class="filter-tab" 
              :class="{ active: activeFilter === 'all' }"
              @click="setActiveFilter('all')"
            >
              <i class="material-icons">inbox</i>
              <span>Todas</span>
              <span class="tab-badge">{{ notifications.length }}</span>
            </button>
            <button 
              class="filter-tab" 
              :class="{ active: activeFilter === 'unread' }"
              @click="setActiveFilter('unread')"
            >
              <i class="material-icons">mark_email_unread</i>
              <span>Não lidas</span>
              <span class="tab-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
            </button>
            <button 
              class="filter-tab" 
              :class="{ active: activeFilter === 'pedidos' }"
              @click="setActiveFilter('pedidos')"
            >
              <i class="material-icons">assignment</i>
              <span>Pedidos</span>
              <span class="tab-badge">{{ pedidoNotifications.length }}</span>
            </button>
          </div>
        </div>
        
        <!-- Conteúdo das notificações -->
        <div class="notification-content-area">
          <div v-if="notifications.length > 0" class="notifications-container">
            <!-- Lista de notificações -->
            <div class="notification-list">
              <div 
                v-for="notification in filteredNotifications" 
                :key="notification.id"
                class="notification-item"
                :class="{ 
                  'unread': !notification.read,
                  'clickable': isClickable(notification)
                }"
                @click="handleNotificationClick(notification)"
              >
                <div class="notification-icon-wrapper">
                  <div class="notification-icon-type" :class="getNotificationTypeClass(notification.type)">
                    <i class="material-icons">{{ getNotificationIcon(notification.type) }}</i>
                  </div>
                  <div v-if="!notification.read" class="unread-indicator"></div>
                </div>
                
                <div class="notification-content">
                  <div class="notification-header-item">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                  </div>
                  <div class="notification-message">{{ notification.message }}</div>
                  <div class="notification-meta" v-if="notification.data && notification.data.pedido">
                    <span class="meta-item">
                      <i class="material-icons">tag</i>
                      Pedido #{{ notification.data.pedido.id }}
                    </span>
                    <span class="meta-item" v-if="notification.data.pedido.setor">
                      <i class="material-icons">business</i>
                      {{ notification.data.pedido.setor }}
                    </span>
                  </div>
                </div>
                
                <div class="notification-actions">
                  <button 
                    v-if="!notification.read" 
                    @click.stop="markAsRead(notification.id)" 
                    class="mini-action-btn"
                    title="Marcar como lida"
                  >
                    <i class="material-icons">done</i>
                  </button>
                  <button 
                    @click.stop="removeNotification(notification.id)" 
                    class="mini-action-btn danger"
                    title="Remover notificação"
                  >
                    <i class="material-icons">close</i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Estado vazio -->
          <div v-else class="empty-state">
            <div class="empty-icon">
              <i class="material-icons">notifications_none</i>
            </div>
            <h3>Nenhuma notificação</h3>
            <p>Você está em dia! Não há notificações pendentes no momento.</p>
          </div>
        </div>

        <!-- Botões de ação padrão do sistema -->
        <div class="button-row">
          <button class="close-btn" @click="closeNotifications">FECHAR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';

export default {
  name: 'NotificationIndicator',
  setup() {
    const notifications = ref([]);
    const showDropdown = ref(false);
    const websocketService = ref(null);
    const activeFilter = ref('all');
    
    // Computed para verificar se deve mostrar o indicador (apenas para admin/gestor)
    const showIndicator = computed(() => {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      return user.tipo_usuario === 'admin' || user.tipo_usuario === 'gestor';
    });
    
    // Computed para contar notificações não lidas
    const unreadCount = computed(() => {
      return notifications.value.filter(n => !n.read).length;
    });
    
    // Computed para notificações de pedidos
    const pedidoNotifications = computed(() => {
      return notifications.value.filter(n => 
        n.type && (n.type.includes('pedido') || n.type === 'novo_pedido' || n.type === 'pedido_concluido')
      );
    });
    
    // Computed para notificações filtradas
    const filteredNotifications = computed(() => {
      switch (activeFilter.value) {
        case 'unread':
          return notifications.value.filter(n => !n.read);
        case 'pedidos':
          return pedidoNotifications.value;
        default:
          return notifications.value;
      }
    });
    
    // Função para definir filtro ativo
    const setActiveFilter = (filter) => {
      activeFilter.value = filter;
    };
    
    // Função para alternar dropdown
    const toggleNotifications = () => {
      showDropdown.value = !showDropdown.value;
      if (showDropdown.value) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    };
    
    // Função para fechar notificações
    const closeNotifications = () => {
      showDropdown.value = false;
      document.body.style.overflow = '';
    };
    
    // Função para verificar se notificação é clicável
    const isClickable = (notification) => {
      return notification.data && notification.data.pedido && notification.data.pedido.id;
    };
    
    // Função para adicionar nova notificação
    const addNotification = (notificationData) => {
      // Criar ID único para evitar duplicatas
      const uniqueId = `${notificationData.type}_${notificationData.data?.pedido?.id || 'unknown'}_${notificationData.timestamp}`;
      
      // Verificar se já existe uma notificação com este ID
      const existingNotification = notifications.value.find(n => n.uniqueId === uniqueId);
      if (existingNotification) {
        console.log('Notificação duplicada ignorada no indicador:', uniqueId);
        return;
      }
      
      // Processar dados da notificação WebSocket
      let processedData;
      
      if (notificationData.data && typeof notificationData.data === 'object') {
        // Notificação vem do WebSocket com estrutura aninhada
        processedData = {
          title: notificationData.data.title || 'Nova Notificação',
          message: notificationData.data.message || '',
          type: notificationData.type || 'info',
          timestamp: new Date(notificationData.timestamp || Date.now()),
          data: notificationData.data || {}
        };
      } else {
        // Notificação direta ou formato simples
        processedData = {
          title: notificationData.title || 'Nova Notificação',
          message: notificationData.message || '',
          type: notificationData.type || 'info',
          timestamp: new Date(notificationData.timestamp || Date.now()),
          data: notificationData.data || {}
        };
      }
      
      const notification = {
        id: Date.now() + Math.random(),
        uniqueId: uniqueId, // Adicionar ID único
        ...processedData,
        read: false
      };
      
      console.log('Adicionando notificação ao indicador:', uniqueId);
      
      // Adicionar no início da lista
      notifications.value.unshift(notification);
      
      // Limitar a 50 notificações
      if (notifications.value.length > 50) {
        notifications.value = notifications.value.slice(0, 50);
      }
      
      // Salvar no localStorage
      saveNotifications();
    };
    
    // Função para marcar notificação como lida
    const markAsRead = (notificationId) => {
      const notification = notifications.value.find(n => n.id === notificationId);
      if (notification) {
        notification.read = true;
        saveNotifications();
      }
    };
    
    // Função para marcar todas como lidas
    const markAllAsRead = () => {
      notifications.value.forEach(n => n.read = true);
      saveNotifications();
    };
    
    // Função para remover notificação
    const removeNotification = (notificationId) => {
      const index = notifications.value.findIndex(n => n.id === notificationId);
      if (index > -1) {
        notifications.value.splice(index, 1);
        saveNotifications();
      }
    };
    
    // Função para limpar todas as notificações
    const clearAllNotifications = () => {
      notifications.value = [];
      saveNotifications();
      closeNotifications();
    };
    
    // Função para lidar com clique na notificação
    const handleNotificationClick = (notification) => {
      markAsRead(notification.id);
      
      // Se a notificação tem dados de pedido, abrir modal de impressão
      if (notification.data && notification.data.pedido && notification.data.pedido.id) {
        // Fechar dropdown
        closeNotifications();
        
        // Emitir evento para abrir modal de impressão no AppMenu
        window.dispatchEvent(new CustomEvent('open-print-modal', {
          detail: { pedidoId: notification.data.pedido.id }
        }));
      }
    };
    
    // Função para obter ícone baseado no tipo
    const getNotificationIcon = (type) => {
      switch (type) {
        case 'novo_pedido':
          return 'add_circle';
        case 'pedido_atualizado':
          return 'edit';
        case 'pedido_concluido':
          return 'check_circle';
        case 'error':
          return 'error';
        case 'warning':
          return 'warning';
        case 'teste':
          return 'science';
        default:
          return 'info';
      }
    };
    
    // Função para obter classe do tipo de notificação
    const getNotificationTypeClass = (type) => {
      switch (type) {
        case 'novo_pedido':
          return 'type-new';
        case 'pedido_atualizado':
          return 'type-update';
        case 'pedido_concluido':
          return 'type-success';
        case 'error':
          return 'type-error';
        case 'warning':
          return 'type-warning';
        case 'teste':
          return 'type-test';
        default:
          return 'type-info';
      }
    };
    
    // Função para formatar tempo
    const formatTime = (timestamp) => {
      const now = new Date();
      const time = new Date(timestamp);
      const diffInMinutes = Math.floor((now - time) / (1000 * 60));
      
      if (diffInMinutes < 1) {
        return 'Agora';
      } else if (diffInMinutes < 60) {
        return `${diffInMinutes}m atrás`;
      } else if (diffInMinutes < 1440) {
        const hours = Math.floor(diffInMinutes / 60);
        return `${hours}h atrás`;
      } else {
        const days = Math.floor(diffInMinutes / 1440);
        return `${days}d atrás`;
      }
    };
    
    // Função para salvar notificações no localStorage
    const saveNotifications = () => {
      localStorage.setItem('notifications', JSON.stringify(notifications.value));
    };
    
    // Função para carregar notificações do localStorage
    const loadNotifications = () => {
      try {
        const saved = localStorage.getItem('notifications');
        if (saved) {
          const parsed = JSON.parse(saved);
          // Converter timestamps de volta para Date objects
          notifications.value = parsed.map(n => ({
            ...n,
            timestamp: new Date(n.timestamp)
          }));
        }
      } catch (error) {
        console.error('Erro ao carregar notificações:', error);
        notifications.value = [];
      }
    };
    
    // Função para conectar ao WebSocket (será chamada pelo AppMenu)
    const connectToWebSocket = (websocketServiceInstance) => {
      try {
        websocketService.value = websocketServiceInstance;
        
        // Registrar callback para novas notificações
        websocketService.value.onNotification(addNotification);
        
        console.log('NotificationIndicator registrado no WebSocket');
      } catch (error) {
        console.error('Erro ao registrar NotificationIndicator no WebSocket:', error);
      }
    };
    
    onMounted(() => {
      // Carregar notificações salvas
      loadNotifications();
      
      // Escutar evento do AppMenu para conectar ao WebSocket
      window.addEventListener('websocket-ready', (event) => {
        if (showIndicator.value && event.detail.websocketService) {
          connectToWebSocket(event.detail.websocketService);
        }
      });
      
      // Listener para fechar com ESC
      const handleEscape = (event) => {
        if (event.key === 'Escape' && showDropdown.value) {
          closeNotifications();
        }
      };
      document.addEventListener('keydown', handleEscape);
    });
    
    onUnmounted(() => {
      // Desregistrar callback do WebSocket
      if (websocketService.value) {
        websocketService.value.offNotification(addNotification);
      }
      
      // Restaurar overflow do body
      document.body.style.overflow = '';
    });
    
    return {
      notifications,
      showDropdown,
      showIndicator,
      unreadCount,
      activeFilter,
      filteredNotifications,
      pedidoNotifications,
      toggleNotifications,
      closeNotifications,
      setActiveFilter,
      markAsRead,
      markAllAsRead,
      removeNotification,
      clearAllNotifications,
      handleNotificationClick,
      getNotificationIcon,
      getNotificationTypeClass,
      formatTime,
      isClickable
    };
  }
};
</script>

<style scoped>
/* Indicador de notificação */
.notification-indicator {
  position: relative;
  display: inline-block;
}

.notification-icon {
  position: relative;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
}

.notification-icon:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  transform: scale(1.05);
}

.notification-icon.has-notifications {
  color: #ff6f61;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: bold;
  min-width: 18px;
  text-align: center;
  line-height: 1.2;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.4);
  border: 2px solid #1f1f1f;
}

/* Modal Overlay - Padrão do sistema */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85); 
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: 20px;
  box-sizing: border-box;
}

/* Estilo do Formulário - Padrão do sistema */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 25px; 
  border-radius: 12px;
  width: 90%;
  max-width: 800px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  overflow-y: auto;
  max-height: 90vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  margin: 20px 0;
}

/* Cabeçalho do formulário - Padrão do sistema */
.form-header {
  margin-bottom: 25px;
  border-bottom: 1px solid #333;
  padding-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

/* Título do formulário - Padrão do sistema */
.form-header h2 {
  color: #ff6f61; 
  font-size: 1.4rem;
  margin: 0;
}

/* Informações das notificações */
.notification-summary {
  background-color: #333;
  padding: 5px 10px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 0.9rem;
}

.notification-count {
  color: #999;
}

.unread-count {
  color: #ff6f61;
  font-weight: bold;
}

/* Ações do header */
.notification-actions-header {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.action-btn {
  background-color: #333;
  border: 1px solid #444;
  color: #f5f5f5;
  padding: 8px 15px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.action-btn:hover:not(:disabled) {
  background-color: #444;
  border-color: #ff6f61;
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.secondary:hover:not(:disabled) {
  background-color: #4db6ac;
  border-color: #4db6ac;
  color: white;
}

.action-btn.danger:hover:not(:disabled) {
  background-color: #e74c3c;
  border-color: #e74c3c;
  color: white;
}

/* Filtros */
.notification-filters {
  background-color: #333;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.filter-tabs {
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.filter-tab {
  background: none;
  border: 1px solid #444;
  color: #999;
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  border-radius: 5px;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 500;
}

.filter-tab:hover {
  color: #ff6f61;
  border-color: #ff6f61;
  background-color: rgba(255, 111, 97, 0.1);
}

.filter-tab.active {
  color: #ff6f61;
  border-color: #ff6f61;
  background-color: rgba(255, 111, 97, 0.2);
}

.tab-badge {
  background: #ff6f61;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 10px;
  font-weight: 600;
  min-width: 16px;
  text-align: center;
}

/* Área de conteúdo */
.notification-content-area {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 50vh;
}

.notifications-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Lista de notificações */
.notification-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  margin-bottom: 10px;
  background-color: #333;
  border-radius: 8px;
  border: 1px solid #444;
  transition: all 0.3s ease;
  position: relative;
}

.notification-item:hover {
  background-color: #3a3a3a;
  border-color: #555;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.notification-item.unread {
  background-color: rgba(255, 111, 97, 0.05);
  border-left: 4px solid #ff6f61;
}

.notification-item.clickable {
  cursor: pointer;
}

.notification-item.clickable:hover {
  background-color: rgba(255, 111, 97, 0.1);
}

.notification-icon-wrapper {
  position: relative;
  margin-right: 15px;
  flex-shrink: 0;
}

.notification-icon-type {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.notification-icon-type.type-new {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.notification-icon-type.type-update {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.notification-icon-type.type-success {
  background: linear-gradient(135deg, #2ecc71, #27ae60);
}

.notification-icon-type.type-error {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.notification-icon-type.type-warning {
  background: linear-gradient(135deg, #f39c12, #e67e22);
}

.notification-icon-type.type-test {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
}

.notification-icon-type.type-info {
  background: linear-gradient(135deg, #3498db, #2980b9);
}

.unread-indicator {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 12px;
  height: 12px;
  background: #ff6f61;
  border-radius: 50%;
  border: 2px solid #1f1f1f;
  animation: pulse 2s infinite;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
  gap: 10px;
}

.notification-title {
  font-weight: 600;
  font-size: 14px;
  color: #f5f5f5;
  line-height: 1.3;
  flex: 1;
}

.notification-time {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
  flex-shrink: 0;
}

.notification-message {
  font-size: 14px;
  color: #ccc;
  line-height: 1.4;
  margin-bottom: 10px;
  word-wrap: break-word;
}

.notification-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #999;
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 6px;
  border-radius: 3px;
}

.meta-item i {
  font-size: 14px;
  opacity: 0.7;
}

.notification-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-left: 10px;
  flex-shrink: 0;
}

.mini-action-btn {
  background-color: #444;
  border: 1px solid #555;
  color: #ccc;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 16px;
}

.mini-action-btn:hover {
  background-color: #ff6f61;
  border-color: #ff6f61;
  color: white;
  transform: scale(1.1);
}

.mini-action-btn.danger:hover {
  background-color: #e74c3c;
  border-color: #e74c3c;
}

/* Estado vazio */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  color: #999;
  flex: 1;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 111, 97, 0.1), rgba(255, 111, 97, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  border: 2px solid rgba(255, 111, 97, 0.2);
}

.empty-icon i {
  font-size: 40px;
  color: #ff6f61;
  opacity: 0.7;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #f5f5f5;
  font-size: 18px;
  font-weight: 600;
}

.empty-state p {
  margin: 0 0 20px 0;
  font-size: 14px;
  line-height: 1.5;
  max-width: 300px;
}

/* Botões de ação padrão do sistema */
.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #333;
}

.close-btn {
  background-color: #ff6f61;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.close-btn:hover {
  background-color: #e55b55;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 111, 97, 0.3);
}

/* Responsividade */
@media (max-width: 1024px) {
  .order-form {
    max-width: 95%;
    padding: 20px;
  }
  
  .form-header {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .action-buttons {
    justify-content: space-between;
  }
  
  .btn-text {
    display: none;
  }
  
  .action-btn {
    padding: 8px;
    min-width: 40px;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .order-form {
    max-width: 100%;
    max-height: 95vh;
    padding: 15px;
  }
  
  .notification-content-area {
    max-height: 40vh;
  }
  
  .notification-item {
    padding: 10px;
    margin-bottom: 8px;
  }
  
  .notification-icon-type {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }
  
  .notification-actions {
    flex-direction: row;
  }
  
  .mini-action-btn {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: 5px;
  }
  
  .order-form {
    max-height: 98vh;
    padding: 10px;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
  }
  
  .filter-tab span:not(.tab-badge) {
    display: none;
  }
  
  .notification-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .notification-icon-wrapper {
    margin-right: 0;
    align-self: flex-start;
  }
  
  .notification-header-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
  
  .notification-actions {
    flex-direction: row;
    align-self: flex-end;
    margin-left: 0;
  }
  
  .empty-state {
    padding: 20px;
  }
  
  .empty-icon {
    width: 60px;
    height: 60px;
  }
  
  .empty-icon i {
    font-size: 30px;
  }
}
</style> 