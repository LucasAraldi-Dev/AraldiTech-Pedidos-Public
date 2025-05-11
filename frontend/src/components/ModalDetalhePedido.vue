<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Detalhes do Pedido #{{ pedido.id }}</h2>
        <button class="close-btn" @click="fecharModal">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="pedido-details">
          <div class="detail-row">
            <div class="detail-label">Status:</div>
            <div class="detail-value" :class="'status-' + (pedido.status || 'pendente').toLowerCase()">
              {{ pedido.status || 'Pendente' }}
            </div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Descrição:</div>
            <div class="detail-value">{{ pedido.descricao }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Quantidade:</div>
            <div class="detail-value">{{ pedido.quantidade }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Categoria:</div>
            <div class="detail-value">{{ pedido.categoria || 'Não categorizado' }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Urgência:</div>
            <div class="detail-value">{{ pedido.urgencia || 'Padrão' }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Data do Pedido:</div>
            <div class="detail-value">{{ formatarData(pedido.deliveryDate) }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Solicitante:</div>
            <div class="detail-value">{{ pedido.sender || 'Não informado' }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Observação:</div>
            <div class="detail-value">{{ pedido.observacao || 'Sem observações' }}</div>
          </div>
          
          <div class="detail-row" v-if="pedido.anexo">
            <div class="detail-label">Anexo:</div>
            <div class="detail-value">
              <img :src="pedido.anexo" alt="Anexo" class="anexo-imagem" />
            </div>
          </div>
        </div>
        
        <div v-if="historico && historico.length > 0" class="historico-section">
          <h3>Histórico de Alterações</h3>
          <div class="historico-list">
            <div v-for="(item, index) in historico" :key="index" class="historico-item">
              <div class="historico-header">
                <span class="historico-user">{{ item.usuario_nome }}</span>
                <span class="historico-date">{{ formatarDataHora(item.data_edicao) }}</span>
              </div>
              <div class="historico-content">
                <span class="campo">{{ item.campo_alterado }}</span>:
                <span class="valor-antigo">{{ item.valor_anterior }}</span> →
                <span class="valor-novo">{{ item.valor_novo }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="fecharModal">Fechar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import authService from '@/api/authService';

export default {
  name: 'ModalDetalhePedido',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    pedido: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      historico: []
    };
  },
  async mounted() {
    if (this.isOpen && this.pedido) {
      await this.carregarHistorico();
    }
  },
  methods: {
    fecharModal() {
      this.$emit('close');
    },
    
    formatarData(dataString) {
      if (!dataString) return 'Data não informada';
      
      try {
        const data = new Date(dataString);
        
        // Verificar se a data é válida
        if (isNaN(data.getTime())) {
          console.warn(`Data inválida: ${dataString}`);
          return 'Data inválida';
        }
        
        return data.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
      } catch (error) {
        console.error(`Erro ao formatar data: ${dataString}`, error);
        return 'Erro de formato';
      }
    },
    
    formatarDataHora(dataString) {
      if (!dataString) return 'Data não informada';
      
      try {
        const data = new Date(dataString);
        
        // Verificar se a data é válida
        if (isNaN(data.getTime())) {
          console.warn(`Data/hora inválida: ${dataString}`);
          return 'Data/hora inválida';
        }
        
        return new Intl.DateTimeFormat('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        }).format(data);
      } catch (error) {
        console.error(`Erro ao formatar data/hora: ${dataString}`, error);
        return 'Erro de formato';
      }
    },
    
    async carregarHistorico() {
      try {
        const response = await axios.get(`/pedidos/${this.pedido.id}/historico`, {
          headers: authService.getAuthHeaders()
        });
        this.historico = response.data;
      } catch (error) {
        console.error('Erro ao carregar histórico do pedido:', error);
        this.historico = [];
      }
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #777;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.pedido-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  gap: 15px;
}

.detail-label {
  flex: 0 0 120px;
  font-weight: bold;
  color: #555;
}

.detail-value {
  flex: 1;
}

.status-pendente {
  color: #f0ad4e;
  font-weight: bold;
}

.status-em.andamento {
  color: #337ab7;
  font-weight: bold;
}

.status-concluído {
  color: #5cb85c;
  font-weight: bold;
}

.status-cancelado {
  color: #d9534f;
  font-weight: bold;
}

.anexo-imagem {
  max-width: 100%;
  max-height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.historico-section {
  margin-top: 25px;
  border-top: 1px dashed #ddd;
  padding-top: 15px;
}

.historico-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.historico-item {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 10px 15px;
}

.historico-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.historico-user {
  font-weight: bold;
  color: #444;
}

.historico-date {
  font-size: 0.85em;
  color: #777;
}

.historico-content {
  font-size: 0.95em;
}

.historico-content .campo {
  font-weight: bold;
}

.historico-content .valor-antigo {
  color: #d9534f;
  text-decoration: line-through;
}

.historico-content .valor-novo {
  color: #5cb85c;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.btn {
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style> 