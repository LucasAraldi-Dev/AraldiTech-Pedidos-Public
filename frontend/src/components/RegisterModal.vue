<template>
  <transition name="expand-modal">
    <div class="modal-overlay" v-if="isModalOpen">
      <div class="modal" :class="{ 'registering': isRegistering, 'success': registerSuccess, 'error': registerError }">
        <!-- Formulário de cadastro normal -->
        <div v-if="!isRegistering && !registerSuccess && !registerError">
          <h2>Cadastro</h2>
          <form @submit.prevent="startRegistrationProcess">
            <div class="form-group">
              <label for="name" class="form-label">Nome Completo</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-user"></i>
                </div>
                <input
                  id="name"
                  type="text"
                  v-model="name"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="username" class="form-label">Nome de Usuário</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-user-tag"></i>
                </div>
                <input
                  id="username"
                  type="text"
                  v-model="username"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="signupEmail" class="form-label">E-mail</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-envelope"></i>
                </div>
                <input
                  id="signupEmail"
                  type="email"
                  v-model="signupEmail"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="signupPassword" class="form-label">Senha</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-lock"></i>
                </div>
                <input
                  id="signupPassword"
                  type="password"
                  v-model="signupPassword"
                  required
                  @input="checkPasswordStrength"
                />
              </div>
              <div class="password-strength" :class="passwordStrengthClass">
                {{ passwordStrengthMessage }}
              </div>
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="form-label">Repetir Senha</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-shield"></i>
                </div>
                <input
                  id="confirmPassword"
                  type="password"
                  v-model="confirmPassword"
                  required
                  @input="checkPasswordMatch"
                />
              </div>
              <div v-if="!passwordsMatch && confirmPassword" class="password-error">
                As senhas não coincidem
              </div>
            </div>

            <div class="form-group">
              <label for="setor" class="form-label">Setor</label>
              <div class="input-container">
                <div class="input-icon">
                  <i class="fa-building"></i>
                </div>
                <select v-model="setor" id="setor" required>
                  <option value="" disabled selected>Selecione um setor</option>
                  <option value="Escritório">Escritório</option>
                  <option value="Fábrica de Ração">Fábrica de Ração</option>
                  <option value="CPO">CPO</option>
                  <option value="Granjas">Granjas</option>
                  <option value="Abatedouro">Abatedouro</option>
                  <option value="Transporte">Transporte</option>
                  <option value="Incubatório">Incubatório</option>
                  <option value="Favorito">Favorito</option>
                </select>
              </div>
            </div>

            <div class="terms-info">
              <p>Ao clicar em "Cadastrar", você concorda com nossos <span class="terms-link">Termos de Serviço</span> e <span class="terms-link">Política de Privacidade</span>.</p>
            </div>

            <div class="action-buttons">
              <button type="submit" class="submit-button" :disabled="!isFormValid">Cadastrar</button>
              <button type="button" class="cancel-button" @click="closeModal">Cancelar</button>
            </div>
          </form>
        </div>

        <!-- Estado de registro em andamento -->
        <div v-if="isRegistering" class="register-progress">
          <div class="progress-steps">
            <div class="progress-step" :class="{ 'active': currentStep >= 1, 'completed': currentStep > 1 }">
              <div class="step-indicator">1</div>
              <div class="step-label">Validando informações</div>
            </div>
            <div class="progress-step" :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
              <div class="step-indicator">2</div>
              <div class="step-label">Criando conta</div>
            </div>
            <div class="progress-step" :class="{ 'active': currentStep >= 3, 'completed': currentStep > 3 }">
              <div class="step-indicator">3</div>
              <div class="step-label">Configurando perfil</div>
            </div>
          </div>
          <div class="spinner"></div>
          <div class="status-message">{{ statusMessage }}</div>
        </div>

        <!-- Estado de sucesso no cadastro -->
        <div v-if="registerSuccess" class="register-success">
          <div class="success-icon">✓</div>
          <div class="success-message">Cadastro realizado com sucesso!</div>
          
          <!-- Card de informações do usuário -->
          <div class="user-card">
            <div class="user-card-header">
              <div class="user-avatar">{{ getUserInitials() }}</div>
              <h3 class="user-name">{{ name }}</h3>
            </div>
            <div class="user-card-body">
              <div class="user-info-item">
                <div class="info-label">Nome de Usuário:</div>
                <div class="info-value">{{ username }}</div>
              </div>
              <div class="user-info-item">
                <div class="info-label">E-mail:</div>
                <div class="info-value">{{ signupEmail }}</div>
              </div>
              <div class="user-info-item">
                <div class="info-label">Setor:</div>
                <div class="info-value">{{ setor }}</div>
              </div>
            </div>
            <div class="user-card-footer">
              <div class="success-buttons">
                <button class="login-now-button" @click="goToLogin">Fazer Login</button>
                <button class="close-button" @click="closeModal">Fechar</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Estado de erro no cadastro -->
        <div v-if="registerError" class="register-error">
          <div class="error-icon">!</div>
          <div class="error-title">{{ errorTitle }}</div>
          <div class="error-message">{{ errorMessage }}</div>
          <div class="error-help">{{ errorHelp }}</div>
          <div class="error-actions">
            <button @click="resetRegistration" class="retry-button">Tentar novamente</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
  
  <!-- Modal de Termos de Serviço -->
  <TermsOfServiceModal 
    :show="showTermsModal" 
    @accept-terms="handleTermsAccepted" 
    @decline-terms="handleTermsDeclined" 
  />
</template>

<script>
import { useToast } from 'vue-toastification';
import { ref, computed, watch } from 'vue';
import TermsOfServiceModal from './TermsOfServiceModal.vue';

export default {
  props: {
    isModalOpen: Boolean,
  },
  components: {
    TermsOfServiceModal
  },
  emits: ['close-modal', 'signup', 'go-to-login'],
  setup(props, { emit }) {
    const toast = useToast();
    
    // Campos do formulário
    const name = ref("");
    const username = ref("");
    const signupEmail = ref("");
    const signupPassword = ref("");
    const confirmPassword = ref("");
    const setor = ref("");
    
    // Estados para o fluxo de cadastro
    const isRegistering = ref(false);
    const registerSuccess = ref(false);
    const registerError = ref(false);
    const currentStep = ref(0);
    const statusMessage = ref("");
    
    // Estado para o modal de termos de serviço
    const showTermsModal = ref(false);
    const termsAcceptance = ref(null);
    
    // Estados para tratamento de erros
    const errorType = ref("");
    const errorTitle = ref("");
    const errorMessage = ref("");
    const errorHelp = ref("");
    
    // Validação de senha
    const passwordStrength = ref(0);
    const passwordStrengthMessage = ref("");
    const passwordsMatch = ref(true);
    
    const passwordStrengthClass = computed(() => ({
      'weak': passwordStrength.value < 2,
      'medium': passwordStrength.value === 2,
      'strong': passwordStrength.value > 2
    }));
    
    const isFormValid = computed(() => 
      name.value && 
      username.value && 
      signupEmail.value && 
      signupPassword.value && 
      confirmPassword.value && 
      passwordsMatch.value &&
      setor.value
    );
    
    // Método para iniciar o processo de cadastro
    const startRegistrationProcess = async () => {
      if (!isFormValid.value) {
        toast.error("Por favor, preencha todos os campos corretamente!");
        return;
      }
      
      // Mostrar o modal de termos de serviço antes de prosseguir
      showTermsModal.value = true;
    };
    
    // Callback quando os termos são aceitos
    const handleTermsAccepted = (termsData) => {
      showTermsModal.value = false;
      termsAcceptance.value = termsData;
      proceedWithRegistration();
    };
    
    // Callback quando os termos são recusados
    const handleTermsDeclined = () => {
      showTermsModal.value = false;
      toast.error("É necessário aceitar os Termos de Serviço para criar uma conta");
    };
    
    // Continuar com o processo de cadastro após aceitar os termos
    const proceedWithRegistration = async () => {
      isRegistering.value = true;
      currentStep.value = 1;
      statusMessage.value = "Validando suas informações...";
      
      // Simulação de verificação inicial (1.5 segundos)
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      try {
        // Passo 2: Criando conta
        currentStep.value = 2;
        statusMessage.value = "Criando sua conta...";
        
        // Simulação de criação de conta (2 segundos)
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Dados do usuário a serem enviados para cadastro
        const userData = {
          nome: name.value,
          username: username.value,
          email: signupEmail.value,
          senha: signupPassword.value,
          setor: setor.value,
          // Incluir informações do aceite dos termos
          termsAcceptance: termsAcceptance.value
        };
        
        // Passo 3: Configurando perfil
        currentStep.value = 3;
        statusMessage.value = "Configurando seu perfil...";
        
        // Simulação de configuração de perfil (1.5 segundos)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Envia os dados para o componente pai para efetuar o cadastro
        try {
          // Emite o evento signup e aguarda resposta
          await new Promise((resolve, reject) => {
            // Cria um ouvinte de evento único para resposta de cadastro
            const handleSignupResponse = (success, error) => {
              if (success) {
                resolve(true);
              } else {
                reject(error || new Error("Falha ao cadastrar usuário"));
              }
            };
            
            // Emite o evento com o callback para resposta
            emit("signup", userData, handleSignupResponse);
            
            // Timeout para caso não haja resposta em 5 segundos
            setTimeout(() => {
              reject(new Error("Timeout ao tentar cadastrar usuário"));
            }, 5000);
          });
          
          // Se chegou aqui, o cadastro foi bem sucedido
          isRegistering.value = false;
          registerSuccess.value = true;
        } catch (error) {
          // Erro específico do cadastro
          console.error("Erro na resposta do cadastro:", error);
          isRegistering.value = false;
          showDatabaseError(error.message);
        }
      } catch (error) {
        console.error("Erro ao processar cadastro:", error);
        isRegistering.value = false;
        
        // Mostrar erro específico com base no tipo de erro
        showGenericError();
      }
    };
    
    // Função para obter as iniciais do nome do usuário
    const getUserInitials = () => {
      if (!name.value) return '';
      
      return name.value
        .split(' ')
        .map(word => word.charAt(0).toUpperCase())
        .slice(0, 2)
        .join('');
    };
    
    // Funções para validação de senha
    const checkPasswordStrength = () => {
      let strength = 0;
      let message = "Senha fraca";

      // Verifica comprimento
      if (signupPassword.value.length >= 8) strength++;
      
      // Verifica se contém números
      if (/\d/.test(signupPassword.value)) strength++;
      
      // Verifica se contém letras maiúsculas e minúsculas
      if (/[a-z]/.test(signupPassword.value) && /[A-Z]/.test(signupPassword.value)) strength++;
      
      // Verifica se contém caracteres especiais
      if (/[!@#$%^&*(),.?":{}|<>]/.test(signupPassword.value)) strength++;

      // Define a mensagem baseada na força
      if (strength <= 1) {
        message = "Senha fraca";
      } else if (strength === 2) {
        message = "Senha média";
      } else if (strength === 3) {
        message = "Senha forte";
      } else {
        message = "Senha muito forte";
      }

      passwordStrength.value = strength;
      passwordStrengthMessage.value = message;
      
      // Verificar se as senhas coincidem quando a senha é alterada
      if (confirmPassword.value) {
        checkPasswordMatch();
      }
    };
    
    const checkPasswordMatch = () => {
      passwordsMatch.value = signupPassword.value === confirmPassword.value;
    };
    
    // Funções para tratamento de erros
    const showGenericError = () => {
      registerError.value = true;
      errorType.value = "generic";
      errorTitle.value = "Erro no cadastro";
      errorMessage.value = "Ocorreu um erro durante o processo de cadastro.";
      errorHelp.value = "Verifique suas informações e tente novamente. Se o problema persistir, entre em contato com o suporte.";
    };
    
    const showDatabaseError = (message) => {
      registerError.value = true;
      errorType.value = "database";
      
      // Identificar tipos de erros específicos através das mensagens recebidas
      if (message && message.includes("Nome de usuário já está em uso")) {
        errorTitle.value = "Nome de usuário indisponível";
        errorMessage.value = "Este nome de usuário já está cadastrado no sistema.";
        errorHelp.value = "Por favor, escolha um nome de usuário diferente e tente novamente.";
      } 
      else if (message && message.includes("E-mail já está em uso")) {
        errorTitle.value = "E-mail já cadastrado";
        errorMessage.value = "Este endereço de e-mail já está associado a uma conta.";
        errorHelp.value = "Se este e-mail é seu, tente fazer login ou recuperar sua senha. Caso contrário, utilize outro e-mail.";
      }
      else if (message && message.includes("Timeout")) {
        errorTitle.value = "Tempo de conexão esgotado";
        errorMessage.value = "O servidor demorou muito para responder.";
        errorHelp.value = "Verifique sua conexão com a internet e tente novamente. Se o problema persistir, o servidor pode estar sobrecarregado.";
      }
      else if (message && message.includes("Network Error")) {
        errorTitle.value = "Erro de conexão";
        errorMessage.value = "Não foi possível estabelecer conexão com o servidor.";
        errorHelp.value = "Verifique sua conexão com a internet e tente novamente.";
      }
      else {
        // Erro genérico de banco de dados
        errorTitle.value = "Erro no processamento";
        errorMessage.value = message || "Ocorreu um erro ao processar seu cadastro.";
        errorHelp.value = "Por favor, tente novamente. Se o problema persistir, entre em contato com o suporte técnico.";
      }
    };
    
    // Função para reiniciar o processo de cadastro
    const resetRegistration = () => {
      registerError.value = false;
      errorType.value = "";
      errorTitle.value = "";
      errorMessage.value = "";
      errorHelp.value = "";
    };
    
    // Função para ir para a tela de login após cadastro
    const goToLogin = () => {
      emit("close-modal");
      emit("go-to-login");
    };
    
    // Função para fechar o modal
    const closeModal = () => {
      emit("close-modal");
    };
    
    // Resetar o estado quando o modal é fechado
    watch(() => props.isModalOpen, (newValue) => {
      if (!newValue) {
        termsAcceptance.value = null;
        showTermsModal.value = false;
      }
    });
    
    return {
      // Campos do formulário
      name,
      username,
      signupEmail,
      signupPassword,
      confirmPassword,
      setor,
      
      // Estados e mensagens
      isRegistering,
      registerSuccess,
      registerError,
      currentStep,
      statusMessage,
      errorType,
      errorTitle,
      errorMessage,
      errorHelp,
      passwordStrength,
      passwordStrengthMessage,
      passwordsMatch,
      
      // Estado do modal de termos
      showTermsModal,
      handleTermsAccepted,
      handleTermsDeclined,
      
      // Computed properties
      passwordStrengthClass,
      isFormValid,
      
      // Métodos
      startRegistrationProcess,
      checkPasswordStrength,
      checkPasswordMatch,
      resetRegistration,
      goToLogin,
      closeModal,
      getUserInitials,
      
      // Utilitários
      toast
    };
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
  transition: backdrop-filter 0.3s ease;
}

.modal {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: 40px;
  border-radius: 12px;
  width: 90%;
  max-width: 550px;
  color: white;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
}

h2 {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 24px;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 16px;
  color: #eee;
  font-weight: 500;
}

.input-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.input-container input,
.input-container select {
  width: 100%;
  padding: 14px 20px;
  padding-left: 45px;
  border: 1px solid #555;
  border-radius: 8px;
  background: #444;
  color: white;
  outline: none;
  font-size: 16px;
  transition: all 0.3s ease;
}

.input-container input:focus,
.input-container select:focus {
  border-color: #66ccff;
  box-shadow: 0 0 8px rgba(102, 204, 255, 0.3);
}

.input-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 15px;
  font-size: 18px;
  color: #bbb;
  pointer-events: none;
  z-index: 1;
}

.input-icon i::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-size: contain;
  background-repeat: no-repeat;
}

/* Estilos para ícones */
.input-icon .fa-user::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 5c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-user-tag::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-envelope::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6h16l-8 5z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-lock::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-shield::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-building::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z' fill='%23bbb'/%3E%3C/svg%3E");
}

/* Botões de ação */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.submit-button, .cancel-button {
  flex: 1;
  padding: 14px 20px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.submit-button {
  background-color: #555;
  color: white;
  border: 2px solid #555;
}

.submit-button:hover {
  background-color: #444;
  border-color: #444;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.cancel-button {
  background-color: transparent;
  color: #bbb;
  border: 2px solid #555;
}

.cancel-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

/* Estilos para verificação de senha */
.password-strength {
  margin-top: 8px;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
}

.password-strength.weak {
  background-color: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
  border: 1px solid #ff6b6b;
}

.password-strength.medium {
  background-color: rgba(255, 217, 61, 0.2);
  color: #ffd93d;
  border: 1px solid #ffd93d;
}

.password-strength.strong {
  background-color: rgba(107, 255, 107, 0.2);
  color: #6bff6b;
  border: 1px solid #6bff6b;
}

.password-error {
  color: #ff6b6b;
  font-size: 13px;
  margin-top: 5px;
  padding-left: 5px;
}

/* Estilos para o processo de registro */
.register-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.progress-steps {
  width: 100%;
  margin-bottom: 30px;
}

.progress-step {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.progress-step.active {
  opacity: 1;
}

.step-indicator {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 10px;
}

.progress-step.active .step-indicator {
  background: #66ccff;
  box-shadow: 0 0 10px rgba(102, 204, 255, 0.5);
}

.progress-step.completed .step-indicator {
  background: #00cc66;
}

.step-label {
  font-size: 15px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top: 4px solid #66ccff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 20px 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.status-message {
  font-size: 16px;
  text-align: center;
  color: #ddd;
  margin-top: 10px;
}

/* Estilos para o estado de sucesso */
.register-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.success-icon {
  width: 70px;
  height: 70px;
  background: #00cc66;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-bottom: 20px;
  box-shadow: 0 5px 15px rgba(0, 204, 102, 0.4);
  animation: scaleIn 0.5s ease forwards, pulse 2s infinite 0.5s;
  transform: scale(0);
}

@keyframes scaleIn {
  to { transform: scale(1); }
}

@keyframes pulse {
  0% { box-shadow: 0 5px 15px rgba(0, 204, 102, 0.4); }
  50% { box-shadow: 0 5px 25px rgba(0, 204, 102, 0.7); }
  100% { box-shadow: 0 5px 15px rgba(0, 204, 102, 0.4); }
}

.success-message {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #00cc66;
}

/* Card de informações do usuário */
.user-card {
  width: 100%;
  margin: 20px 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: fadeIn 0.5s ease-in-out forwards;
  opacity: 0;
  z-index: 10;
}

@keyframes fadeIn {
  to { opacity: 1; }
}

.user-card-header {
  padding: 20px;
  background: linear-gradient(135deg, #444, #333);
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 50px;
  height: 50px;
  background: #66ccff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  margin-right: 15px;
  box-shadow: 0 3px 8px rgba(102, 204, 255, 0.4);
}

.user-name {
  font-size: 18px;
  margin: 0;
  font-weight: 500;
}

.user-card-body {
  padding: 20px;
}

.user-info-item {
  display: flex;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-label {
  flex: 1;
  font-weight: bold;
  color: #bbb;
  text-align: left;
}

.info-value {
  flex: 2;
  text-align: left;
  word-break: break-word;
}

.user-card-footer {
  padding: 15px 20px;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;
}

.success-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.login-now-button {
  background: #66ccff;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.login-now-button:hover {
  background: #5ab8e6;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 204, 255, 0.4);
}

.close-button {
  background: transparent;
  color: #bbb;
  border: 1px solid #555;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  transform: translateY(-2px);
}

/* Estilos para o estado de erro */
.register-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  animation: shakeError 0.5s cubic-bezier(.36,.07,.19,.97) both;
  transform: translate3d(0, 0, 0);
}

@keyframes shakeError {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

.error-icon {
  width: 70px;
  height: 70px;
  background: #ff3d71;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 20px;
  box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4);
  animation: pulseError 2s infinite;
}

@keyframes pulseError {
  0% { transform: scale(1); box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4); }
  50% { transform: scale(1.05); box-shadow: 0 5px 25px rgba(255, 61, 113, 0.6); }
  100% { transform: scale(1); box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4); }
}

.error-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #ff3d71;
}

.error-message {
  color: #ddd;
  font-size: 16px;
  margin-bottom: 10px;
}

.error-help {
  color: #bbb;
  font-size: 14px;
  margin-bottom: 25px;
  padding: 0 10px;
}

.error-actions {
  width: 100%;
  display: flex;
  justify-content: center;
}

.retry-button {
  padding: 12px 25px;
  background-color: #555;
  border: 1px solid #555;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background-color: #666;
  transform: translateY(-3px);
}

/* Transição do Modal */
.expand-modal-enter-active,
.expand-modal-leave-active {
  transition: all 0.4s ease;
}

.expand-modal-enter-from {
  transform: scale(0.9);
  opacity: 0;
}

.expand-modal-enter-to {
  transform: scale(1);
  opacity: 1;
}

.expand-modal-leave-from {
  transform: scale(1);
  opacity: 1;
}

.expand-modal-leave-to {
  transform: scale(0.9);
  opacity: 0;
}

/* Responsividade para diferentes dispositivos */
@media (min-width: 1200px) {
  .modal {
    max-width: 600px;
    padding: 50px;
  }
  
  h2 {
    font-size: 28px;
    margin-bottom: 30px;
  }
  
  .input-container input, 
  .input-container select {
    padding: 16px 22px;
    padding-left: 50px;
    font-size: 17px;
  }
  
  .input-icon {
    left: 18px;
  }
  
  .form-label {
    font-size: 17px;
  }
  
  .submit-button, .cancel-button {
    padding: 16px 22px;
    font-size: 17px;
  }
}

@media (max-width: 768px) {
  .modal {
    padding: 30px;
    max-width: 450px;
  }
  
  .input-container input, 
  .input-container select {
    padding: 12px 15px;
    padding-left: 40px;
  }
  
  .input-icon {
    left: 12px;
  }
  
  .form-label {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .modal {
    padding: 25px;
    width: 95%;
    border-radius: 10px;
  }
  
  h2 {
    font-size: 22px;
    margin-bottom: 15px;
  }
  
  .input-container input, 
  .input-container select {
    padding: 10px 8px;
    padding-left: 36px;
    font-size: 15px;
  }
  
  .form-label {
    font-size: 14px;
    margin-bottom: 6px;
  }
  
  .input-icon {
    left: 10px;
    font-size: 16px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .submit-button, .cancel-button {
    padding: 10px 15px;
    font-size: 15px;
    margin-bottom: 10px;
  }
  
  .user-card-header, .user-card-body, .user-card-footer {
    padding: 15px;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}

@media (max-width: 320px) {
  .modal {
    padding: 20px;
  }
  
  h2 {
    font-size: 20px;
  }
  
  .input-container input, 
  .input-container select {
    padding-left: 32px;
  }
  
  .input-icon {
    left: 10px;
  }
}

/* Estilos para a informação de termos */
.terms-info {
  margin: 15px 0;
  font-size: 14px;
  color: #aaa;
  text-align: center;
}

.terms-link {
  color: #66ccff;
  cursor: pointer;
  text-decoration: underline;
}

.terms-link:hover {
  color: #99ddff;
}
</style>
