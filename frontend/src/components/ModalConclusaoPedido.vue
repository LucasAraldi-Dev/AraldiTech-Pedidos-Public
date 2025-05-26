<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="cancelConfirmation">
    <div class="order-form" @click.stop>
      <!-- Header do Modal -->
      <div class="form-header">
        <h2><i class="material-icons">check_circle</i> CONCLUIR PEDIDO</h2>
        <button class="close-btn" @click="cancelConfirmation">
          <i class="material-icons">close</i>
          FECHAR
        </button>
      </div>

      <!-- Resumo do Pedido -->
      <div class="order-summary" v-if="pedido">
        <div class="summary-header">
          <span class="order-id">#{{ pedido.id }}</span>
          <span class="urgency-badge" :class="getUrgencyClass(pedido.urgencia)" v-if="pedido.urgencia !== 'Padrão'">
            {{ pedido.urgencia }}
          </span>
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

      <!-- Formulário de Conclusão -->
      <div class="completion-form">
        <!-- Data de Conclusão -->
        <div class="form-section">
          <h4><i class="material-icons">event_available</i> Data de Conclusão <span class="required">*</span></h4>
          <div class="form-group">
            <label for="completionDate">Data de Conclusão:</label>
            <input 
              id="completionDate" 
              type="date" 
              v-model="formData.completionDate" 
              :min="minDate"
              required 
              class="form-input"
              :class="{ 'error': !formData.completionDate && showValidation }"
            />
            <p class="helper-text">
              <i class="material-icons">info</i>
              Selecione a data em que o pedido foi realmente concluído
            </p>
          </div>
        </div>

        <!-- Informações Financeiras -->
        <div class="form-section">
          <h4><i class="material-icons">attach_money</i> Informações Financeiras</h4>
          <div class="financial-grid">
            <div class="form-group">
              <label for="precoUnitario">Preço por Unidade - Itens (R$):</label>
              <input 
                id="precoUnitario" 
                type="number" 
                step="0.01" 
                min="0"
                v-model="formData.precoUnitario" 
                placeholder="0,00"
                class="form-input"
                @input="calculateTotal"
              />
            </div>
            <div class="form-group">
              <label for="valorTotal">Valor Total - Itens (R$):</label>
              <input 
                id="valorTotal" 
                type="number" 
                step="0.01" 
                min="0"
                v-model="formData.valorTotal" 
                placeholder="0,00"
                class="form-input"
                @input="calculateUnitPrice"
              />
            </div>
          </div>
          
          <!-- Campo de Mão de Obra (aparece apenas se selecionado) -->
          <div v-if="formData.temMaoDeObra" class="mao-obra-section">
            <div class="form-group">
              <label for="valorMaoDeObra">Valor da Mão de Obra (R$):</label>
              <input 
                id="valorMaoDeObra" 
                type="number" 
                step="0.01" 
                min="0"
                v-model="formData.valorMaoDeObra" 
                placeholder="0,00"
                class="form-input"
                @input="calculateTotalWithLabor"
              />
            </div>
            <div class="form-group">
              <label for="valorTotalComMaoDeObra">Valor Total (Itens + Mão de Obra) (R$):</label>
              <input 
                id="valorTotalComMaoDeObra" 
                type="number" 
                step="0.01" 
                min="0"
                v-model="formData.valorTotalComMaoDeObra" 
                placeholder="0,00"
                class="form-input"
                readonly
                style="background-color: #444; cursor: not-allowed;"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="fornecedor">Fornecedor:</label>
            <input 
              id="fornecedor" 
              type="text" 
              v-model="formData.fornecedor" 
              placeholder="Nome do fornecedor (opcional)"
              class="form-input"
            />
          </div>
        </div>

        <!-- Tipo de Serviço -->
        <div class="form-section">
          <h4><i class="material-icons">build</i> Tipo de Atendimento <span class="required">*</span></h4>
          <div class="service-options" :class="{ 'error': !formData.temMaterial && showValidation }">
            <label class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="formData.temMaoDeObra"
                class="checkbox-input"
                @change="onMaoDeObraChange"
              />
              <span class="checkbox-custom"></span>
              <span class="checkbox-text">
                <i class="material-icons">build</i>
                Envolveu mão de obra / serviço
              </span>
            </label>
            <label class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="formData.temMaterial"
                class="checkbox-input"
                @change="onMaterialChange"
              />
              <span class="checkbox-custom"></span>
              <span class="checkbox-text">
                <i class="material-icons">inventory</i>
                Envolveu material / produto
              </span>
            </label>
          </div>
        </div>

        <!-- Upload de Anexos -->
        <div class="form-section">
          <h4><i class="material-icons">attach_file</i> Anexar Comprovante</h4>
          <div class="upload-area" :class="{ 'drag-over': isDragOver, 'uploading': isUploadingFile }" 
               @drop="handleDrop" 
               @dragover.prevent="isDragOver = true" 
               @dragleave="isDragOver = false">
            
            <!-- Loading durante upload -->
            <div v-if="isUploadingFile" class="upload-loading">
              <LoadingIndicator 
                :overlay="false" 
                size="medium" 
                message="Fazendo upload do arquivo..." 
              />
            </div>
            
            <!-- Arquivo não selecionado -->
            <div v-else-if="!formData.anexo && !uploadSuccess" class="upload-placeholder">
              <i class="material-icons upload-icon">cloud_upload</i>
              <p>Arraste e solte a nota fiscal ou comprovante aqui</p>
              <p class="upload-subtitle">ou</p>
              <button type="button" class="upload-btn" @click="$refs.fileInput.click()">
                <i class="material-icons">folder_open</i>
                Selecionar Arquivo
              </button>
              <p class="upload-info">Formatos aceitos: PDF, JPG, PNG (máx. 5MB)</p>
            </div>
            
            <!-- Upload bem-sucedido -->
            <div v-else-if="uploadSuccess" class="upload-success">
              <i class="material-icons success-icon">check_circle</i>
              <p class="success-message">Upload realizado com sucesso!</p>
              <p class="success-subtitle">Arquivo pronto para envio</p>
              <div class="file-info-success">
                <span class="file-name">{{ formData.anexo.name || formData.anexo.file?.name }}</span>
                <span class="file-size">{{ formatFileSize(formData.anexo.size || formData.anexo.file?.size) }}</span>
              </div>
              <button type="button" class="change-file-btn" @click="resetUpload">
                <i class="material-icons">refresh</i>
                Alterar Arquivo
              </button>
            </div>
            
            <!-- Arquivo selecionado (fallback) -->
            <div v-else class="uploaded-file">
              <div class="file-info">
                <i class="material-icons file-icon">description</i>
                <div class="file-details">
                  <span class="file-name">{{ formData.anexo.name || formData.anexo.file?.name }}</span>
                  <span class="file-size">{{ formatFileSize(formData.anexo.size || formData.anexo.file?.size) }}</span>
                  <span class="file-status">Pronto para envio</span>
                </div>
                <button type="button" class="remove-file-btn" @click="removeFile">
                  <i class="material-icons">delete</i>
                </button>
              </div>
            </div>
            
            <input 
              ref="fileInput" 
              type="file" 
              accept=".pdf,.jpg,.jpeg,.png" 
              @change="handleFileSelect" 
              style="display: none"
            />
          </div>
        </div>

        <!-- Feedback/Comentários -->
        <div class="form-section">
          <h4><i class="material-icons">feedback</i> Feedback e Observações</h4>
          <div class="form-group">
            <label for="feedback">Comentários sobre a conclusão:</label>
            <textarea 
              id="feedback" 
              v-model="formData.feedback" 
              placeholder="Ex: Pedido atendido rapidamente, boa qualidade do produto... (opcional)"
              rows="4"
              class="form-textarea"
              maxlength="500"
            ></textarea>
            <div class="char-counter">
              {{ formData.feedback.length }}/500 caracteres
            </div>
          </div>
          
          <!-- Avaliação Rápida -->
          <div class="quick-rating">
            <label>Avaliação geral: <span class="required">*</span></label>
            <div class="rating-options" :class="{ 'error': !formData.avaliacao && showValidation }">
              <button 
                type="button" 
                v-for="rating in ratingOptions" 
                :key="rating.value"
                class="rating-btn" 
                :class="{ 'active': formData.avaliacao === rating.value }"
                @click="formData.avaliacao = rating.value"
              >
                <i class="material-icons">{{ rating.icon }}</i>
                <span>{{ rating.label }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Botões de Ação -->
      <div class="form-actions">
        <button class="action-button close" @click="cancelConfirmation">
          <i class="material-icons">cancel</i>
          CANCELAR
        </button>
        <button class="action-button confirm" @click="confirmCompletion" :disabled="isSubmitting">
          <i class="material-icons">{{ isSubmitting ? 'hourglass_empty' : 'check_circle' }}</i>
          {{ isSubmitting ? 'PROCESSANDO...' : 'CONCLUIR PEDIDO' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

export default {
  name: 'ModalConclusaoPedido',
  components: {
    LoadingIndicator
  },
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
  emits: ['close', 'completed'],
  data() {
    return {
      toast: useToast(),
      isSubmitting: false,
      isDragOver: false,
      minDate: null,
      showValidation: false,
      isUploadingFile: false,
      uploadSuccess: false,
      formData: {
        completionDate: null,
        precoUnitario: 0,
        valorTotal: 0,
        valorMaoDeObra: 0,
        valorTotalComMaoDeObra: 0,
        fornecedor: '',
        temMaoDeObra: false,
        temMaterial: false,
        anexo: null,
        feedback: '',
        avaliacao: null
      },
      ratingOptions: [
        { value: 'excelente', label: 'Excelente', icon: 'sentiment_very_satisfied' },
        { value: 'bom', label: 'Bom', icon: 'sentiment_satisfied' },
        { value: 'regular', label: 'Regular', icon: 'sentiment_neutral' },
        { value: 'ruim', label: 'Ruim', icon: 'sentiment_dissatisfied' }
      ]
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal && this.pedido) {
        this.initializeForm();
      }
    },
    pedido(newVal) {
      if (newVal && this.isOpen) {
        this.initializeForm();
      }
    }
  },
  methods: {
    initializeForm() {
      // Configurar data mínima
      if (this.pedido?.deliveryDate) {
        const dataPedido = new Date(this.pedido.deliveryDate);
        console.log('[DEBUG] Configurando data mínima:');
        console.log('- Data do pedido (original):', this.pedido.deliveryDate);
        console.log('- Data do pedido (objeto Date):', dataPedido);
        
        if (!isNaN(dataPedido.getTime())) {
          // Usar a data do pedido (apenas o dia) como data mínima
          this.minDate = dataPedido.toISOString().split('T')[0];
          console.log('- Data mínima configurada:', this.minDate);
        } else {
          console.log('- Data do pedido inválida, usando data atual');
          this.minDate = new Date().toISOString().split('T')[0];
        }
      } else {
        console.log('- Pedido sem data, usando data atual como mínima');
        this.minDate = new Date().toISOString().split('T')[0];
      }

      // Inicializar data de conclusão com hoje
      this.formData.completionDate = new Date().toISOString().split('T')[0];
      console.log('[DEBUG] Data de conclusão inicializada:', this.formData.completionDate);
      
      // Resetar outros campos
      this.formData.precoUnitario = 0;
      this.formData.valorTotal = 0;
      this.formData.valorMaoDeObra = 0;
      this.formData.valorTotalComMaoDeObra = 0;
      this.formData.fornecedor = '';
      this.formData.temMaoDeObra = false;
      this.formData.temMaterial = true; // Material sempre selecionado por padrão
      this.formData.anexo = null;
      this.formData.feedback = '';
      this.formData.avaliacao = null;

      // Resetar estados de upload
      this.isUploadingFile = false;
      this.uploadSuccess = false;
      this.showValidation = false;

      // Impedir scroll do body
      document.body.style.overflow = 'hidden';
    },

    calculateTotal() {
      if (this.formData.precoUnitario && this.pedido?.quantidade) {
        this.formData.valorTotal = (parseFloat(this.formData.precoUnitario) * this.pedido.quantidade).toFixed(2);
        this.calculateTotalWithLabor();
      }
    },

    calculateUnitPrice() {
      if (this.formData.valorTotal && this.pedido?.quantidade) {
        this.formData.precoUnitario = (parseFloat(this.formData.valorTotal) / this.pedido.quantidade).toFixed(2);
        this.calculateTotalWithLabor();
      }
    },

    calculateTotalWithLabor() {
      const valorItens = parseFloat(this.formData.valorTotal) || 0;
      const valorMaoDeObra = parseFloat(this.formData.valorMaoDeObra) || 0;
      this.formData.valorTotalComMaoDeObra = (valorItens + valorMaoDeObra).toFixed(2);
    },

    onMaoDeObraChange() {
      if (!this.formData.temMaoDeObra) {
        this.formData.valorMaoDeObra = 0;
        this.formData.valorTotalComMaoDeObra = 0;
        this.calculateTotalWithLabor();
      }
    },

    onMaterialChange() {
      // Manter pelo menos material selecionado
      if (!this.formData.temMaterial && !this.formData.temMaoDeObra) {
        this.formData.temMaterial = true;
      }
    },

    handleFileSelect(event) {
      const file = event.target.files[0];
      this.processFile(file);
    },

    handleDrop(event) {
      event.preventDefault();
      this.isDragOver = false;
      const file = event.dataTransfer.files[0];
      this.processFile(file);
    },

    async processFile(file) {
      if (!file) return;

      // Validar tipo de arquivo
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
      if (!allowedTypes.includes(file.type)) {
        this.toast.error('Formato de arquivo não suportado. Use PDF, JPG ou PNG.');
        return;
      }

      // Validar tamanho (5MB)
      if (file.size > 5 * 1024 * 1024) {
        this.toast.error('Arquivo muito grande. Tamanho máximo: 5MB.');
        return;
      }

      // Converter para Base64 com loading
      this.isUploadingFile = true;
      this.uploadSuccess = false;

      try {
        // Converter arquivo para Base64
        const base64 = await this.convertFileToBase64(file);
        
        // Armazenar dados do arquivo
        this.formData.anexo = {
          file: file,
          base64: base64,
          name: file.name,
          size: file.size,
          type: file.type
        };
        
        this.uploadSuccess = true;
        this.toast.success('Arquivo processado com sucesso! Pronto para envio.');
        
      } catch (error) {
        console.error('Erro ao processar arquivo:', error);
        this.toast.error('Erro ao processar arquivo. Tente novamente.');
        this.uploadSuccess = false;
      } finally {
        this.isUploadingFile = false;
      }
    },

    convertFileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
      });
    },

    removeFile() {
      this.formData.anexo = null;
      this.uploadSuccess = false;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },

    resetUpload() {
      this.formData.anexo = null;
      this.uploadSuccess = false;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    getUrgencyClass(urgencia) {
      switch(urgencia) {
        case 'Crítico': return 'urgency-critical';
        case 'Urgente': return 'urgency-urgent';
        default: return 'urgency-normal';
      }
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
          year: 'numeric'
        });
      } catch (error) {
        return 'Erro de formato';
      }
    },

    async confirmCompletion() {
      this.showValidation = true;
      if (!this.validateForm()) return;

      this.isSubmitting = true;

      try {
        // Obter dados do usuário
        const userStr = localStorage.getItem("user");
        let userId = null;
        let userName = null;
        let userType = null;

        if (userStr) {
          const userObj = JSON.parse(userStr);
          userId = userObj.id;
          userName = userObj.nome || userObj.username;
          userType = userObj.tipo_usuario;
        }

        // Verificar permissões
        const isAdminOrGestor = userType === "admin" || userType === "gestor";
        const isCreator = this.pedido.usuario_id === userId || this.pedido.usuario_nome === userName;

        if (!isAdminOrGestor && !isCreator) {
          this.toast.error("Você não tem permissão para concluir este pedido.");
          return;
        }

        // Preparar dados para envio
        const updateData = {
          id: this.pedido.id,
          descricao: this.pedido.descricao,
          quantidade: this.pedido.quantidade,
          categoria: this.pedido.categoria,
          urgencia: this.pedido.urgencia,
          deliveryDate: this.pedido.deliveryDate,
          setor: this.pedido.setor,
          status: "Concluído",
          sender: this.pedido.sender || this.pedido.usuario_nome,
          observacao: this.pedido.observacao || "",
          completionDate: this.formData.completionDate,
          usuario_nome: userName,
          usuario_id: userId,
          // Dados de conclusão
          conclusao_dados: {
            preco_unitario: parseFloat(this.formData.precoUnitario) || 0,
            valor_total: parseFloat(this.formData.valorTotal) || 0,
            valor_mao_de_obra: parseFloat(this.formData.valorMaoDeObra) || 0,
            valor_total_com_mao_de_obra: parseFloat(this.formData.valorTotalComMaoDeObra) || 0,
            fornecedor: this.formData.fornecedor,
            tem_mao_de_obra: this.formData.temMaoDeObra,
            tem_material: this.formData.temMaterial,
            feedback: this.formData.feedback,
            avaliacao: this.formData.avaliacao,
            data_conclusao: new Date().toISOString(),
            usuario_conclusao: userName
          },
          historico: [{
            campo_alterado: "status",
            valor_anterior: this.pedido.status || "Pendente",
            valor_novo: "Concluído",
            data_edicao: new Date().toISOString(),
            usuario_nome: userName,
            pedido_id: this.pedido.id
          }]
        };

        // Anexar arquivo Base64 se existir
        if (this.formData.anexo && this.formData.anexo.base64) {
          updateData.conclusao_dados.anexo_base64 = this.formData.anexo.base64;
          updateData.conclusao_dados.anexo_nome = this.formData.anexo.name;
          updateData.conclusao_dados.anexo_tipo = this.formData.anexo.type;
          updateData.conclusao_dados.anexo_tamanho = this.formData.anexo.size;
          console.log("Anexo Base64 adicionado aos dados de conclusão");
        }

        // Atualizar pedido
        const response = await axios.put(
          `${process.env.VUE_APP_API_URL}/pedidos/${this.pedido.id}/com-historico`,
          updateData,
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
          }
        );

        this.toast.success("Pedido concluído com sucesso!");
        this.$emit('completed', response.data);
        this.cancelConfirmation();

      } catch (error) {
        console.error("Erro ao concluir pedido:", error);
        
        let errorMessage = "Erro ao concluir pedido. Tente novamente.";
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
        
        this.toast.error(errorMessage);
      } finally {
        this.isSubmitting = false;
      }
    },

    validateForm() {
      const errors = [];

      // Validação da data de conclusão
      if (!this.formData.completionDate) {
        errors.push("Data de conclusão é obrigatória.");
      } else {
        // Corrigir o problema de fuso horário ao criar a data de conclusão
        const [year, month, day] = this.formData.completionDate.split('-').map(Number);
        const completionDate = new Date(year, month - 1, day); // month - 1 porque Date usa 0-11 para meses
        
        const today = new Date();
        today.setHours(23, 59, 59, 999); // Fim do dia atual
        
        if (completionDate > today) {
          errors.push("Data de conclusão não pode ser no futuro.");
        }
        
        if (this.pedido?.deliveryDate) {
          const orderDate = new Date(this.pedido.deliveryDate);
          
          // Debug: Log das datas para análise
          console.log('[DEBUG] Validação de data:');
          console.log('- Data do pedido (original):', this.pedido.deliveryDate);
          console.log('- Data do pedido (objeto Date):', orderDate);
          console.log('- Data de conclusão selecionada:', this.formData.completionDate);
          console.log('- Data de conclusão (objeto Date corrigido):', completionDate);
          
          // Normalizar as datas para comparar apenas o dia (sem horário)
          const completionDateOnly = new Date(completionDate.getFullYear(), completionDate.getMonth(), completionDate.getDate());
          const orderDateOnly = new Date(orderDate.getFullYear(), orderDate.getMonth(), orderDate.getDate());
          
          console.log('- Data do pedido (normalizada):', orderDateOnly);
          console.log('- Data de conclusão (normalizada):', completionDateOnly);
          console.log('- Comparação (conclusão < pedido):', completionDateOnly < orderDateOnly);
          
          // Permitir conclusão no mesmo dia ou depois
          if (completionDateOnly < orderDateOnly) {
            const orderDateFormatted = orderDate.toLocaleDateString('pt-BR');
            const completionDateFormatted = completionDate.toLocaleDateString('pt-BR');
            errors.push(`Data de conclusão (${completionDateFormatted}) não pode ser anterior à data do pedido (${orderDateFormatted}).`);
          }
        }
      }

      // Validação de valores financeiros
      if (this.formData.valorTotal < 0 || this.formData.precoUnitario < 0) {
        errors.push("Valores financeiros não podem ser negativos.");
      }

      // Validação de tipo de atendimento (material é obrigatório)
      if (!this.formData.temMaterial) {
        errors.push("É obrigatório selecionar 'Material/produto'.");
      }

      // Validação de avaliação
      if (!this.formData.avaliacao) {
        errors.push("Avaliação geral é obrigatória.");
      }

      // Exibir erros
      if (errors.length > 0) {
        this.toast.error(errors.join(" "));
        return false;
      }

      return true;
    },

    cancelConfirmation() {
      this.isSubmitting = false;
      document.body.style.overflow = '';
      this.$emit('close');
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

/* Título do formulário */
.form-header h2 {
  color: #ff6f61;
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
  border: 2px solid #ff6f61;
  color: #ff6f61;
  font-size: 1rem;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.close-btn:hover {
  background-color: #ff6f61;
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
  color: #ff6f61; 
  font-weight: bold;
  text-align: left;
}

.urgency-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.urgency-critical {
  background-color: #e74c3c;
}

.urgency-urgent {
  background-color: #f39c12;
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
  color: #ff6f61;
  font-size: 16px;
}

/* Formulário */
.completion-form {
  padding: 0;
}

.form-section {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  border: 1px solid #333;
}

.form-section h4 {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin: 0 0 var(--spacing-md) 0;
  color: #ff6f61;
  font-size: 1.1rem;
  padding-bottom: var(--spacing-xs);
  border-bottom: 1px solid #444;
}

.form-group {
  margin-bottom: var(--spacing-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 600;
  color: #f5f5f5;
  font-size: 0.95rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid #444;
  border-radius: 5px;
  font-size: 1rem;
  background-color: #333;
  color: #f5f5f5;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #ff6f61;
  background-color: #3a3a3a;
}

.financial-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.mao-obra-section {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md);
  background-color: rgba(255, 111, 97, 0.1);
  border: 1px solid #ff6f61;
  border-radius: 8px;
}

.mao-obra-section .form-group {
  margin-bottom: var(--spacing-md);
}

.helper-text {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-xs);
  font-size: 0.85rem;
  color: #999;
}

/* Opções de Serviço */
.service-options {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  padding: var(--spacing-sm);
  border: 2px solid #444;
  border-radius: 5px;
  transition: all 0.2s ease;
  background-color: #333;
}

.checkbox-label:hover {
  border-color: #ff6f61;
  background-color: #3a3a3a;
}

.checkbox-input {
  display: none;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #666;
  border-radius: 4px;
  position: relative;
  transition: all 0.2s ease;
  background-color: #444;
}

.checkbox-input:checked + .checkbox-custom {
  background-color: #ff6f61;
  border-color: #ff6f61;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 12px;
}

.checkbox-text {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-weight: 500;
  color: #f5f5f5;
}

/* Upload de Arquivos */
.upload-area {
  border: 2px dashed #666;
  border-radius: 8px;
  padding: var(--spacing-xl);
  text-align: center;
  transition: all 0.2s ease;
  cursor: pointer;
  background-color: #333;
  position: relative;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area.drag-over {
  border-color: #ff6f61;
  background-color: rgba(255, 111, 97, 0.1);
}

.upload-area.uploading {
  border-color: #ff6f61;
  background-color: rgba(255, 111, 97, 0.05);
  cursor: not-allowed;
}



.upload-placeholder {
  color: #ccc;
  width: 100%;
}

/* Estados de Upload */
.upload-loading {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
}

.upload-success {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  color: #27ae60;
}

.success-icon {
  font-size: 3rem;
  color: #27ae60;
  margin-bottom: var(--spacing-md);
}

.success-message {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: #27ae60;
}

.success-subtitle {
  font-size: 0.9rem;
  color: #999;
  margin-bottom: var(--spacing-md);
}

.file-info-success {
  text-align: center;
  margin-bottom: var(--spacing-md);
}

.file-info-success .file-name {
  display: block;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: var(--spacing-xs);
}

.file-info-success .file-size {
  display: block;
  font-size: 0.85rem;
  color: #999;
}

.change-file-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 5px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.2s ease;
  font-weight: 500;
}

.change-file-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}



.upload-icon {
  font-size: 3rem;
  color: #ff6f61;
  margin-bottom: var(--spacing-md);
}

.upload-subtitle {
  color: #999;
  margin: var(--spacing-sm) 0;
}

.upload-btn {
  background-color: #ff6f61;
  color: white;
  border: none;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: 5px;
  cursor: pointer;
  margin: var(--spacing-md) 0;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.2s ease;
  font-weight: 600;
}

.upload-btn:hover {
  background-color: #e05545;
  transform: translateY(-2px);
}

.upload-info {
  font-size: 0.85rem;
  color: #999;
  margin-top: var(--spacing-xs);
}

.uploaded-file {
  background-color: #3a3a3a;
  border-radius: 6px;
  padding: var(--spacing-md);
  border: 1px solid #555;
}

.file-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.file-icon {
  color: #ff6f61;
  font-size: 2rem;
}

.file-details {
  flex: 1;
  text-align: left;
}

.file-name {
  display: block;
  font-weight: 600;
  color: #f5f5f5;
}

.file-size {
  display: block;
  font-size: 0.85rem;
  color: #999;
}

.file-status {
  display: block;
  font-size: 0.8rem;
  color: #27ae60;
  font-weight: 500;
  margin-top: 2px;
}

.remove-file-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: var(--spacing-xs);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-file-btn:hover {
  background-color: #c0392b;
  transform: scale(1.1);
}

/* Textarea */
.form-textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.char-counter {
  text-align: right;
  font-size: 0.85rem;
  color: #999;
  margin-top: var(--spacing-xs);
}

/* Avaliação */
.quick-rating {
  margin-top: var(--spacing-md);
}

.quick-rating label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 600;
  color: #f5f5f5;
  font-size: 0.95rem;
}

.rating-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--spacing-xs);
}

.rating-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border: 2px solid #444;
  border-radius: 5px;
  background-color: #333;
  color: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  font-weight: 500;
}

.rating-btn:hover {
  border-color: #ff6f61;
  background-color: #3a3a3a;
}

.rating-btn.active {
  border-color: #ff6f61;
  background-color: #ff6f61;
  color: white;
}

/* Botões de Ação */
.form-actions {
  padding: var(--spacing-lg) 0 0 0;
  border-top: 1px solid #333;
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
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

.action-button.confirm {
  background-color: #ff6f61;
  color: white;
  border-color: #ff6f61;
}

.action-button.confirm:hover:not(:disabled) {
  background-color: #e05545;
  transform: translateY(-2px);
}

.action-button.confirm:disabled {
  background-color: #666;
  border-color: #666;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Campos obrigatórios e validação */
.required {
  color: #ff6f61;
  font-weight: bold;
}

.form-input.error,
.form-textarea.error {
  border-color: #e74c3c;
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
}

.service-options.error {
  border: 2px solid #e74c3c;
  border-radius: 5px;
  background-color: rgba(231, 76, 60, 0.1);
}

.rating-options.error {
  border: 2px solid #e74c3c;
  border-radius: 5px;
  background-color: rgba(231, 76, 60, 0.1);
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

  .financial-grid {
    grid-template-columns: 1fr;
  }

  .rating-options {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-actions {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .action-button {
    width: 100%;
    justify-content: center;
    padding: var(--spacing-md);
  }

  .upload-area {
    padding: var(--spacing-lg);
  }

  .upload-icon {
    font-size: 2.5rem;
  }
}

/* Dispositivos móveis muito pequenos */
@media (max-width: 480px) {
  .modal-overlay {
    padding: var(--spacing-xs);
  }

  .order-form {
    width: var(--modal-width-sm);
    padding: var(--spacing-sm);
  }

  .form-section {
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

  .detail-item {
    font-size: 0.85rem;
  }

  .rating-options {
    grid-template-columns: 1fr;
  }

  .upload-area {
    padding: var(--spacing-md);
  }

  .upload-icon {
    font-size: 2rem;
  }
}

/* Ajustes para notebooks pequenos (13-14 polegadas) */
@media screen and (max-width: 1366px) and (max-height: 768px) {
  .order-form {
    width: var(--modal-width-md);
    max-height: 85vh;
    padding: var(--spacing-md);
  }

  .form-section {
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
  }

  .upload-area {
    padding: var(--spacing-lg);
  }
}

/* Ajustes para telas muito pequenas onde a rolagem pode ser necessária */
@media (max-height: 640px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: var(--spacing-sm);
    padding-bottom: var(--spacing-sm);
  }

  .order-form {
    margin-top: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
    max-height: 95vh;
  }
}

/* Ajustes para telas com zoom */
@media screen and (min-resolution: 1.25dppx) {
  .order-form {
    max-height: 88vh;
  }

  .form-section {
    padding: var(--spacing-md);
  }
}
</style> 