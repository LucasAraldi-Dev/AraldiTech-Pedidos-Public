<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="order-form" @click.stop>
      <!-- Header do Modal -->
      <div class="form-header">
        <h2><i class="material-icons">assignment_turned_in</i> PEDIDO CONCLUÍDO</h2>
        <button class="close-btn" @click="closeModal">
          <i class="material-icons">close</i>
          FECHAR
        </button>
      </div>

      <!-- Resumo do Pedido -->
      <div class="order-summary" v-if="pedido">
        <div class="summary-header">
          <span class="order-id">#{{ pedido.id }}</span>
          <span class="status-badge completed">CONCLUÍDO</span>
        </div>
        <h3 class="order-title">{{ sanitizeHtml(pedido.descricao) }}</h3>
        <div class="summary-details">
          <div class="detail-item">
            <i class="material-icons">format_list_numbered</i>
            <span><strong>Quantidade:</strong> {{ pedido.quantidade }}</span>
          </div>
          <div class="detail-item">
            <i class="material-icons">category</i>
            <span><strong>Categoria:</strong> {{ sanitizeHtml(pedido.categoria) }}</span>
          </div>
          <div class="detail-item">
            <i class="material-icons">business</i>
            <span><strong>Setor:</strong> {{ sanitizeHtml(pedido.setor) }}</span>
          </div>
          <div class="detail-item">
            <i class="material-icons">event</i>
            <span><strong>Data do Pedido:</strong> {{ formatDate(pedido.deliveryDate) }}</span>
          </div>
          <div class="detail-item">
            <i class="material-icons">person</i>
            <span><strong>Solicitante:</strong> {{ sanitizeHtml(pedido.usuario_nome) }}</span>
          </div>
        </div>
      </div>

      <!-- Dados de Conclusão -->
      <div class="conclusion-data" v-if="conclusaoData">
        <h3><i class="material-icons">check_circle</i> Dados da Conclusão</h3>
        
        <!-- Data de Conclusão -->
        <div class="conclusion-section">
          <h4><i class="material-icons">event_available</i> Data de Conclusão</h4>
          <div class="info-item">
            <span class="info-value">{{ formatDate(conclusaoData.data_conclusao) }}</span>
            <span class="info-label">Concluído por: {{ conclusaoData.usuario_conclusao }}</span>
          </div>
        </div>

        <!-- Informações Financeiras -->
        <div class="conclusion-section" v-if="hasFinancialData">
          <h4><i class="material-icons">attach_money</i> Informações Financeiras</h4>
          <div class="financial-summary">
            <div class="financial-item" v-if="conclusaoData.preco_unitario > 0">
              <span class="financial-label">Preço por Unidade (Itens):</span>
              <span class="financial-value">R$ {{ formatCurrency(conclusaoData.preco_unitario) }}</span>
            </div>
            <div class="financial-item" v-if="conclusaoData.valor_total > 0">
              <span class="financial-label">Valor Total (Itens):</span>
              <span class="financial-value">R$ {{ formatCurrency(conclusaoData.valor_total) }}</span>
            </div>
            <div class="financial-item" v-if="conclusaoData.valor_mao_de_obra > 0">
              <span class="financial-label">Valor da Mão de Obra:</span>
              <span class="financial-value">R$ {{ formatCurrency(conclusaoData.valor_mao_de_obra) }}</span>
            </div>
            <div class="financial-item total" v-if="conclusaoData.valor_total_com_mao_de_obra > 0">
              <span class="financial-label">Valor Total Final:</span>
              <span class="financial-value">R$ {{ formatCurrency(conclusaoData.valor_total_com_mao_de_obra) }}</span>
            </div>
            <div class="financial-item" v-if="conclusaoData.fornecedor">
              <span class="financial-label">Fornecedor:</span>
              <span class="financial-value">{{ conclusaoData.fornecedor }}</span>
            </div>
          </div>
        </div>

        <!-- Tipo de Atendimento -->
        <div class="conclusion-section">
          <h4><i class="material-icons">build</i> Tipo de Atendimento</h4>
          <div class="service-types">
            <div class="service-type" v-if="conclusaoData.tem_material">
              <i class="material-icons">inventory</i>
              <span>Material / Produto</span>
            </div>
            <div class="service-type" v-if="conclusaoData.tem_mao_de_obra">
              <i class="material-icons">build</i>
              <span>Mão de Obra / Serviço</span>
            </div>
          </div>
        </div>

        <!-- Anexo -->
        <div class="conclusion-section" v-if="hasAttachment">
          <h4><i class="material-icons">attach_file</i> Comprovante</h4>
          <div class="attachment-info">
            <div class="attachment-item">
              <div class="attachment-preview">
                <!-- Miniatura da imagem ou ícone do arquivo -->
                <div class="attachment-thumbnail" @click="togglePreview">
                  <img 
                    v-if="isImageFile(conclusaoData.anexo_tipo)" 
                    :src="conclusaoData.anexo_base64" 
                    :alt="conclusaoData.anexo_nome"
                    class="thumbnail-image"
                  />
                  <div v-else class="file-icon-container">
                    <i class="material-icons file-icon">{{ getFileIcon(conclusaoData.anexo_tipo) }}</i>
                    <span class="file-extension">{{ getFileExtension(conclusaoData.anexo_nome) }}</span>
                  </div>
                </div>
                
                <!-- Detalhes do arquivo -->
                <div class="attachment-details">
                  <span class="attachment-name">{{ conclusaoData.anexo_nome }}</span>
                  <span class="attachment-size">{{ formatFileSize(conclusaoData.anexo_tamanho) }}</span>
                  <span class="attachment-type">{{ getFileTypeDescription(conclusaoData.anexo_tipo) }}</span>
                </div>
              </div>
              
              <!-- Botões de ação -->
              <div class="attachment-actions">
                <button 
                  v-if="isImageFile(conclusaoData.anexo_tipo)" 
                  class="preview-btn" 
                  @click="togglePreview"
                >
                  <i class="material-icons">{{ showPreview ? 'visibility_off' : 'visibility' }}</i>
                  {{ showPreview ? 'Ocultar' : 'Visualizar' }}
                </button>
                <button class="download-btn" @click="downloadAttachment">
                  <i class="material-icons">download</i>
                  Baixar
                </button>
              </div>
            </div>
            
            <!-- Preview expandido da imagem -->
            <div v-if="showPreview && isImageFile(conclusaoData.anexo_tipo)" class="image-preview">
              <div class="preview-header">
                <span class="preview-title">{{ conclusaoData.anexo_nome }}</span>
                <button class="close-preview-btn" @click="togglePreview">
                  <i class="material-icons">close</i>
                </button>
              </div>
              <div class="preview-content">
                <img 
                  :src="conclusaoData.anexo_base64" 
                  :alt="conclusaoData.anexo_nome"
                  class="preview-image"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Feedback e Avaliação -->
        <div class="conclusion-section" v-if="conclusaoData.feedback || conclusaoData.avaliacao">
          <h4><i class="material-icons">feedback</i> Feedback e Avaliação</h4>
          <div class="feedback-section">
            <div class="feedback-item" v-if="conclusaoData.feedback">
              <span class="feedback-label">Comentários:</span>
              <p class="feedback-text">{{ conclusaoData.feedback }}</p>
            </div>
            <div class="rating-item" v-if="conclusaoData.avaliacao">
              <span class="rating-label">Avaliação:</span>
              <div class="rating-display">
                <i class="material-icons" :class="getRatingClass(conclusaoData.avaliacao)">
                  {{ getRatingIcon(conclusaoData.avaliacao) }}
                </i>
                <span class="rating-text">{{ getRatingText(conclusaoData.avaliacao) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Botão de Fechar -->
      <div class="form-actions">
        <button class="action-button close" @click="closeModal">
          <i class="material-icons">close</i>
          FECHAR
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalPedidoConcluido',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    pedido: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  data() {
    return {
      showPreview: false
    };
  },
  computed: {
    conclusaoData() {
      return this.pedido?.conclusao_dados || null;
    },
    hasFinancialData() {
      if (!this.conclusaoData) return false;
      return this.conclusaoData.preco_unitario > 0 || 
             this.conclusaoData.valor_total > 0 || 
             this.conclusaoData.valor_mao_de_obra > 0 ||
             this.conclusaoData.fornecedor;
    },
    hasAttachment() {
      return this.conclusaoData?.anexo_base64 && this.conclusaoData?.anexo_nome;
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
        this.showPreview = false; // Reset preview state when modal closes
      }
    }
  },
  methods: {
    closeModal() {
      document.body.style.overflow = '';
      this.$emit('close');
    },

    sanitizeHtml(text) {
      if (!text) return '';
      return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    },

    formatDate(date) {
      if (!date) return 'Data não informada';
      
      try {
        const d = new Date(date);
        if (isNaN(d.getTime())) {
          return 'Data inválida';
        }
        
        return d.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        return 'Erro de formato';
      }
    },

    formatCurrency(value) {
      if (!value) return '0,00';
      return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },

    formatFileSize(bytes) {
      if (!bytes || bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    getRatingIcon(rating) {
      const icons = {
        'excelente': 'sentiment_very_satisfied',
        'bom': 'sentiment_satisfied',
        'regular': 'sentiment_neutral',
        'ruim': 'sentiment_dissatisfied'
      };
      return icons[rating] || 'sentiment_neutral';
    },

    getRatingClass(rating) {
      return `rating-${rating}`;
    },

    getRatingText(rating) {
      const texts = {
        'excelente': 'Excelente',
        'bom': 'Bom',
        'regular': 'Regular',
        'ruim': 'Ruim'
      };
      return texts[rating] || 'Não informado';
    },

    downloadAttachment() {
      if (this.conclusaoData?.anexo_base64) {
        // Criar um link temporário para download
        const link = document.createElement('a');
        link.href = this.conclusaoData.anexo_base64;
        link.download = this.conclusaoData.anexo_nome || 'anexo';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    },

    togglePreview() {
      this.showPreview = !this.showPreview;
    },

    isImageFile(mimeType) {
      if (!mimeType) return false;
      return mimeType.startsWith('image/');
    },

    getFileIcon(mimeType) {
      if (!mimeType) return 'description';
      
      if (mimeType.includes('pdf')) return 'picture_as_pdf';
      if (mimeType.startsWith('image/')) return 'image';
      if (mimeType.includes('word')) return 'description';
      if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return 'table_chart';
      if (mimeType.includes('text')) return 'text_snippet';
      
      return 'description';
    },

    getFileExtension(fileName) {
      if (!fileName) return '';
      const parts = fileName.split('.');
      return parts.length > 1 ? parts.pop().toUpperCase() : '';
    },

    getFileTypeDescription(mimeType) {
      if (!mimeType) return 'Arquivo';
      
      if (mimeType.includes('pdf')) return 'Documento PDF';
      if (mimeType.includes('jpeg') || mimeType.includes('jpg')) return 'Imagem JPEG';
      if (mimeType.includes('png')) return 'Imagem PNG';
      if (mimeType.includes('gif')) return 'Imagem GIF';
      if (mimeType.includes('word')) return 'Documento Word';
      if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return 'Planilha Excel';
      if (mimeType.includes('text')) return 'Arquivo de Texto';
      
      return 'Arquivo';
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  z-index: var(--z-index-modal);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: var(--spacing-md);
  box-sizing: border-box;
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: var(--spacing-md);
  width: var(--modal-width-lg);
  max-width: var(--modal-max-width);
  border-radius: 10px;
  position: relative;
  text-transform: none;
  font-size: 1.1rem;
  overflow-y: auto;
  max-height: var(--modal-max-height);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Cabeçalho do formulário */
.form-header {
  margin-bottom: var(--spacing-lg);
  border-bottom: 1px solid #333;
  padding-bottom: var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.form-header h2 {
  color: #27ae60;
  font-size: 1.4rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  background: transparent;
  border: 2px solid #27ae60;
  color: #27ae60;
  font-size: 1rem;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.close-btn:hover {
  background-color: #27ae60;
  color: #1f1f1f;
}

/* Resumo do Pedido */
.order-summary {
  background-color: #2a2a2a;
  color: white;
  padding: var(--spacing-lg);
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  margin-bottom: var(--spacing-lg);
  border: 1px solid #333;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.order-id {
  font-size: 1.5em;
  color: #27ae60; 
  font-weight: bold;
  text-align: left;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.status-badge.completed {
  background-color: #27ae60;
}

.order-title {
  font-size: 1.3rem;
  color: #f5f5f5; 
  text-align: center;
  width: 100%;
  margin: 5px 0 10px;
  border-bottom: 1px solid #444;
  padding-bottom: 8px;
}

.summary-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-sm);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: #dfe6e9;
  font-size: 0.9rem;
  margin: 8px 0;
}

.detail-item i {
  color: #27ae60;
  font-size: 16px;
}

/* Dados de Conclusão */
.conclusion-data {
  background-color: #2a2a2a;
  border-radius: 10px;
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  border: 1px solid #333;
}

.conclusion-data h3 {
  color: #27ae60;
  font-size: 1.2rem;
  margin: 0 0 var(--spacing-lg) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  border-bottom: 1px solid #444;
  padding-bottom: var(--spacing-sm);
}

.conclusion-section {
  margin-bottom: var(--spacing-lg);
}

.conclusion-section h4 {
  color: #ff6f61;
  font-size: 1rem;
  margin: 0 0 var(--spacing-md) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.info-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #f5f5f5;
}

.info-label {
  font-size: 0.9rem;
  color: #999;
}

/* Informações Financeiras */
.financial-summary {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.financial-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm);
  background-color: #333;
  border-radius: 5px;
}

.financial-item.total {
  background-color: #27ae60;
  color: white;
  font-weight: 600;
}

.financial-label {
  font-weight: 500;
}

.financial-value {
  font-weight: 600;
  color: #27ae60;
}

.financial-item.total .financial-value {
  color: white;
}

/* Tipos de Serviço */
.service-types {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.service-type {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: #333;
  border-radius: 5px;
  border: 1px solid #27ae60;
}

.service-type i {
  color: #27ae60;
}

/* Anexo */
.attachment-info {
  background-color: #333;
  border-radius: 8px;
  padding: var(--spacing-md);
  border: 1px solid #444;
}

.attachment-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.attachment-preview {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.attachment-thumbnail {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #555;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2a2a2a;
}

.attachment-thumbnail:hover {
  border-color: #27ae60;
  transform: scale(1.05);
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.file-icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  text-align: center;
}

.file-icon {
  color: #ff6f61;
  font-size: 2rem;
  margin-bottom: 4px;
}

.file-extension {
  font-size: 0.7rem;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
}

.attachment-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  min-width: 0;
}

.attachment-name {
  font-weight: 600;
  color: #f5f5f5;
  word-break: break-word;
  line-height: 1.3;
}

.attachment-size {
  font-size: 0.85rem;
  color: #999;
}

.attachment-type {
  font-size: 0.8rem;
  color: #27ae60;
  font-weight: 500;
}

.attachment-actions {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.preview-btn,
.download-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.9rem;
  flex: 1;
  justify-content: center;
  min-width: 100px;
}

.preview-btn {
  background-color: #27ae60;
}

.download-btn {
  background-color: #3498db;
}

.preview-btn:hover {
  background-color: #229954;
  transform: translateY(-2px);
}

.download-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

/* Preview expandido da imagem */
.image-preview {
  margin-top: var(--spacing-md);
  border: 1px solid #555;
  border-radius: 8px;
  overflow: hidden;
  background-color: #2a2a2a;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: #333;
  border-bottom: 1px solid #555;
}

.preview-title {
  font-weight: 600;
  color: #f5f5f5;
  font-size: 0.9rem;
  word-break: break-word;
}

.close-preview-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: var(--spacing-xs);
  border-radius: 3px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-preview-btn:hover {
  background-color: #444;
  color: #f5f5f5;
}

.preview-content {
  padding: var(--spacing-md);
  text-align: center;
  max-height: 400px;
  overflow: auto;
}

.preview-image {
  max-width: 100%;
  max-height: 350px;
  border-radius: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

/* Feedback */
.feedback-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.feedback-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.feedback-label {
  font-weight: 600;
  color: #ff6f61;
}

.feedback-text {
  background-color: #333;
  padding: var(--spacing-md);
  border-radius: 5px;
  margin: 0;
  line-height: 1.5;
}

.rating-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.rating-label {
  font-weight: 600;
  color: #ff6f61;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: #333;
  border-radius: 5px;
}

.rating-excelente {
  color: #27ae60;
}

.rating-bom {
  color: #3498db;
}

.rating-regular {
  color: #f39c12;
}

.rating-ruim {
  color: #e74c3c;
}

.rating-text {
  font-weight: 500;
}

/* Botões de Ação */
.form-actions {
  padding: var(--spacing-lg) 0 0 0;
  border-top: 1px solid #333;
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 2px solid transparent;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-button.close {
  background-color: #444;
  color: #f5f5f5;
  border-color: #555;
}

.action-button.close:hover {
  background-color: #555;
  transform: translateY(-2px);
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-overlay {
    padding: var(--spacing-sm);
    align-items: flex-start;
    padding-top: var(--spacing-md);
  }

  .order-form {
    width: var(--modal-width-md);
    max-height: var(--modal-max-height);
    padding: var(--spacing-md);
  }

  .form-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    text-align: center;
  }

  .form-header h2 {
    font-size: 1.2rem;
  }

  .close-btn {
    width: 100%;
    justify-content: center;
  }

  .summary-details {
    grid-template-columns: 1fr;
  }

  .financial-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }

  .service-types {
    flex-direction: column;
  }

  .attachment-preview {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
  }

  .attachment-thumbnail {
    width: 100px;
    height: 100px;
  }

  .attachment-details {
    text-align: center;
    width: 100%;
  }

  .attachment-actions {
    width: 100%;
    justify-content: center;
  }

  .preview-btn,
  .download-btn {
    min-width: 120px;
  }

  .rating-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: var(--spacing-xs);
  }

  .order-form {
    width: var(--modal-width-sm);
    padding: var(--spacing-sm);
  }

  .conclusion-data {
    padding: var(--spacing-md);
  }

  .form-header h2 {
    font-size: 1.1rem;
  }

  .order-id {
    font-size: 1.3em;
  }

  .order-title {
    font-size: 1.1rem;
  }

  .attachment-actions {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .preview-btn,
  .download-btn {
    width: 100%;
    min-width: auto;
  }

  .attachment-thumbnail {
    width: 80px;
    height: 80px;
  }

  .preview-content {
    padding: var(--spacing-sm);
    max-height: 250px;
  }

  .preview-image {
    max-height: 200px;
  }
}
</style> 