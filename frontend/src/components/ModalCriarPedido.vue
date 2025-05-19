<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleOverlayClick">
    <div class="order-form" @click.stop>
      <button type="button" class="close-modal-btn" @click="closeForm">
        <i class="material-icons">close</i>
      </button>
      <div class="form-header">
        <h2>ADICIONAR PEDIDO</h2>
        <div class="user-info" v-if="userName">
          <span class="user-label">Criado por:</span>
          <span class="user-name">{{ userName }}</span>
        </div>
      </div>

      <!-- Formulário de Criação de Pedido -->
      <form v-show="!successMessage" @submit.prevent="handleCreateOrder">
        <div class="form-grid">
          <div class="form-group full-width">
            <label for="orderDescription">
              <i class="material-icons">description</i>
              DESCRIÇÃO DO PEDIDO
            </label>
            <textarea
              id="orderDescription"
              v-model="orderDescription"
              placeholder="DESCRIÇÃO DO PEDIDO"
              required
              @blur="validateDescription"
              :class="{ 'invalid': validationErrors.description }"
            ></textarea>
            <span class="error-message" v-if="validationErrors.description">{{ validationErrors.description }}</span>
          </div>

          <div class="form-group">
            <label for="orderQuantity">
              <i class="material-icons">format_list_numbered</i>
              QUANTIDADE
            </label>
            <div class="quantity-input-container">
              <button type="button" class="quantity-btn" @click="decrementQuantity" :disabled="orderQuantity <= 1">
                <i class="material-icons">remove</i>
              </button>
              <input 
                id="orderQuantity" 
                type="number" 
                v-model.number="orderQuantity" 
                min="1" 
                @input="validateQuantity"
                @blur="validateQuantity"
                required 
                :class="{ 'invalid': validationErrors.quantity }"
              />
              <button type="button" class="quantity-btn" @click="incrementQuantity">
                <i class="material-icons">add</i>
              </button>
            </div>
            <span class="error-message" v-if="validationErrors.quantity">{{ validationErrors.quantity }}</span>
            <div class="input-note" v-else>
              Quantidade mínima: 1
            </div>
          </div>

          <div class="form-group">
            <label for="orderCategory">
              <i class="material-icons">category</i>
              CATEGORIA
            </label>
            <select id="orderCategory" v-model="orderCategory" required>
              <option value="" disabled selected>SELECIONE A CATEGORIA</option>
              <option value="Matérias-primas">Matérias-primas</option>
              <option value="Equipamentos e Máquinas">Equipamentos e Máquinas</option>
              <option value="Peças de Reposição">Peças de Reposição</option>
              <option value="Serviços">Serviços</option>
              <option value="Mercadorias diversas">Mercadorias diversas</option>
            </select>
          </div>

          <div class="form-group">
            <label for="orderUrgency">
              <i class="material-icons">priority_high</i>
              URGÊNCIA
            </label>
            <select id="orderUrgency" v-model="orderUrgency" required>
              <option value="Padrão">Padrão (Sem prioridade)</option>
              <option value="Urgente">Urgente (Para o mesmo dia)</option>
              <option value="Crítico">Crítico (Fábrica parada)</option>
            </select>
            <TooltipInfo 
              title="Informações de Urgência" 
              position="left"
              :maxWidth="300"
            >
              <div class="urgency-legend">
                <div class="urgency-item">
                  <span class="urgency-icon padrão">●</span>
                  <span class="urgency-desc">Padrão: Para pedidos sem prioridade, prazo de até 7 dias</span>
                </div>
                <div class="urgency-item">
                  <span class="urgency-icon urgente">●</span>
                  <span class="urgency-desc">Urgente: Necessário para o mesmo dia</span>
                </div>
                <div class="urgency-item">
                  <span class="urgency-icon critico">●</span>
                  <span class="urgency-desc">Crítico: Emergência, processo de produção interrompido</span>
                </div>
              </div>
            </TooltipInfo>
          </div>

          <div class="form-group">
            <label for="orderDeliveryDate">
              <i class="material-icons">event</i>
              DATA DO PEDIDO
            </label>
            <div class="date-input-container">
              <input 
                id="orderDeliveryDate" 
                type="date" 
                v-model="orderDeliveryDate" 
                :disabled="!isAdmin"
                required 
                class="date-picker"
              />
              <i class="material-icons date-icon">calendar_today</i>
            </div>
            <div class="input-note">
              {{ isAdmin ? 'Como administrador, você pode alterar a data do pedido' : 'A data do pedido é preenchida automaticamente' }}
            </div>
          </div>

          <div class="form-group full-width">
            <label for="orderNotes">
              <i class="material-icons">notes</i>
              OBSERVAÇÃO
            </label>
            <textarea
              id="orderNotes"
              v-model="orderNotes"
              placeholder="OBSERVAÇÃO"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="orderFile">
              <i class="material-icons">attach_file</i>
              ANEXO (IMAGEM/ARQUIVO)
            </label>
            <div class="file-input-container">
              <input id="orderFile" type="file" @change="handleFileUpload" class="file-input" />
              <div class="custom-file-button">
                <i class="material-icons">cloud_upload</i>
                <span>{{ orderFile ? 'Arquivo selecionado' : 'Escolher arquivo' }}</span>
              </div>
              <div class="file-info" v-if="orderFile">
                <div class="file-name">
                  <i class="material-icons">insert_drive_file</i>
                  <span>{{ orderFile.name }}</span>
                </div>
                <button type="button" class="remove-file" @click="removeFile">
                  <i class="material-icons">close</i>
                </button>
              </div>
              <div class="file-input-wrapper" v-if="!orderFile">
                <div class="input-note">
                  Clique para anexar um arquivo de referência (opcional)
                </div>
                <TooltipInfo 
                  title="Sobre anexos" 
                  position="right"
                  :maxWidth="300"
                >
                  <div class="file-info-content">
                    <p>Você pode anexar arquivos como:</p>
                    <ul>
                      <li>Imagens (JPG, PNG, GIF)</li>
                      <li>Documentos (PDF, DOC, XLS)</li>
                      <li>Outros arquivos de referência</li>
                    </ul>
                    <p>Tamanho máximo: 10MB</p>
                  </div>
                </TooltipInfo>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label for="orderSender">
              <i class="material-icons">person</i>
              RESPONSÁVEL PELA COMPRA
            </label>
            <input id="orderSender" type="text" v-model="orderSender" required />
          </div>

          <div class="form-group">
            <label for="orderSenderSector">
              <i class="material-icons">business</i>
              SETOR DO RESPONSÁVEL
            </label>
            <select 
              id="orderSenderSector" 
              v-model="orderSenderSector" 
              :disabled="!isAdminOrGestor"
              required 
            >
              <option value="Escritório">Escritório</option>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="CPO">CPO</option>
              <option value="Granjas">Granjas</option>
              <option value="Abatedouro">Abatedouro</option>
              <option value="Transporte">Transporte</option>
              <option value="Incubatório">Incubatório</option>
              <option value="Favorito">Favorito</option>
            </select>
            <div class="input-note" v-if="!isAdminOrGestor">
              O setor é definido automaticamente com base no seu perfil
            </div>
          </div>

          <div class="form-group options-group full-width">
            <label class="toggle-container">
              <span class="toggle-label">
                <i class="material-icons">repeat</i>
                Criar múltiplos pedidos em sequência
              </span>
              <div class="toggle-switch">
                <input type="checkbox" v-model="createMultiple" />
                <span class="slider"></span>
              </div>
            </label>
          </div>
        </div>

        <div class="form-buttons">
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            <LoadingIndicator v-if="isSubmitting" size="small" />
            <template v-else>
              <i class="material-icons">send</i>
              ENVIAR PEDIDO
            </template>
          </button>
          <button type="button" class="close-btn" @click="closeForm" :disabled="isSubmitting">
            <i class="material-icons">close</i>
            CANCELAR
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
// Usando axiosService para requisições HTTP
import axiosService from '../api/axiosService';
import { useToast } from 'vue-toastification';  // Importando Vue Toastification
import { validateQuantity, validateText, validateDate } from '../utils/validationService';
import { ensureCsrfToken } from '../utils/securityService';
import LoadingIndicator from './ui/LoadingIndicator.vue';
import TooltipInfo from './ui/TooltipInfo.vue';

export default {
  components: {
    LoadingIndicator,
    TooltipInfo
  },
  props: {
    isOpen: Boolean,
    onClose: Function,
  },
  data() {
    return {
      orderDescription: "",
      orderQuantity: 1,
      orderCategory: "", 
      orderUrgency: "Padrão", 
      orderDeliveryDate: new Date().toISOString().split('T')[0],
      orderNotes: "",
      orderSender: "",
      orderSenderSector: "",
      orderFile: null,
      orderFileBase64: "",
      userEmail: null,
      userName: null,
      userType: null,
      userSector: null,
      token: null,
      createMultiple: false,
      isUrgencyTooltipVisible: false,
      isFileTooltipVisible: false,
      validationErrors: {
        description: "",
        quantity: "",
        category: "",
        date: "",
        sender: ""
      },
      isSubmitting: false,
      successMessage: "",
      isMobile: false,
      tooltipStyle: {
        top: '25px',
        left: '0'
      },
      fileTooltipStyle: {
        top: '25px',
        left: '0'
      }
    };
  },
  computed: {
    isAdminOrGestor() {
      return this.userType === "admin" || this.userType === "gestor";
    },
    isAdmin() {
      return this.userType === "admin";
    }
  },
  mounted() {
    // Obter informações do usuário do localStorage
    const userStr = localStorage.getItem("user");
    if (userStr) {
      try {
        const userObj = JSON.parse(userStr);
        this.userName = userObj.nome;
        this.userType = userObj.tipo_usuario;
        this.userSector = userObj.setor;
        this.orderSenderSector = userObj.setor || ""; // Preenche automaticamente com o setor do usuário
        console.log("Dados do usuário carregados:", this.userName, this.userType, this.userSector);
      } catch (e) {
        console.error("Erro ao parsear dados do usuário:", e);
      }
    }
    
    // Fallback para outros campos caso precise
    if (!this.userName) {
      this.userName = localStorage.getItem("user_name");
    }
    
    this.userEmail = localStorage.getItem("user_email"); 
    this.token = localStorage.getItem("access_token");
    
    // Verificar autenticação ao montar o componente
    if (!this.token) {
      console.error("Usuário não autenticado.");
      this.$emit("close");
      const toast = useToast();
      toast.error("É necessário estar autenticado para criar pedidos.");
    } else {
      console.log("Usuário autenticado:", this.userName);
    }

    // Verificar se o dispositivo é móvel
    this.isMobile = window.innerWidth < 768;

    // Monitorar scroll para adicionar efeito sticky aos botões
    this.$nextTick(() => {
      const formEl = this.$el.querySelector('.order-form');
      const buttonsEl = this.$el.querySelector('.form-buttons');
      
      if (formEl && buttonsEl) {
        this.handleScroll = () => {
          // Verifica se estamos próximos do final do formulário
          const isNearBottom = formEl.scrollHeight - formEl.scrollTop - formEl.clientHeight < 50;
          
          if (isNearBottom) {
            buttonsEl.classList.remove('sticky');
          } else {
            buttonsEl.classList.add('sticky');
          }
        };
        
        formEl.addEventListener('scroll', this.handleScroll);
      }
    });
  },
  beforeUnmount() {
    // Limpar os event listeners quando o componente for desmontado
    const formEl = this.$el.querySelector('.order-form');
    if (formEl && this.handleScroll) {
      formEl.removeEventListener('scroll', this.handleScroll);
    }
  },
  methods: {
    async handleCreateOrder() {
      const toast = useToast();

      // Validar se usuário está logado
      const token = localStorage.getItem("access_token");
      if (!token) {
        toast.error("É necessário estar autenticado para criar pedidos.");
        return;
      }
      
      // Garantir que temos um token CSRF válido
      try {
        await ensureCsrfToken();
      } catch (error) {
        console.error("Erro ao obter token CSRF:", error);
        toast.error("Erro de segurança. Tente fazer login novamente.");
        return;
      }
      
      // Validar formulário completo
      if (!this.validateForm()) {
        // Exibir mensagens de erro para cada campo inválido
        if (this.validationErrors.description) {
          toast.error(this.validationErrors.description);
        }
        if (this.validationErrors.quantity) {
          toast.error(this.validationErrors.quantity);
        }
        if (this.validationErrors.category) {
          toast.error(this.validationErrors.category);
        }
        if (this.validationErrors.date) {
          toast.error(this.validationErrors.date);
        }
        if (this.validationErrors.sender) {
          toast.error(this.validationErrors.sender);
        }
        return;
      }

      if (!this.orderFileBase64 && this.orderFile) {
        toast.warning("Aguarde o processamento do arquivo antes de enviar o pedido.");
        return;
      }

      // Ativar indicador de carregamento
      this.isSubmitting = true;

      // Usar o nome do usuário e setor do token
      this.token = localStorage.getItem("access_token");
      
      if (!this.userName) {
        const userStr = localStorage.getItem("user");
        if (userStr) {
          try {
            const userObj = JSON.parse(userStr);
            this.userName = userObj.nome;
            this.userSector = userObj.setor;
          } catch (e) {
            console.error("Erro ao parsear dados do usuário:", e);
          }
        }
      }

      // Preencher o campo de responsável automaticamente com o nome do usuário logado
      if (!this.orderSender) {
        this.orderSender = this.userName || "Usuário do sistema";
      }

      // Capturar informações adicionais para auditoria
      let userAgent = navigator.userAgent;
      let browserInfo = {
        userAgent: userAgent,
        platform: navigator.platform,
        language: navigator.language,
        screenWidth: window.screen.width,
        screenHeight: window.screen.height
      };

      // Data e hora exata da criação
      const creationDateTime = new Date().toISOString();

      // Criar o payload para o pedido com informações de auditoria
      const payload = {
        descricao: this.orderDescription,
        quantidade: this.orderQuantity,
        categoria: this.orderCategory,
        urgencia: this.orderUrgency,
        deliveryDate: this.orderDeliveryDate,
        observacao: this.orderNotes || "",
        sender: this.orderSender,
        setor: this.orderSenderSector,
        usuario_nome: this.userName || "Usuário do Sistema",
        file: this.orderFileBase64 || null,
        status: "Pendente",
        // Informações de auditoria
        audit_info: {
          created_at_exact: creationDateTime,
          browser_info: browserInfo,
          user_email: this.userEmail,
          user_type: this.userType,
          created_by_id: localStorage.getItem("user_id") || null
        }
      };

      console.log("Enviando pedido com nome de usuário:", this.userName);

      try {
        const response = await axiosService.post(
          `/pedidos/`,
          payload
        );

        // Exibe a notificação de sucesso
        toast.success("Pedido criado com sucesso!");

        // Se a opção de criar múltiplos pedidos estiver marcada, só limpa o formulário
        // Caso contrário, fecha o modal e emite os eventos normalmente
        if (this.createMultiple) {
          // Emitir evento para gerar a imagem automaticamente
          this.$emit("create-order-with-image", response.data);
          
          // Depois resetar formulário e manter campos relevantes
          this.resetForm();
          // Mantém os campos de responsável e urgência para facilitar múltiplos cadastros
          this.orderSender = payload.sender;
          this.orderUrgency = payload.urgencia;
        } else {
          this.resetForm();
          this.$emit("create-order", response.data);
          this.$emit("open-print-modal", response.data);
        }
      } catch (error) {
        // Exibe a notificação de erro
        toast.error(error.response?.data?.detail || "Erro ao criar o pedido. Verifique sua autenticação.");
        console.error("Erro ao criar pedido:", error.response ? error.response.data : error);
        
        // Se for erro de autenticação
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          toast.error("Sessão expirada ou inválida. Por favor, faça login novamente.");
        }
      } finally {
        // Desativar indicador de carregamento
        this.isSubmitting = false;
      }
    },
    resetForm() {
      this.orderDescription = "";
      this.orderQuantity = 1;
      this.orderCategory = "";
      this.orderUrgency = "Padrão";
      this.orderDeliveryDate = new Date().toISOString().split('T')[0];
      this.orderNotes = "";
      this.orderSender = "";
      this.orderSenderSector = "";
      this.orderFile = null;
      this.orderFileBase64 = "";
    },
    closeForm() {
      this.$emit("close");
    },
    handleOverlayClick(event) {
      event.stopPropagation(); 
    },
    handleFileUpload(event) {
      const file = event.target.files[0];

      if (!file) {
        console.error("Nenhum arquivo selecionado.");
        return;
      }

      console.log("Arquivo selecionado:", file);

      const reader = new FileReader();

      reader.onloadend = () => {
        const result = reader.result;
        console.log("FileReader resultado bruto:", result);

        if (result.includes(",")) {
          this.orderFileBase64 = result.split(",")[1];
        } else {
          this.orderFileBase64 = result;
        }

        console.log("Base64 gerado:", this.orderFileBase64);
      };

      reader.onerror = (error) => {
        console.error("Erro ao ler o arquivo:", error);
      };

      reader.readAsDataURL(file);
    },
    removeFile() {
      this.orderFile = null;
      this.orderFileBase64 = "";
    },
    decrementQuantity() {
      this.orderQuantity--;
    },
    incrementQuantity() {
      this.orderQuantity++;
    },
    validateQuantity() {
      const result = validateQuantity(this.orderQuantity);
      this.validationErrors.quantity = result.isValid ? "" : result.message;
      return result.isValid;
    },
    validateDescription() {
      const result = validateText(this.orderDescription, {
        required: true,
        fieldName: "Descrição do pedido"
      });
      this.validationErrors.description = result.isValid ? "" : result.message;
      return result.isValid;
    },
    validateCategory() {
      const result = validateText(this.orderCategory, {
        required: true,
        fieldName: "Categoria"
      });
      this.validationErrors.category = result.isValid ? "" : result.message;
      return result.isValid;
    },
    validateDate() {
      // Se o usuário não for admin, a data já está definida como hoje
      // então não precisa validar se está no passado
      const today = new Date().toISOString().split('T')[0];
      
      // Se data selecionada for hoje (data atual) para usuário comum, retorna como válido
      if (!this.isAdmin && this.orderDeliveryDate === today) {
        this.validationErrors.date = "";
        return true;
      }
      
      const result = validateDate(this.orderDeliveryDate, {
        required: true,
        allowPastDates: this.isAdmin // Apenas admin pode selecionar datas passadas
      });
      this.validationErrors.date = result.isValid ? "" : result.message;
      return result.isValid;
    },
    validateSender() {
      const result = validateText(this.orderSender, {
        required: true,
        minLength: 3,
        fieldName: "Responsável pela compra"
      });
      this.validationErrors.sender = result.isValid ? "" : result.message;
      return result.isValid;
    },
    validateForm() {
      // Executar todas as validações
      const isQuantityValid = this.validateQuantity();
      const isDescriptionValid = this.validateDescription();
      const isCategoryValid = this.validateCategory();
      const isDateValid = this.validateDate();
      const isSenderValid = this.validateSender();
      
      return isQuantityValid && isDescriptionValid && isCategoryValid && 
             isDateValid && isSenderValid;
    },
    showUrgencyTooltip(event) {
      this.isUrgencyTooltipVisible = true;
      
      // Calcula posição do tooltip em relação ao cursor
      if (!this.isMobile && event) {
        this.$nextTick(() => {
          const tooltip = this.$refs.urgencyTooltip;
          if (tooltip) {
            const rect = event.target.getBoundingClientRect();
            const tooltipWidth = tooltip.offsetWidth;
            
            // Posiciona o tooltip abaixo do cursor, considerando as bordas da tela
            this.tooltipStyle = {
              position: 'fixed',
              top: `${rect.bottom + 10}px`,
              left: `${Math.min(rect.left, window.innerWidth - tooltipWidth - 20)}px`,
              zIndex: '2000'
            };
          }
        });
      }
    },
    hideUrgencyTooltip() {
      this.isUrgencyTooltipVisible = false;
    },
    showFileTooltip(event) {
      this.isFileTooltipVisible = true;
      
      // Calcula posição do tooltip em relação ao cursor
      if (!this.isMobile && event) {
        this.$nextTick(() => {
          const tooltip = this.$refs.fileTooltip;
          if (tooltip) {
            const rect = event.target.getBoundingClientRect();
            const tooltipWidth = tooltip.offsetWidth;
            
            // Posiciona o tooltip abaixo do cursor, considerando as bordas da tela
            this.fileTooltipStyle = {
              position: 'fixed',
              top: `${rect.bottom + 10}px`,
              left: `${Math.min(rect.left, window.innerWidth - tooltipWidth - 20)}px`,
              zIndex: '2000'
            };
          }
        });
      }
    },
    hideFileTooltip() {
      this.isFileTooltipVisible = false;
    },
  },
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

/* Botão de fechar no canto superior */
.close-modal-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(255, 111, 97, 0.2);
  color: #fff;
  border: 1px solid #ff6f61;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
  z-index: 10;
  transition: all 0.2s ease;
}

.close-modal-btn:hover {
  background-color: rgba(255, 111, 97, 0.3);
}

.close-modal-btn i {
  font-size: 20px;
  margin: 0;
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: var(--spacing-lg); 
  border-radius: var(--border-radius-lg);
  width: var(--modal-width-md);
  max-width: var(--modal-max-width); 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  overflow-y: auto;
  max-height: var(--modal-max-height);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  margin: 20px 0;
}

/* Cabeçalho do formulário */
.form-header {
  margin-bottom: 25px;
  border-bottom: 1px solid #333;
  padding-bottom: 15px;
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
}

/* Informações do usuário */
.user-info {
  background-color: #333;
  padding: 5px 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.user-label {
  color: #999;
  margin-right: 5px;
}

.user-name {
  color: #ff6f61;
  font-weight: bold;
}

/* Grid para o formulário */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.full-width {
  grid-column: 1 / -1;
}

/* Estilo dos campos do formulário */
.form-group {
  margin-bottom: 15px; 
}

.form-group label {
  font-weight: bold;
  margin-bottom: 8px; 
  display: flex;
  align-items: center;
  color: #ff6f61; 
  font-size: 0.9rem;
}

.form-group label i {
  margin-right: 8px;
  font-size: 18px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px; 
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #333;
  color: #f5f5f5;
  font-size: 14px; 
  box-sizing: border-box;
  resize: vertical;
  text-transform: uppercase;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 111, 97, 0.2);
}

/* Estilo para o input de arquivo personalizado */
.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 2;
}

.custom-file-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 5px;
  color: #f5f5f5;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-file-button:hover {
  background-color: #444;
  border-color: #ff6f61;
}

.custom-file-button i {
  margin-right: 8px;
  color: #ff6f61;
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #333;
  border-radius: 5px;
  border: 1px solid #444;
}

.file-name {
  display: flex;
  align-items: center;
  max-width: 85%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-name i {
  margin-right: 5px;
  color: #ff6f61;
}

.remove-file {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.remove-file:hover {
  background-color: #444;
  color: #ff6f61;
}

.file-input-container {
  position: relative;
  margin-bottom: 10px;
}

/* Estilo para validação de campos */
input.invalid,
select.invalid,
textarea.invalid {
  border-color: #e74c3c;
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
}

.error-message {
  color: #ff5252;
  font-size: 0.85rem;
  margin-top: 5px;
  display: block;
  font-weight: 500;
}

.invalid {
  border-color: #ff5252 !important;
  box-shadow: 0 0 5px rgba(255, 82, 82, 0.3) !important;
}

textarea.invalid,
input.invalid,
select.invalid {
  background-color: rgba(255, 82, 82, 0.05);
}

/* Container para input de arquivo */
.file-input-container {
  position: relative;
}

.file-name {
  display: block;
  margin-top: 5px;
  font-size: 0.8rem;
  color: #ddd;
  word-break: break-all;
}

textarea {
  min-height: 90px; 
}

.options-group input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
  vertical-align: middle;
}

.options-group label {
  color: #f5f5f5;
  display: flex;
  align-items: center;
  font-weight: normal;
  cursor: pointer;
}

/* Estilo para o novo checkbox toggle switch */
.toggle-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  margin: 15px 0;
  padding: 10px;
  background-color: #333;
  border-radius: 8px;
  border: 1px solid #444;
}

.toggle-label {
  color: #f5f5f5;
  font-weight: normal;
  margin-right: 10px;
  flex: 1;
  display: flex;
  align-items: center;
}

.toggle-label i {
  margin-right: 8px;
  color: #ff6f61;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #555;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #fff;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #ff6f61;
}

input:focus + .slider {
  box-shadow: 0 0 1px #ff6f61;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* Botões do formulário */
.form-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  gap: 15px;
  position: relative;
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

button i {
  margin-right: 8px;
  font-size: 18px;
}

.submit-btn {
  background-color: #ff6f61;
  color: #1f1f1f;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 45px;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.submit-btn:hover {
  background-color: #e05545;
}

.close-btn {
  background-color: rgba(51, 51, 51, 0.7);
  color: #f5f5f5;
  border: 1px solid #555;
}

.close-btn:hover {
  background-color: #333;
  color: #fff;
  border-color: #999;
}

/* Mensagem de sucesso */
.success-message {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  text-align: center;
}

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .order-form {
    width: 90%;
    max-width: var(--modal-max-width);
    padding: 20px;
  }
  
  .form-header h2 {
    font-size: 1.3rem;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .order-form {
    width: 90%;
    max-width: 550px;
    padding: 20px;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-info {
    margin-top: 10px;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 10px;
    align-items: flex-start;
  }
  
  .order-form {
    width: 95%;
    padding: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    max-height: 85vh;
  }
  
  .close-modal-btn {
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    background-color: rgba(255, 111, 97, 0.3);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
  
  .close-modal-btn i {
    font-size: 18px;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
    text-align: center;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .user-info {
    width: 100%;
    justify-content: center;
  }
  
  .form-group {
    margin-bottom: 12px;
  }
  
  .form-group label {
    font-size: 0.85rem;
  }
  
  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 10px;
    font-size: 0.85rem;
  }
  
  textarea {
    min-height: 70px;
  }
  
  .form-buttons {
    position: sticky;
    bottom: 0;
    background-color: #1f1f1f;
    padding-top: 10px;
    margin-bottom: 0;
    z-index: 5;
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin-top: 15px;
  }
  
  .form-buttons button {
    padding: 12px 15px;
    font-size: 0.85rem;
  }
  
  .submit-btn, .close-btn {
    min-height: 44px;
  }
  
  button i {
    margin-right: 5px;
    font-size: 16px;
  }
  
  .submit-btn {
    background-color: #ff6f61;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
}

/* Ajustes para telas pequenas */
@media (max-width: 360px) {
  .form-buttons {
    flex-direction: column;
    gap: 10px;
    padding-bottom: 5px;
  }
  
  .form-buttons button {
    width: 100%;
    margin: 0;
  }
  
  .submit-btn {
    order: -1;
    margin-bottom: 8px;
  }
}

/* Ajustes para modo paisagem em telas pequenas */
@media (max-height: 500px) {
  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .full-width {
    grid-column: 1 / -1;
  }
  
  .form-buttons {
    padding: 5px 0;
    margin-top: 10px;
  }
  
  textarea {
    min-height: 60px;
  }
}

/* Ajuste para telas menores com altura suficiente */
@media (max-width: 480px) and (min-height: 600px) {
  .order-form {
    padding-bottom: 70px;
  }
  
  .form-buttons {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #1f1f1f;
    padding: 10px 15px;
    margin: 0;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
    z-index: 100;
  }
}

/* Legenda de urgência */
.urgency-legend {
  margin-top: 8px;
  background-color: #2a2a2a;
  border-radius: 5px;
  padding: 8px 10px;
  font-size: 0.8rem;
  border: 1px solid #444;
}

.urgency-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.urgency-item:last-child {
  margin-bottom: 0;
}

.urgency-icon {
  font-size: 14px;
  margin-right: 8px;
}

.urgency-icon.padrão {
  color: #3498db;
}

.urgency-icon.urgente {
  color: #ff6f61;
}

.urgency-icon.critico {
  color: #e74c3c;
}

.urgency-desc {
  color: #ddd;
}

.input-helper {
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.helper-text {
  font-size: 0.8rem;
  color: #999;
}

/* Info Tooltip Container */
.info-tooltip-container {
  position: relative;
  display: inline-block;
  margin-top: 5px;
  margin-left: 10px;
  z-index: 1000;
}

.info-icon-wrapper {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 3px;
  border-radius: 50%;
  transition: all 0.3s ease;
  margin-right: 5px;
}

.info-icon-wrapper:hover {
  background-color: rgba(255, 111, 97, 0.1);
}

.info-icon {
  color: #ff6f61;
  font-size: 16px;
}

.info-tooltip {
  position: absolute;
  top: 25px;
  left: 0;
  background-color: #333;
  color: #f5f5f5;
  padding: 12px;
  border-radius: 5px;
  width: 280px;
  max-width: 90vw;
  z-index: 1001;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity 0.3s ease, visibility 0.3s ease;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  border: 1px solid #444;
}

.info-tooltip:after {
  content: '';
  position: absolute;
  top: -10px;
  left: 10px;
  border-width: 0 10px 10px;
  border-style: solid;
  border-color: transparent transparent #333;
}

.info-tooltip.show {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}

/* Para o tooltip que segue cursor em modo desktop */
@media (min-width: 992px) {
  .info-tooltip {
    width: 320px;
    max-width: calc(100vw - 100px);
  }
  
  .info-tooltip.show[style] {
    position: fixed !important;
  }
  
  .info-tooltip.show[style]:after {
    display: none;
  }
}

/* Para o caso específico da legenda de urgência, ajuste o posicionamento */
.form-group .info-tooltip-container .info-tooltip {
  width: 300px;
}

/* Para a posição do tooltip em diferentes tipos de dispositivos */
@media (min-width: 481px) and (max-width: 991px) {
  .info-tooltip-container .info-tooltip {
    top: 25px;
    right: auto;
    left: 0;
  }
  
  .info-tooltip-container .info-tooltip:after {
    right: auto;
    left: 10px;
    border-width: 0 10px 10px;
    border-color: transparent transparent #333;
  }
}

@media (max-width: 480px) {
  .tooltip-header {
    padding-bottom: 10px;
    margin-bottom: 12px;
  }
  
  .tooltip-title {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .info-tooltip {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    max-width: 280px;
    border-radius: 8px;
    z-index: 1100;
  }
  
  .info-tooltip:after {
    display: none;
  }
  
  .info-tooltip.show:before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1099;
  }
  
  .form-group .info-tooltip-container .info-tooltip {
    width: 80%;
    max-width: 300px;
  }
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  margin-bottom: 10px;
  border-bottom: 1px solid #444;
}

.tooltip-title {
  font-weight: bold;
  color: #ff6f61;
  font-size: 1rem;
}

.close-tooltip {
  background: none;
  border: none;
  color: #999;
  padding: 4px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-tooltip:hover {
  background-color: #444;
  color: #ff6f61;
}

/* Quantity Input Container */
.quantity-input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  border: 1px solid #444;
  border-radius: 5px;
  overflow: hidden;
  background-color: #333;
}

.quantity-input-container input {
  border: none;
  text-align: center;
  width: 60%;
  padding: 12px 0;
  margin: 0;
  background-color: transparent;
}

.quantity-input-container input:focus {
  box-shadow: none;
  border: none;
  outline: none;
}

.quantity-btn {
  background-color: #444;
  border: none;
  color: #f5f5f5;
  cursor: pointer;
  padding: 12px 15px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.quantity-btn:hover:not(:disabled) {
  background-color: #555;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-note {
  font-size: 0.8rem;
  color: #999;
  margin-top: 5px;
}

.file-input-wrapper {
  display: flex;
  align-items: center;
  margin-top: 8px;
}

.file-info-content {
  font-size: 0.85rem;
}

.file-info-content p {
  margin: 8px 0;
}

.file-info-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.file-info-content li {
  margin-bottom: 4px;
}

/* Ajustes visuais adicionais */
.urgency-legend {
  margin: 0;
  padding: 5px 0;
}

@media (min-width: 481px) and (max-width: 991px) {
  .info-tooltip-container .info-tooltip {
    top: 25px;
    right: auto;
    left: 0;
  }
  
  .info-tooltip-container .info-tooltip:after {
    right: auto;
    left: 10px;
    border-width: 0 10px 10px;
    border-color: transparent transparent #333;
  }
}

/* Date Input Container */
.date-input-container {
  position: relative;
}

.date-input-container input[type="date"] {
  padding-right: 40px; /* Espaço para o ícone */
}

.date-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  pointer-events: none; /* Para não interferir com cliques no input */
}

/* Fundo para os botões para efeito visual na parte inferior */
.form-buttons::before {
  content: '';
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(to top, rgba(31, 31, 31, 1), rgba(31, 31, 31, 0));
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.form-buttons.sticky::before {
  opacity: 1;
}

/* Dispositivos móveis em orientação retrato */
@media (max-width: 480px) and (orientation: portrait) {
  .modal-overlay {
    padding: 10px;
    align-items: flex-start;
  }
  
  .order-form {
    width: 95%;
    padding: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    max-height: 85vh;
  }
  
  .close-modal-btn {
    top: 10px;
    right: 10px;
    width: 32px;
    height: 32px;
    background-color: rgba(255, 111, 97, 0.3);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
  
  .close-modal-btn i {
    font-size: 18px;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
    text-align: center;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .user-info {
    width: 100%;
    justify-content: center;
  }
}

/* Ajustes de formulário para dispositivos móveis (ambas orientações) */
@media (max-width: 480px) {
  .form-group {
    margin-bottom: 12px;
  }
  
  .form-group label {
    font-size: 0.85rem;
  }
  
  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 10px;
    font-size: 0.85rem;
  }
  
  textarea {
    min-height: 70px;
  }
  
  .form-buttons {
    display: flex;
    flex-direction: row;
    gap: 10px;
    margin-top: 15px;
    padding: 10px 0;
  }
  
  .form-buttons button {
    padding: 12px 15px;
    font-size: 0.85rem;
    min-height: 44px;
  }
  
  button i {
    margin-right: 5px;
    font-size: 16px;
  }
  
  .submit-btn {
    background-color: #ff6f61;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
}

/* Dispositivos móveis em orientação paisagem */
@media (max-width: 850px) and (orientation: landscape) {
  .modal-overlay {
    align-items: flex-start;
    padding: 10px 15px;
  }
  
  .order-form {
    max-height: 85vh;
    padding: 15px;
    margin: 5px 0;
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .form-header {
    margin-bottom: 15px;
    padding-bottom: 10px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  textarea {
    min-height: 60px;
  }
}
</style>

