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
            <div class="detail-value" v-sanitize="pedido.descricao"></div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Quantidade:</div>
            <div class="detail-value">{{ pedido.quantidade }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Categoria:</div>
            <div class="detail-value" v-sanitize="pedido.categoria || 'Não categorizado'"></div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Urgência:</div>
            <div class="detail-value" v-sanitize="pedido.urgencia || 'Padrão'"></div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Data do Pedido:</div>
            <div class="detail-value">{{ formatarData(pedido.deliveryDate) }}</div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Solicitante:</div>
            <div class="detail-value" v-sanitize="pedido.sender || 'Não informado'"></div>
          </div>
          
          <div class="detail-row">
            <div class="detail-label">Observação:</div>
            <div class="detail-value" v-sanitize="pedido.observacao || 'Sem observações'"></div>
          </div>
          
          <div class="detail-row" v-if="pedido.anexo">
            <div class="detail-label">Anexo:</div>
            <div class="detail-value">
              <img v-if="isValidImageUrl(pedido.anexo)" :src="pedido.anexo" alt="Anexo" class="anexo-imagem" />
              <div v-else class="anexo-erro">Anexo inválido ou não suportado</div>
            </div>
          </div>
        </div>
        
        <div v-if="historico && historico.length > 0" class="historico-section">
          <h3>Histórico de Alterações</h3>
          <div class="historico-list">
            <div v-for="(item, index) in historico" :key="index" class="historico-item">
              <div class="historico-header">
                <span class="historico-user" v-sanitize="item.usuario_nome"></span>
                <span class="historico-date">{{ formatarDataHora(item.data_edicao) }}</span>
              </div>
              <div class="historico-content">
                <span class="campo" v-sanitize="item.campo_alterado"></span>:
                <span class="valor-antigo" v-sanitize="item.valor_anterior"></span> →
                <span class="valor-novo" v-sanitize="item.valor_novo"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Dados de Conclusão (se o pedido estiver concluído) -->
        <div v-if="pedido.status === 'Concluído' && pedido.conclusao_dados" class="conclusion-section">
          <h3><i class="material-icons">check_circle</i> Dados da Conclusão</h3>
          
          <div class="conclusion-grid">
            <!-- Informações Financeiras -->
            <div class="conclusion-item" v-if="pedido.conclusao_dados.valor_total || pedido.conclusao_dados.preco_unitario">
              <h4><i class="material-icons">attach_money</i> Informações Financeiras</h4>
              <div class="financial-details">
                <p v-if="pedido.conclusao_dados.preco_unitario">
                  <strong>Preço Unitário:</strong> R$ {{ formatCurrency(pedido.conclusao_dados.preco_unitario) }}
                </p>
                <p v-if="pedido.conclusao_dados.valor_total">
                  <strong>Valor Total:</strong> R$ {{ formatCurrency(pedido.conclusao_dados.valor_total) }}
                </p>
                <p v-if="pedido.conclusao_dados.fornecedor">
                  <strong>Fornecedor:</strong> {{ pedido.conclusao_dados.fornecedor }}
                </p>
              </div>
            </div>

            <!-- Tipo de Atendimento -->
            <div class="conclusion-item" v-if="pedido.conclusao_dados.tem_mao_de_obra || pedido.conclusao_dados.tem_material">
              <h4><i class="material-icons">build</i> Tipo de Atendimento</h4>
              <div class="service-types">
                <span v-if="pedido.conclusao_dados.tem_mao_de_obra" class="service-badge">
                  <i class="material-icons">build</i> Mão de Obra
                </span>
                <span v-if="pedido.conclusao_dados.tem_material" class="service-badge">
                  <i class="material-icons">inventory</i> Material
                </span>
              </div>
            </div>

            <!-- Avaliação -->
            <div class="conclusion-item" v-if="pedido.conclusao_dados.avaliacao">
              <h4><i class="material-icons">star</i> Avaliação</h4>
              <div class="rating-display">
                <span class="rating-value" :class="getRatingClass(pedido.conclusao_dados.avaliacao)">
                  <i class="material-icons">{{ getRatingIcon(pedido.conclusao_dados.avaliacao) }}</i>
                  {{ capitalizeFirst(pedido.conclusao_dados.avaliacao) }}
                </span>
              </div>
            </div>

            <!-- Feedback -->
            <div class="conclusion-item" v-if="pedido.conclusao_dados.feedback">
              <h4><i class="material-icons">feedback</i> Feedback</h4>
              <div class="feedback-content">
                <p>{{ pedido.conclusao_dados.feedback }}</p>
              </div>
            </div>

            <!-- Anexo -->
            <div class="conclusion-item" v-if="pedido.conclusao_dados.anexo_url">
              <h4><i class="material-icons">attach_file</i> Comprovante</h4>
              <div class="attachment-link">
                <a :href="getAttachmentUrl(pedido.conclusao_dados.anexo_url)" target="_blank" class="download-btn">
                  <i class="material-icons">download</i>
                  Visualizar Comprovante
                </a>
              </div>
            </div>

            <!-- Dados da Conclusão -->
            <div class="conclusion-item">
              <h4><i class="material-icons">event_available</i> Dados da Conclusão</h4>
              <div class="conclusion-meta">
                <p v-if="pedido.conclusao_dados.data_conclusao">
                  <strong>Concluído em:</strong> {{ formatDateTime(pedido.conclusao_dados.data_conclusao) }}
                </p>
                <p v-if="pedido.conclusao_dados.usuario_conclusao">
                  <strong>Concluído por:</strong> {{ pedido.conclusao_dados.usuario_conclusao }}
                </p>
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
import { detectScriptInjection } from '@/utils/securityService';

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
    
    // Verifica se uma URL de imagem é válida e segura
    isValidImageUrl(url) {
      if (!url) return false;
      
      // Verifica se parece uma tentativa de XSS
      if (detectScriptInjection(url)) {
        console.warn('Potencial ataque XSS detectado em URL de imagem');
        return false;
      }
      
      // Verificar se é um formato de imagem comum
      const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'];
      const hasValidExtension = validExtensions.some(ext => 
        url.toLowerCase().endsWith(ext)
      );
      
      // Verificar se é uma URL ou um Data URL de imagem válido
      const isDataUrl = url.startsWith('data:image/');
      
      return hasValidExtension || isDataUrl;
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
    },
    
    formatCurrency(value) {
      if (!value) return '0,00';
      return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    
    formatDateTime(dateString) {
      if (!dateString) return 'Data não informada';
      try {
        const date = new Date(dateString);
        return date.toLocaleString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        return 'Data inválida';
      }
    },
    
    getRatingClass(rating) {
      switch(rating) {
        case 'excelente': return 'rating-excellent';
        case 'bom': return 'rating-good';
        case 'regular': return 'rating-regular';
        case 'ruim': return 'rating-bad';
        default: return '';
      }
    },
    
    getRatingIcon(rating) {
      switch(rating) {
        case 'excelente': return 'sentiment_very_satisfied';
        case 'bom': return 'sentiment_satisfied';
        case 'regular': return 'sentiment_neutral';
        case 'ruim': return 'sentiment_dissatisfied';
        default: return 'help';
      }
    },
    
    capitalizeFirst(str) {
      if (!str) return '';
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    
    getAttachmentUrl(url) {
      if (!url) return '#';
      if (url.startsWith('http')) return url;
      return `${process.env.VUE_APP_API_URL}${url}`;
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
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
  color: #666;
}

.modal-body {
  padding: 20px;
  flex: 1;
  overflow-y: auto;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
}

.pedido-details {
  margin-bottom: 24px;
}

.detail-row {
  display: flex;
  margin-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 12px;
}

.detail-label {
  font-weight: bold;
  width: 140px;
  color: #555;
}

.detail-value {
  flex: 1;
}

.anexo-imagem {
  max-width: 100%;
  max-height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.anexo-erro {
  color: #d9534f;
  font-style: italic;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.status-pendente {
  color: #ffc107;
  font-weight: bold;
}

.status-concluido {
  color: #28a745;
  font-weight: bold;
}

.status-cancelado {
  color: #dc3545;
  font-weight: bold;
}

.historico-section {
  margin-top: 24px;
  border-top: 1px solid #e0e0e0;
  padding-top: 16px;
}

.historico-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.2rem;
  color: #333;
}

.historico-list {
  max-height: 300px;
  overflow-y: auto;
}

.historico-item {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 8px;
}

.historico-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.historico-user {
  font-weight: bold;
  color: #0056b3;
}

.historico-date {
  color: #6c757d;
  font-size: 0.9rem;
}

.historico-content {
  line-height: 1.4;
}

.campo {
  font-weight: bold;
}

.valor-antigo {
  text-decoration: line-through;
  color: #dc3545;
}

.valor-novo {
  color: #28a745;
}

.conclusion-section {
  margin-top: 24px;
  border-top: 1px solid #e0e0e0;
  padding-top: 16px;
}

.conclusion-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.2rem;
  color: #333;
}

.conclusion-grid {
  display: flex;
  flex-wrap: wrap;
}

.conclusion-item {
  width: 50%;
  margin-bottom: 16px;
}

.financial-details {
  margin-bottom: 12px;
}

.service-types {
  margin-top: 8px;
}

.service-badge {
  background-color: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
  margin-right: 8px;
}

.rating-display {
  margin-top: 8px;
}

.rating-value {
  font-weight: bold;
  color: #28a745;
}

.feedback-content {
  margin-top: 8px;
}

.attachment-link {
  margin-top: 8px;
}

.download-btn {
  text-decoration: none;
  color: #007bff;
}

.conclusion-meta {
  margin-top: 8px;
}

.rating-excellent {
  color: #28a745;
}

.rating-good {
  color: #17a2b8;
}

.rating-regular {
  color: #ffc107;
}

.rating-bad {
  color: #dc3545;
}
</style> 