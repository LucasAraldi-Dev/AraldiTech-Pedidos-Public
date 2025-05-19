<template>
  <div v-if="isOpen" class="log-detail-overlay" @click.self="closeModal">
    <div class="log-detail-modal" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">
          <i class="material-icons">description</i>
          Detalhes do Log
        </h2>
        <button class="close-button" @click="closeModal">
          <i class="material-icons">close</i>
        </button>
      </div>

      <div class="modal-content" v-if="log">
        <div class="log-detail-header">
          <div class="log-type-badge" :class="getLogTypeClass(log.tipo)">
            <i class="material-icons">{{ getLogTypeIcon(log.tipo) }}</i>
            {{ formatLogType(log.tipo) }}
          </div>
          <div class="log-date-time">
            <i class="material-icons">event</i>
            {{ formatDateTime(log.data) }}
          </div>
        </div>

        <div class="log-detail-section">
          <h3>Descrição do Evento</h3>
          <p class="log-description">{{ log.descricao }}</p>
        </div>

        <div class="log-detail-grid">
          <div class="log-detail-item">
            <span class="detail-label">ID:</span>
            <span class="detail-value">{{ log.id || 'N/A' }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">Tipo:</span>
            <span class="detail-value">{{ formatLogType(log.tipo) }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">Usuário:</span>
            <span class="detail-value">{{ log.usuario_nome || 'Sistema' }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">ID do Usuário:</span>
            <span class="detail-value">{{ log.usuario_id || 'N/A' }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">Endereço IP:</span>
            <span class="detail-value">{{ log.ip_address || 'Não registrado' }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">User Agent:</span>
            <span class="detail-value">{{ log.user_agent || 'Não registrado' }}</span>
          </div>
          
          <div class="log-detail-item" v-if="log.pedido_id">
            <span class="detail-label">ID do Pedido:</span>
            <span class="detail-value">#{{ log.pedido_id }}</span>
          </div>
          
          <div class="log-detail-item" v-if="log.entidade">
            <span class="detail-label">Entidade:</span>
            <span class="detail-value">{{ log.entidade }}</span>
          </div>
          
          <div class="log-detail-item" v-if="log.entidade_id">
            <span class="detail-label">ID da Entidade:</span>
            <span class="detail-value">{{ log.entidade_id }}</span>
          </div>
          
          <div class="log-detail-item">
            <span class="detail-label">Data Criação:</span>
            <span class="detail-value">{{ formatDateTime(log.data) }}</span>
          </div>
        </div>

        <div class="log-detail-section" v-if="log.dados_adicionais">
          <h3>Dados Adicionais</h3>
          <pre class="json-data">{{ formatJsonData(log.dados_adicionais) }}</pre>
        </div>

        <div class="log-detail-section" v-if="log.pedido_id">
          <h3>Ações</h3>
          <div class="log-actions">
            <button class="action-btn view-order-btn" @click="viewOrder">
              <i class="material-icons">visibility</i>
              Ver Pedido
            </button>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button @click="copyToClipboard" class="copy-button">
          <i class="material-icons">content_copy</i>
          COPIAR DADOS
        </button>
        <button @click="closeModal" class="close-button">
          <i class="material-icons">close</i>
          FECHAR
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  name: "ModalLogDetail",
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    log: {
      type: Object,
      default: null
    },
    onClose: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      toast: useToast()
    };
  },
  methods: {
    closeModal() {
      this.onClose();
    },
    formatDateTime(dateString) {
      if (!dateString) return 'Data desconhecida';
      
      try {
        const date = new Date(dateString);
        return date.toLocaleString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
      } catch (error) {
        console.error('Erro ao formatar data:', error);
        return dateString;
      }
    },
    formatLogType(type) {
      const types = {
        login: 'AUTENTICAÇÃO',
        criacao: 'CRIAÇÃO',
        edicao: 'EDIÇÃO',
        conclusao: 'CONCLUSÃO',
        orcamento: 'ORÇAMENTO',
        erro: 'ERRO',
        seguranca: 'SEGURANÇA',
        registro: 'CADASTRO',
        cancelamento: 'CANCELAMENTO'
      };
      
      return types[type] || type.toUpperCase();
    },
    getLogTypeIcon(type) {
      const icons = {
        login: 'login',
        criacao: 'add_circle',
        edicao: 'edit',
        conclusao: 'check_circle',
        orcamento: 'attach_money',
        erro: 'error',
        seguranca: 'security',
        registro: 'person_add',
        cancelamento: 'cancel'
      };
      
      return icons[type] || 'info';
    },
    getLogTypeClass(type) {
      return `log-type-${type}`;
    },
    formatJsonData(data) {
      if (!data) return 'Nenhum dado adicional';
      
      try {
        if (typeof data === 'string') {
          return JSON.stringify(JSON.parse(data), null, 2);
        } else {
          return JSON.stringify(data, null, 2);
        }
      } catch (error) {
        console.error('Erro ao formatar JSON:', error);
        return String(data);
      }
    },
    copyToClipboard() {
      if (!this.log) return;
      
      try {
        const logData = {
          id: this.log.id,
          tipo: this.formatLogType(this.log.tipo),
          descricao: this.log.descricao,
          data: this.formatDateTime(this.log.data),
          usuario: this.log.usuario_nome || 'Sistema',
          usuario_id: this.log.usuario_id || 'N/A',
          ip: this.log.ip_address || 'Não registrado',
          user_agent: this.log.user_agent || 'Não registrado',
          pedido_id: this.log.pedido_id || 'N/A',
          entidade: this.log.entidade || 'N/A',
          entidade_id: this.log.entidade_id || 'N/A',
          dados_adicionais: this.log.dados_adicionais || 'Nenhum'
        };
        
        const textToCopy = Object.entries(logData)
          .map(([key, value]) => `${key}: ${value}`)
          .join('\n');
        
        navigator.clipboard.writeText(textToCopy)
          .then(() => {
            this.toast.success('Dados do log copiados para a área de transferência');
          })
          .catch(err => {
            console.error('Erro ao copiar para a área de transferência:', err);
            this.toast.error('Não foi possível copiar os dados');
          });
      } catch (error) {
        console.error('Erro ao preparar dados para cópia:', error);
        this.toast.error('Erro ao copiar os dados');
      }
    },
    viewOrder() {
      if (this.log && this.log.pedido_id) {
        console.log(`ModalLogDetail: Emitindo evento view-order com pedidoId: ${this.log.pedido_id}`);
        
        // Verificar tipo de dados do pedido_id para garantir compatibilidade
        const pedidoId = parseInt(this.log.pedido_id, 10);
        if (isNaN(pedidoId)) {
          console.warn(`O ID do pedido não é um número válido: ${this.log.pedido_id}`);
          this.$emit('view-order', this.log.pedido_id);
        } else {
          console.log(`Emitindo view-order com pedidoId numérico: ${pedidoId}`);
          this.$emit('view-order', pedidoId);
        }
        
        // Notificar usuário que a ação foi reconhecida
        this.toast.info(`Buscando detalhes do pedido #${this.log.pedido_id}...`);
      } else {
        console.error('Não é possível visualizar o pedido: ID não encontrado no log', this.log);
        this.toast.error('Não foi possível identificar o pedido associado a este log');
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

.log-detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1200;
  padding: 20px;
}

.log-detail-modal {
  background-color: #1f1f1f;
  border-radius: 10px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  color: #f5f5f5;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #333;
  background-color: #252525;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.modal-title {
  display: flex;
  align-items: center;
  font-size: 20px;
  margin: 0;
}

.modal-title i {
  margin-right: 10px;
  color: #ff6f61;
}

.modal-content {
  padding: 20px;
  overflow-y: auto;
}

.log-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #333;
}

.log-type-badge {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  border-radius: 20px;
  background-color: #333;
  font-weight: bold;
}

.log-type-badge i {
  margin-right: 8px;
}

.log-date-time {
  display: flex;
  align-items: center;
  color: #aaa;
}

.log-date-time i {
  margin-right: 8px;
}

.log-detail-section {
  margin-bottom: 25px;
}

.log-detail-section h3 {
  font-size: 18px;
  margin: 0 0 15px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #444;
  color: #ff6f61;
}

.log-description {
  font-size: 16px;
  line-height: 1.5;
  background-color: #252525;
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid #ff6f61;
}

.log-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.log-detail-item {
  display: flex;
  flex-direction: column;
  background-color: #252525;
  padding: 12px;
  border-radius: 6px;
}

.detail-label {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 5px;
}

.detail-value {
  font-size: 14px;
  word-break: break-word;
}

.json-data {
  background-color: #252525;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.4;
  white-space: pre-wrap;
  color: #ddd;
}

.log-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn i {
  margin-right: 8px;
}

.view-order-btn {
  background-color: #4caf50;
  color: white;
}

.view-order-btn:hover {
  background-color: #45a049;
}

.modal-actions {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid #333;
  background-color: #252525;
}

.close-button, .copy-button {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.close-button {
  background-color: #444;
  color: white;
}

.close-button:hover {
  background-color: #555;
}

.copy-button {
  background-color: #ff6f61;
  color: white;
}

.copy-button:hover {
  background-color: #e74c3c;
}

.copy-button i, .close-button i {
  margin-right: 8px;
}

/* Estilos específicos para tipos de log */
.log-type-login {
  background-color: rgba(52, 152, 219, 0.2);
  color: #3498db;
}

.log-type-criacao {
  background-color: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
}

.log-type-edicao {
  background-color: rgba(243, 156, 18, 0.2);
  color: #f39c12;
}

.log-type-conclusao {
  background-color: rgba(39, 174, 96, 0.2);
  color: #27ae60;
}

.log-type-orcamento {
  background-color: rgba(155, 89, 182, 0.2);
  color: #9b59b6;
}

.log-type-erro {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.log-type-seguranca {
  background-color: rgba(142, 68, 173, 0.2);
  color: #8e44ad;
}

.log-type-registro {
  background-color: rgba(22, 160, 133, 0.2);
  color: #16a085;
}

.log-type-cancelamento {
  background-color: rgba(192, 57, 43, 0.2);
  color: #c0392b;
}

/* Responsividade */
@media (max-width: 768px) {
  .log-detail-grid {
    grid-template-columns: 1fr;
  }
  
  .log-detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .close-button, .copy-button {
    width: 100%;
    justify-content: center;
  }
}
</style> 