<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleOverlayClick">
    <div class="order-form" @click.stop>
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
            ></textarea>
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
                required 
                :class="{ 'invalid': validationErrors.quantity }"
              />
              <button type="button" class="quantity-btn" @click="incrementQuantity">
                <i class="material-icons">add</i>
              </button>
            </div>
            <div class="input-note">
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
            <div class="info-tooltip-container">
              <span class="info-icon-wrapper" 
                 @mouseenter="showUrgencyTooltip" 
                 @mouseleave="hideUrgencyTooltip">
                <i class="material-icons info-icon">info</i>
              </span>
              <div class="info-tooltip" :class="{ show: isUrgencyTooltipVisible }" ref="urgencyTooltip" 
                 :style="tooltipStyle">
                <div class="tooltip-header" v-if="isMobile">
                  <span class="tooltip-title">Informações de Urgência</span>
                  <button type="button" class="close-tooltip" @click="hideUrgencyTooltip">
                    <i class="material-icons">close</i>
                  </button>
                </div>
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
              </div>
            </div>
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
                <div class="info-tooltip-container">
                  <span class="info-icon-wrapper"
                     @mouseenter="showFileTooltip"
                     @mouseleave="hideFileTooltip">
                    <i class="material-icons info-icon">info</i>
                  </span>
                  <div class="info-tooltip" :class="{ show: isFileTooltipVisible }" ref="fileTooltip"
                     :style="fileTooltipStyle">
                    <div class="tooltip-header" v-if="isMobile">
                      <span class="tooltip-title">Sobre anexos</span>
                      <button type="button" class="close-tooltip" @click="hideFileTooltip">
                        <i class="material-icons">close</i>
                      </button>
                    </div>
                    <div class="file-info-content">
                      <p>Você pode anexar arquivos como:</p>
                      <ul>
                        <li>Imagens (JPG, PNG, GIF)</li>
                        <li>Documentos (PDF, DOC, XLS)</li>
                        <li>Outros arquivos de referência</li>
                      </ul>
                      <p>Tamanho máximo: 10MB</p>
                    </div>
                  </div>
                </div>
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
          <button type="submit" class="submit-btn">
            <i class="material-icons">send</i>
            ENVIAR PEDIDO
          </button>
          <button type="button" class="close-btn" @click="closeForm">
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

export default {
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
        quantity: false
      },
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
      
      // Validar quantidade
      if (this.orderQuantity < 1) {
        this.orderQuantity = 1;
        this.validationErrors.quantity = true;
        toast.warning("A quantidade deve ser maior que zero!");
        return;
      }

      // Validar campos obrigatórios
      if (!this.orderDescription || !this.orderQuantity || !this.orderSender || !this.orderCategory) {
        toast.warning("Por favor, preencha todos os campos obrigatórios!");
        return;
      }

      if (!this.orderFileBase64 && this.orderFile) {
        toast.warning("Aguarde o processamento do arquivo antes de enviar o pedido.");
        return;
      }

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

      // Criar o payload para o pedido
      const payload = {
        descricao: this.orderDescription,
        quantidade: this.orderQuantity,
        categoria: this.orderCategory,
        urgencia: this.orderUrgency,
        deliveryDate: new Date().toISOString(), // Sempre usa a data e hora atual, ignorando o valor do input
        observacao: this.orderNotes || "",
        sender: this.orderSender,
        setor: this.orderSenderSector,
        usuario_nome: this.userName || "Usuário do Sistema",
        file: this.orderFileBase64 || null,
        status: "Pendente",
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
      if (this.orderQuantity < 1) {
        this.orderQuantity = 1;
        this.validationErrors.quantity = true;
      } else {
        this.validationErrors.quantity = false;
      }
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
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: 15px;
  box-sizing: border-box;
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 30px; 
  border-radius: 10px;
  width: 100%;
  max-width: 800px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  overflow-y: auto;
  max-height: 90vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 5px;
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
}

.submit-btn:hover {
  background-color: #e05545;
}

.close-btn {
  background-color: transparent;
  color: #999;
  border: 1px solid #555;
}

.close-btn:hover {
  background-color: #333;
  color: #fff;
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
    max-width: 90%;
    padding: 25px;
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
    max-width: 95%;
    padding: 20px;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-info {
    margin-top: 10px;
  }
  
  .form-group label {
    font-size: 0.85rem;
  }
  
  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 10px;
    font-size: 0.9rem;
  }
  
  textarea {
    min-height: 80px;
  }
  
  button {
    padding: 10px 15px;
    font-size: 0.9rem;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .order-form {
    padding: 15px;
    max-width: 100%;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  .form-group label {
    font-size: 0.8rem;
  }
  
  .form-group input,
  .form-group select,
  .form-group textarea {
    padding: 8px;
    font-size: 0.85rem;
  }
  
  textarea {
    min-height: 70px;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  button {
    padding: 10px;
    font-size: 0.85rem;
    margin-top: 10px;
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
</style>

