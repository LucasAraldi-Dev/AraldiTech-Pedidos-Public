<template>
  <main class="login-page">

    <section class="login" :class="{ 'logging-in': isLoggingIn, 'success': currentStep === 4, 'error': loginError }">
      <h1>Login</h1>
      
      <!-- Formulário de login -->
      <div v-if="!isLoggingIn && currentStep !== 4 && !loginError">
        <form @submit.prevent="startLoginProcess">
          <div class="input-box" :class="{'has-error': validationErrors.username}">
            <input
              type="text"
              v-model="username"
              @input="forceToLowerCase"
              @keydown="checkCapsLock"
              placeholder=" "
              required
              :disabled="isLoggingIn"
              autocapitalize="none"
            />
            <label>Nome de Usuário</label>
            <div class="input-icon">
              <i class="fa-user"></i>
            </div>
            <div class="error-message" v-if="validationErrors.username">
              {{ validationErrors.username }}
            </div>
          </div>
          <div class="input-box" :class="{'has-error': validationErrors.password}">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              @input="checkCapsLock"
              @keydown="checkCapsLock"
              @blur="clearCapsLockWarning"
              placeholder=" "
              required
              :disabled="isLoggingIn"
              autocomplete="new-password"
            />
            <label>Senha</label>
            <div class="input-icon">
              <i class="fa-lock"></i>
            </div>
            <div class="password-toggle" @click="togglePassword">
              <i :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
            </div>
            <div class="error-message" v-if="validationErrors.password">
              {{ validationErrors.password }}
            </div>
            <div class="caps-lock-warning" v-if="capsLockWarning">
              {{ capsLockWarning }}
            </div>
          </div>
          <button type="submit" :disabled="isLoggingIn" class="login-button">Entrar</button>
        </form>
        <p>
          Não tem conta? 
          <span @click="openModal" class="register-link">Cadastre-se</span>
        </p>
      </div>

      <!-- Estado de autenticação em andamento -->
      <div v-if="isLoggingIn" class="auth-progress">
        <div class="progress-steps">
          <div class="progress-step" :class="{ 'active': currentStep >= 1, 'completed': currentStep > 1 }">
            <div class="step-indicator">1</div>
            <div class="step-label">Verificando credenciais</div>
          </div>
          <div class="progress-step" :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
            <div class="step-indicator">2</div>
            <div class="step-label">Autenticando</div>
          </div>
          <div class="progress-step" :class="{ 'active': currentStep >= 3, 'completed': currentStep > 3 }">
            <div class="step-indicator">3</div>
            <div class="step-label">Carregando suas informações</div>
          </div>
        </div>
        <div class="loader-container">
          <template v-if="currentStep < 4">
            <LoadingIndicator message="" size="medium" />
            <div class="status-message">{{ statusMessage }}</div>
          </template>
          <template v-else>
            <div class="success-icon">✓</div>
            <div class="success-message">Login realizado com sucesso!</div>
            <div class="redirect-message">Você será redirecionado em instantes...</div>
            <div class="progress-bar">
              <div class="progress-fill"></div>
            </div>
          </template>
        </div>
      </div>

      <!-- Estado de erro no login -->
      <div v-if="loginError" class="login-error" :data-error-type="errorType">
        <div class="error-icon">
          <!-- Ícones diferentes para cada tipo de erro -->
          <span v-if="errorType === 'user_not_found'">?</span>
          <span v-else-if="errorType === 'wrong_password'">!</span>
          <span v-else-if="errorType === 'account_blocked'">&#x1F512;</span> <!-- Cadeado -->
          <span v-else-if="errorType === 'connection' || errorType === 'network' || errorType === 'timeout'">&#x1F50C;</span> <!-- Plugue -->
          <span v-else-if="errorType === 'server'">&#x1F6A7;</span> <!-- Construção -->
          <span v-else-if="errorType === 'too_many_attempts'">&#x23F0;</span> <!-- Relógio -->
          <span v-else>!</span>
        </div>
        <div class="error-title">{{ errorTitle }}</div>
        <div class="error-message">{{ errorMessage }}</div>
        <div class="error-help">{{ errorHelp }}</div>
        <div class="error-actions">
          <button @click="resetLogin" class="retry-button">Tentar novamente</button>
          <button v-if="errorType === 'wrong_password'" @click="togglePasswordVisibility" class="action-button">
            {{ showPassword ? 'Ocultar senha' : 'Mostrar senha' }}
          </button>
          <button v-if="errorType === 'connection'" @click="tryOfflineMode" class="offline-button">Modo offline</button>
        </div>
      </div>
    </section>

    <!-- Modal de Cadastro -->
    <RegisterModal
      :isModalOpen="isModalOpen"
      @signup="handleSignup"
      @close-modal="closeModal"
    />
  </main>
</template>

<script>
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import RegisterModal from "../components/RegisterModal.vue";
import { useToast } from "vue-toastification";
import { ref, onMounted } from "vue";
import { validateText } from "../utils/validationService";
import { initCsrfProtection, ensureCsrfToken } from "../utils/securityService";
import LoadingIndicator from "../components/ui/LoadingIndicator.vue";
import authService from '../api/authService';

export default {
  name: "AppLogin",
  components: {
    RegisterModal,
    LoadingIndicator,
  },
  setup() {
    const toast = useToast();
    const username = ref("");
    const password = ref("");
    const isModalOpen = ref(false);
    const successMessage = ref("");
    const errorMessage = ref("");
    
    // Estados para o fluxo de login
    const isLoggingIn = ref(false);
    const currentStep = ref(0);
    const statusMessage = ref("");
    
    // Estados para tratamento de erros
    const loginError = ref(false);
    const errorType = ref(""); // "credentials" ou "connection"
    const errorTitle = ref("");
    const errorHelp = ref("");
    
    // Estado para validação de campos
    const validationErrors = ref({
      username: "",
      password: ""
    });
    
    // Inicializar proteção CSRF ao montar o componente
    onMounted(async () => {
      try {
        // Inicializar proteção CSRF
        await initCsrfProtection();
      } catch (error) {
        console.error("Falha ao inicializar proteção CSRF:", error);
      }
    });
    
    // Função para validar formulário antes de enviar
    const validateForm = () => {
      // Resetar erros de validação
      validationErrors.value = {
        username: "",
        password: ""
      };
      
      // Validar usuário
      const userValidation = validateText(username.value, {
        required: true,
        minLength: 3,
        fieldName: "Nome de usuário"
      });
      
      // Validar senha
      const passValidation = validateText(password.value, {
        required: true,
        minLength: 6,
        fieldName: "Senha"
      });
      
      // Atualizar mensagens de erro
      if (!userValidation.isValid) {
        validationErrors.value.username = userValidation.message;
      }
      
      if (!passValidation.isValid) {
        validationErrors.value.password = passValidation.message;
      }
      
      return userValidation.isValid && passValidation.isValid;
    };

    const startLoginProcess = async () => {
      // Validar formulário antes de prosseguir
      if (!validateForm()) {
        // Mostrar mensagens de erro para o usuário
        if (validationErrors.value.username) {
          toast.error(validationErrors.value.username);
        }
        if (validationErrors.value.password) {
          toast.error(validationErrors.value.password);
        }
        return;
      }
      
      isLoggingIn.value = true;
      currentStep.value = 1;
      statusMessage.value = "Verificando suas credenciais...";
      
      // Simulação de verificação inicial (1 segundo)
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      try {
        currentStep.value = 2;
        statusMessage.value = "Autenticando...";
        
        // Garantir que temos um token CSRF válido antes do login
        await ensureCsrfToken();
        
        // Aguarda 1.5 segundos antes de fazer a requisição real (apenas para efeito de UI)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Usar o authService para fazer login com segurança
        const result = await authService.login(username.value, password.value);
        
        if (!result.success) {
          throw new Error(result.error || "Falha na autenticação");
        }
        
        // Obter dados do usuário logado
        const userData = authService.getUser();
        console.log("Usuário autenticado:", userData);
        
        // Para compatibilidade com código existente
        const nome = userData.nome;
        const tipo_usuario = userData.tipo_usuario;
        const primeiro_login = userData.primeiro_login;
        
        // Verificar se é a primeira vez que o usuário faz login
        const shouldShowTutorial = userData.tipo_usuario === 'comum' && primeiro_login;

        // Registrar dados do usuário no log (para uso das variáveis)
        console.log(`Usuário: ${nome}, Tipo: ${tipo_usuario}`);

        // Avançar para o passo 3 e aguardar mais 1 segundo
        currentStep.value = 3;
        statusMessage.value = "Carregando suas informações...";
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mostrar mensagem de sucesso no fluxo de login
        currentStep.value = 4;
        
        // Redirecionar para o Menu com parâmetro para abrir o tutorial (se necessário)
        setTimeout(() => {
          try {
            if (shouldShowTutorial) {
              window.location.href = '/#/menu?firstLogin=true';
            } else {
              window.location.href = '/#/menu';
            }
          } catch (navError) {
            console.error("Erro durante navegação:", navError);
            window.location.href = '/';
          }
        }, 3000);

        // Após login bem-sucedido:
        await initCsrfProtection();
      } catch (error) {
        console.error("Erro ao fazer login:", error);
        isLoggingIn.value = false;
        
        // Verificar se é erro de credenciais ou conexão
        if (error.response) {
          // O servidor respondeu com código de erro
          if (error.response.status === 401 || error.response.status === 403) {
            // Erro de credenciais - verificar mensagens específicas
            if (error.response.data?.detail) {
              if (error.response.data.detail.includes("não existe")) {
                showUserNotFoundError();
              } else if (error.response.data.detail.includes("senha incorreta") || 
                         error.response.data.detail.includes("inválida")) {
                showWrongPasswordError();
              } else if (error.response.data.detail.includes("bloqueado") || 
                         error.response.data.detail.includes("desativado")) {
                showAccountBlockedError();
              } else {
                // Erro genérico de credenciais
                showCredentialError();
              }
            } else {
              showCredentialError();
            }
          } else if (error.response.status === 429) {
            // Muitas tentativas
            showTooManyAttemptsError();
          } else if (error.response.status >= 500) {
            // Erro de servidor
            showServerError(error.response.status, error.response.data?.detail);
          } else {
            // Outro erro do servidor
            showServerError(error.response.status, error.response.data?.detail);
          }
        } else if (error.request) {
          // Sem resposta do servidor (erro de conexão)
          showConnectionError();
        } else if (error.message && error.message.includes("timeout")) {
          // Timeout na requisição
          showTimeoutError();
        } else if (error.message && error.message.includes("Network Error")) {
          // Erro específico de rede
          showNetworkError();
        } else {
          // Erro na configuração da requisição
          showGenericError(error.message);
        }
      }
    };
    
    // Funções para mostrar diferentes tipos de erro
    const showUserNotFoundError = () => {
      loginError.value = true;
      errorType.value = "user_not_found";
      errorTitle.value = "Usuário não encontrado";
      errorMessage.value = "O nome de usuário informado não existe no sistema.";
      errorHelp.value = "Verifique se digitou o nome de usuário corretamente. Se você é novo, cadastre-se clicando em 'Cadastre-se' abaixo.";
    };
    
    const showWrongPasswordError = () => {
      loginError.value = true;
      errorType.value = "wrong_password";
      errorTitle.value = "Senha incorreta";
      errorMessage.value = "A senha informada está incorreta.";
      errorHelp.value = "Verifique se a tecla CAPS LOCK está ativada e tente novamente. Se você esqueceu sua senha, entre em contato com o administrador.";
    };
    
    const showAccountBlockedError = () => {
      loginError.value = true;
      errorType.value = "account_blocked";
      errorTitle.value = "Conta bloqueada";
      errorMessage.value = "Sua conta está bloqueada ou desativada.";
      errorHelp.value = "Entre em contato com o administrador do sistema para reativar sua conta.";
    };
    
    const showTooManyAttemptsError = () => {
      loginError.value = true;
      errorType.value = "too_many_attempts";
      errorTitle.value = "Muitas tentativas de login";
      errorMessage.value = "Você excedeu o número de tentativas de login permitidas.";
      errorHelp.value = "Por segurança, aguarde alguns minutos antes de tentar novamente.";
    };
    
    const showTimeoutError = () => {
      loginError.value = true;
      errorType.value = "timeout";
      errorTitle.value = "Tempo de conexão esgotado";
      errorMessage.value = "O servidor demorou muito para responder.";
      errorHelp.value = "Verifique sua conexão com a internet ou se o servidor está sobrecarregado. Tente novamente em alguns instantes.";
    };
    
    const showNetworkError = () => {
      loginError.value = true;
      errorType.value = "network";
      errorTitle.value = "Erro de rede";
      errorMessage.value = "Não foi possível estabelecer conexão com a rede.";
      errorHelp.value = "Verifique sua conexão Wi-Fi ou de dados móveis e tente novamente.";
    };
    
    const showCredentialError = () => {
      loginError.value = true;
      errorType.value = "credentials";
      errorTitle.value = "Credenciais inválidas";
      errorMessage.value = "O nome de usuário ou senha estão incorretos.";
      errorHelp.value = "Verifique suas informações e tente novamente. Esqueceu sua senha? Entre em contato com o administrador.";
    };
    
    const showConnectionError = () => {
      loginError.value = true;
      errorType.value = "connection";
      errorTitle.value = "Falha na conexão";
      errorMessage.value = "Não foi possível conectar ao servidor.";
      errorHelp.value = "Verifique sua conexão com a internet, as configurações de firewall ou se o servidor está disponível.";
    };
    
    const showServerError = (statusCode, detail) => {
      loginError.value = true;
      errorType.value = "server";
      errorTitle.value = "Erro no servidor";
      
      if (statusCode === 500) {
        errorMessage.value = "Erro interno no servidor.";
        errorHelp.value = "O servidor encontrou um problema ao processar sua solicitação. Por favor, tente novamente mais tarde.";
      } else if (statusCode === 503) {
        errorMessage.value = "Serviço temporariamente indisponível.";
        errorHelp.value = "O servidor está em manutenção ou sobrecarregado. Por favor, tente novamente mais tarde.";
      } else if (statusCode === 502) {
        errorMessage.value = "Erro de comunicação interna.";
        errorHelp.value = "Ocorreu um problema na comunicação entre servidores. Por favor, tente novamente.";
      } else {
        errorMessage.value = `O servidor retornou um erro (código ${statusCode}).`;
        errorHelp.value = detail ? `Detalhes: ${detail}` : "Tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte.";
      }
    };
    
    const showGenericError = (message) => {
      loginError.value = true;
      errorType.value = "generic";
      errorTitle.value = "Erro no login";
      errorMessage.value = "Ocorreu um erro inesperado durante o processo de login.";
      errorHelp.value = message ? `Detalhes: ${message}` : "Tente novamente. Se o problema persistir, atualize a página ou entre em contato com o suporte.";
    };
    
    // Função para reiniciar o processo de login
    const resetLogin = () => {
      loginError.value = false;
      errorType.value = "";
      errorTitle.value = "";
      errorMessage.value = "";
      errorHelp.value = "";
    };
    
    // Função para tentar modo offline (implementação básica)
    const tryOfflineMode = () => {
      toast.info("Modo offline não disponível nesta versão do sistema.");
      // Aqui você poderia implementar lógica para armazenar dados localmente
      // e sincronizar quando a conexão voltar
    };

    const handleSignup = async (userData, callback) => {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/usuarios/`,
          userData
        );
        
        console.log("Usuário cadastrado com sucesso:", response.data);
        
        // Chamar o callback com sucesso se existir
        if (typeof callback === 'function') {
          callback(true);
        }
        
        // Não exibir toast aqui, já que o card de sucesso no RegisterModal 
        // mostrará as informações do usuário cadastrado
        // O modal permanecerá aberto até que o usuário escolha fechá-lo
        // ou clicar em "Fazer Login"
      } catch (error) {
        console.error("Erro ao cadastrar usuário:", error);
        
        // Chamar o callback com erro se existir
        if (typeof callback === 'function') {
          const errorMessage = error.response?.data?.detail || "Erro na conexão com o servidor";
          callback(false, new Error(errorMessage));
        }
        
        // Exibir mensagem de erro usando toast
        toast.error(error.response?.data?.detail || "Erro ao cadastrar usuário. Por favor, tente novamente.");
        // Não fechar o modal em caso de erro para permitir nova tentativa
      }
    };

    const openModal = () => {
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
    };

    const forceToLowerCase = () => {
      username.value = username.value.toLowerCase();
    };

    const showPassword = ref(false);
    const togglePassword = () => {
      showPassword.value = !showPassword.value;
    };

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    // Alerta para CAPS LOCK
    const capsLockWarning = ref("");
    
    const checkCapsLock = (event) => {
      const isCapsLockOn = event.getModifierState && event.getModifierState('CapsLock');
      if (isCapsLockOn) {
        capsLockWarning.value = "CAPS LOCK está ativado";
      } else {
        capsLockWarning.value = "";
      }
    };
    
    // Limpar alerta quando o foco é removido
    const clearCapsLockWarning = () => {
      setTimeout(() => {
        capsLockWarning.value = "";
      }, 1000);
    };

    return {
      username,
      password,
      isModalOpen,
      successMessage,
      errorMessage,
      startLoginProcess,
      handleSignup,
      openModal,
      closeModal,
      // Estados para o fluxo de login
      isLoggingIn,
      currentStep,
      statusMessage,
      // Estados para tratamento de erros
      loginError,
      errorType,
      errorTitle,
      errorHelp,
      resetLogin,
      tryOfflineMode,
      // Estado para validação de campos
      validationErrors,
      forceToLowerCase,
      showPassword,
      togglePassword,
      togglePasswordVisibility,
      // Alerta para CAPS LOCK
      capsLockWarning,
      checkCapsLock,
      clearCapsLockWarning
    };
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  background-color: #2c2c2c;
}

.login {
  padding: var(--spacing-xl);
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: white;
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 34.375rem; /* Convertido de 550px para rem */
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
}

h1 {
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-xl);
  font-weight: 600;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
}

.input-box {
  position: relative;
  margin-bottom: var(--spacing-md);
  width: 100%;
}

.input-box input {
  width: 100%;
  padding: 0.875rem 1.25rem;
  padding-left: 2.8125rem; /* Convertido de 45px para rem */
  padding-right: 2.8125rem; /* Espaço para o botão de mostrar/ocultar senha */
  border: 1px solid #555;
  border-radius: var(--border-radius-md);
  background: #444;
  color: white;
  outline: none;
  font-size: var(--font-size-md);
  transition: all 0.3s ease;
}

.input-box input:focus {
  border-color: #66ccff;
  box-shadow: 0 0 0.5rem rgba(102, 204, 255, 0.3);
}

.input-box input:not(:placeholder-shown) + label,
.input-box input:focus + label {
  top: -0.625rem; /* Convertido de -10px para rem */
  left: 2.8125rem; /* Convertido de 45px para rem */
  font-size: 0.75rem; /* Convertido de 12px para rem */
  background-color: #444;
  padding: 0 0.3125rem; /* Convertido de 5px para rem */
  color: #66ccff;
}

.input-box label {
  position: absolute;
  top: 1rem; /* Convertido de 16px para rem */
  left: 2.8125rem; /* Convertido de 45px para rem */
  font-size: var(--font-size-md);
  color: #bbb;
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-icon {
  position: absolute;
  top: 0.875rem; /* Convertido de 14px para rem */
  left: 0.9375rem; /* Convertido de 15px para rem */
  font-size: 1.125rem; /* Convertido de 18px para rem */
  color: #bbb;
  pointer-events: none;
}

.input-icon i::before {
  content: '';
  display: inline-block;
  width: 1.125rem; /* Convertido de 18px para rem */
  height: 1.125rem; /* Convertido de 18px para rem */
  background-size: contain;
  background-repeat: no-repeat;
}

.input-icon .fa-user::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM12 5c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-icon .fa-lock::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z' fill='%23bbb'/%3E%3C/svg%3E");
}

.input-box input:focus + label + .input-icon i::before {
  filter: brightness(1.5);
}

button, .login-button {
  padding: 0.875rem 1.25rem; /* Convertido de 14px 20px para rem */
  font-size: var(--font-size-md);
  background-color: #555;
  color: white;
  border: 2px solid #555;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  width: 100%;
  margin-top: 0.625rem; /* Convertido de 10px para rem */
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

button:hover, .login-button:hover {
  background-color: #444;
  border-color: #444;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

button:active, .login-button:active {
  transform: translateY(-1px);
}

button:disabled, .login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

button:after, .login-button:after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.3);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

button:focus:not(:active)::after, .login-button:focus:not(:active)::after {
  animation: ripple 1s ease-out;
}

.register-link {
  color: #bbb;
  cursor: pointer;
  text-decoration: underline;
}

.register-link:hover {
  color: #888;
}

p {
  padding-top: 2.1875rem; /* Convertido de 35px para rem */
}

/* Estilos para o botão de mostrar/ocultar senha */
.password-toggle {
  position: absolute;
  top: 0.875rem; /* 14px */
  right: 0.9375rem; /* 15px */
  cursor: pointer;
  color: #bbb;
  transition: all 0.3s ease;
  z-index: 2;
}

.password-toggle:hover {
  color: #66ccff;
}

.password-toggle i::before {
  content: '';
  display: inline-block;
  width: 1.125rem; /* 18px */
  height: 1.125rem; /* 18px */
  background-size: contain;
  background-repeat: no-repeat;
}

.password-toggle .fa-eye::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 6c-5.33 0-9.6 3.33-11.4 8 1.8 4.67 6.07 8 11.4 8 5.33 0 9.6-3.33 11.4-8-1.8-4.67-6.07-8-11.4-8zm0 13c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z' fill='%23bbb'/%3E%3C/svg%3E");
}

.password-toggle .fa-eye-slash::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 6c-5.33 0-9.6 3.33-11.4 8 1.8 4.67 6.07 8 11.4 8 5.33 0 9.6-3.33 11.4-8-1.8-4.67-6.07-8-11.4-8zm0 13c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z' fill='%23bbb'/%3E%3Cline x1='3' y1='3' x2='21' y2='21' stroke='%23bbb' stroke-width='2'/%3E%3C/svg%3E");
}

/* Melhorias para mensagens de erro humanizadas nos campos */
.input-box .error-message {
  position: absolute;
  bottom: -1.5rem;
  left: 0;
  font-size: 0.75rem;
  color: #ff5b5b;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(-0.5rem);
}

.input-box.has-error .error-message {
  opacity: 1;
  transform: translateY(0);
}

.input-box.has-error input {
  border-color: #ff5b5b;
  box-shadow: 0 0 0.5rem rgba(255, 91, 91, 0.3);
}

@keyframes ripple {
  0% { transform: scale(0, 0); opacity: 0.5; }
  20% { transform: scale(25, 25); opacity: 0.3; }
  100% { opacity: 0; transform: scale(40, 40); }
}

/* Otimizar animações de transição de estados */
.auth-progress, .login-error, .success-icon {
  animation: fadeInUp 0.5s forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Melhorias no feedback visual de erros */
.error-title {
  position: relative;
  display: inline-block;
  padding-left: 1.75rem;
  margin-bottom: 1rem;
}

.error-title:before {
  content: "!";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  line-height: 1.25rem;
  text-align: center;
  background: #ff3d71;
  color: white;
  border-radius: 50%;
  font-weight: bold;
}

/* Melhorar o espaçamento e legibilidade das mensagens de erro */
.error-help {
  background: rgba(255, 255, 255, 0.05);
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.5rem;
  line-height: 1.4;
}

/* Estilos para o processo de login */
.auth-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-top: 0.625rem;
}

.progress-steps {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 25rem;
  margin-bottom: 1.25rem;
}

.progress-step {
  display: flex;
  align-items: center;
  margin-bottom: 0.9375rem;
  opacity: 0.6;
  transition: all 0.3s ease;
}

.progress-step.active {
  opacity: 1;
}

.progress-step.completed {
  opacity: 0.9;
}

.step-indicator {
  width: 1.75rem; /* Convertido de 28px para rem */
  height: 1.75rem; /* Convertido de 28px para rem */
  border-radius: 50%;
  background: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 0.625rem; /* Convertido de 10px para rem */
}

.progress-step.active .step-indicator {
  background: #66ccff;
  box-shadow: 0 0 0.625rem rgba(102, 204, 255, 0.5); /* Convertido de 10px para rem */
}

.progress-step.completed .step-indicator {
  background: #00cc66;
}

.step-label {
  font-size: 0.9375rem; /* Convertido de 15px para rem */
}

.spinner {
  width: 3.125rem; /* Convertido de 50px para rem */
  height: 3.125rem; /* Convertido de 50px para rem */
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top: 4px solid #66ccff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 1.25rem 0; /* Convertido de 20px para rem */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.status-message {
  font-size: var(--font-size-md);
  text-align: center;
  color: #ddd;
  margin-top: 0.625rem; /* Convertido de 10px para rem */
}

/* Estilos para o estado de sucesso */
.success-icon {
  width: 4.375rem; /* 70px */
  height: 4.375rem; /* 70px */
  background: #00cc66;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem; /* 40px */
  margin: 1.25rem auto; /* 20px */
  box-shadow: 0 5px 15px rgba(0, 204, 102, 0.4);
  animation: scaleIn 0.5s ease forwards;
  transform: scale(0);
}

@keyframes scaleIn {
  to { transform: scale(1); }
}

.success-message {
  font-size: 1.375rem; /* 22px */
  font-weight: 600;
  margin-bottom: 0.9375rem; /* 15px */
  color: #00cc66;
}

.redirect-message {
  color: #bbb;
  margin-bottom: 1.25rem; /* 20px */
  font-size: 0.9375rem; /* 15px */
  padding-top: 0;
}

.progress-bar {
  width: 100%;
  height: 0.25rem; /* 4px */
  background: #444;
  border-radius: 0.125rem; /* 2px */
  overflow: hidden;
  max-width: 18.75rem; /* 300px */
  margin: 0 auto;
}

.progress-fill {
  height: 100%;
  background: #00cc66;
  animation: fill 3s linear forwards;
  width: 0;
}

@keyframes fill {
  to { width: 100%; }
}

/* Estilos para o estado de erro */
.login-error {
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
  width: 4.375rem; /* 70px */
  height: 4.375rem; /* 70px */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem; /* 40px */
  font-weight: bold;
  margin-bottom: 1.25rem; /* 20px */
  box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4);
  animation: pulseError 2s infinite;
}

/* Cores diferenciadas para os diferentes tipos de erro */
.error-icon {
  background: #ff3d71; /* Cor padrão para erros */
}

/* Cores para tipos específicos de erro */
.login-error[data-error-type="user_not_found"] .error-icon {
  background: #e95c00; /* Laranja para usuário não encontrado */
  box-shadow: 0 5px 15px rgba(233, 92, 0, 0.4);
}

.login-error[data-error-type="wrong_password"] .error-icon {
  background: #ff3d71; /* Vermelho para senha incorreta */
  box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4);
}

.login-error[data-error-type="account_blocked"] .error-icon {
  background: #ca294a; /* Vermelho escuro para conta bloqueada */
  box-shadow: 0 5px 15px rgba(202, 41, 74, 0.4);
}

.login-error[data-error-type="connection"] .error-icon,
.login-error[data-error-type="network"] .error-icon,
.login-error[data-error-type="timeout"] .error-icon {
  background: #3366ff; /* Azul para erros de conexão */
  box-shadow: 0 5px 15px rgba(51, 102, 255, 0.4);
}

.login-error[data-error-type="server"] .error-icon {
  background: #8252d6; /* Roxo para erros de servidor */
  box-shadow: 0 5px 15px rgba(130, 82, 214, 0.4);
}

.login-error[data-error-type="too_many_attempts"] .error-icon {
  background: #aa7a1c; /* Amarelo escuro para muitas tentativas */
  box-shadow: 0 5px 15px rgba(170, 122, 28, 0.4);
}

@keyframes pulseError {
  0% { transform: scale(1); box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4); }
  50% { transform: scale(1.05); box-shadow: 0 5px 25px rgba(255, 61, 113, 0.6); }
  100% { transform: scale(1); box-shadow: 0 5px 15px rgba(255, 61, 113, 0.4); }
}

.error-title {
  font-size: 1.375rem; /* Convertido de 22px para rem */
  font-weight: 600;
  margin-bottom: 0.625rem; /* Convertido de 10px para rem */
  color: #ff3d71;
}

.error-message {
  color: #ddd;
  font-size: var(--font-size-md);
  margin-bottom: 0.625rem; /* Convertido de 10px para rem */
}

.error-help {
  color: #bbb;
  font-size: 0.875rem; /* Convertido de 14px para rem */
  margin-bottom: 1.5625rem; /* Convertido de 25px para rem */
  padding: 0 0.625rem; /* Convertido de 10px para rem */
}

.error-actions {
  display: flex;
  gap: 0.625rem; /* Convertido de 10px para rem */
  width: 100%;
}

.retry-button {
  flex: 1;
  background-color: #555;
  border: 1px solid #555;
  margin: 0;
}

.retry-button:hover {
  background-color: #666;
  border-color: #666;
}

.action-button {
  flex: 1;
  background-color: #444;
  border: 1px solid #555;
  color: #ddd;
  margin: 0;
}

.action-button:hover {
  background-color: #505050;
  border-color: #666;
  transform: translateY(-3px);
}

.offline-button {
  flex: 1;
  background-color: transparent;
  border: 1px solid #555;
  color: #ddd;
  margin: 0;
}

/* Media queries para responsividade */
@media (min-width: 1200px) {
  .login {
    max-width: 37.5rem; /* Convertido de 600px para rem */
    padding: 3.125rem; /* Convertido de 50px para rem */
  }
  
  h1 {
    font-size: 1.75rem; /* Convertido de 28px para rem */
    margin-bottom: 1.875rem; /* Convertido de 30px para rem */
  }
  
  .input-box input {
    padding: 1rem 1.375rem; /* Convertido de 16px 22px para rem */
    padding-left: 3.125rem; /* Convertido de 50px para rem */
    font-size: 1.0625rem; /* Convertido de 17px para rem */
  }
  
  .input-icon {
    top: 1rem; /* Convertido de 16px para rem */
    left: 1.125rem; /* Convertido de 18px para rem */
  }
  
  .input-box label {
    top: 1.125rem; /* Convertido de 18px para rem */
    left: 3.125rem; /* Convertido de 50px para rem */
    font-size: 1.0625rem; /* Convertido de 17px para rem */
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    top: -0.75rem; /* Convertido de -12px para rem */
    left: 3.125rem; /* Convertido de 50px para rem */
    font-size: 0.8125rem; /* Convertido de 13px para rem */
  }
  
  button {
    padding: 1rem 1.375rem; /* Convertido de 16px 22px para rem */
    font-size: 1.0625rem; /* Convertido de 17px para rem */
    margin-top: 0.9375rem; /* Convertido de 15px para rem */
  }
}

@media (max-width: 768px) {
  .login {
    padding: 1.875rem; /* Convertido de 30px para rem */
    width: 95%;
    max-width: 28.125rem; /* Convertido de 450px para rem */
  }
  
  .input-box input {
    padding: 0.75rem 0.9375rem; /* Convertido de 12px 15px para rem */
    padding-left: 2.5rem; /* Convertido de 40px para rem */
  }
  
  .input-icon {
    top: 0.75rem; /* Convertido de 12px para rem */
    left: 0.75rem; /* Convertido de 12px para rem */
  }
  
  .input-box label {
    top: 0.875rem; /* Convertido de 14px para rem */
    left: 2.5rem; /* Convertido de 40px para rem */
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    top: -0.625rem; /* Convertido de -10px para rem */
    left: 2.5rem; /* Convertido de 40px para rem */
  }
}

@media (max-width: 480px) {
  .login-page {
    padding: 1rem 0.5rem;
    min-height: calc(80vh - 110px); /* Ajustar para header/footer fixos */
  }
  
  .login {
    padding: 1.25rem; /* 20px */
    margin-top: 0.625rem; /* 10px */
    margin-bottom: 0.625rem; /* 10px */
  }
  
  /* Garantir que os inputs possam ser facilmente tocados */
  .input-box input {
    padding: 0.75rem 0.75rem; /* 12px */
    padding-left: 2.5rem; /* 40px */
    padding-right: 2.5rem; /* 40px */
    min-height: 3.125rem; /* 50px */
    font-size: 1rem; /* 16px - evitar zoom no iOS */
  }
  
  .password-toggle {
    top: 1rem; /* 16px */
  }
  
  button, .login-button {
    min-height: 3.125rem; /* 50px */
    margin-top: 1rem; /* 16px */
  }
  
  .input-box .error-message {
    bottom: -1.25rem;
    font-size: 0.6875rem; /* 11px */
  }
  
  .input-box {
    margin-bottom: var(--spacing-lg); /* Espaço extra para mensagens de erro */
  }
}

@media (max-width: 360px) {
  .login {
    padding: 1rem; /* 16px */
  }
  
  h1 {
    font-size: 1.25rem; /* 20px */
    margin-bottom: 0.75rem; /* 12px */
  }
}

@media (max-width: 480px) and (max-height: 800px) {
  .login-page {
    min-height: calc(80vh - 80px);
  }
}

/* Estilos para a área do loader e mensagens */
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.25rem 0;
  min-height: 12.5rem; /* 200px */
  justify-content: center;
}

/* Animações para transições suaves entre etapas */
.loader-container > * {
  animation: fadeIn 0.4s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Estilo especial para o último passo (sucesso) */
.progress-step:last-child.completed .step-indicator {
  background: #00cc66;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 204, 102, 0.7); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(0, 204, 102, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 204, 102, 0); }
}

/* Melhora na transição entre etapas */
.progress-step {
  position: relative;
  transition: all 0.3s ease;
}

.progress-step::after {
  content: '';
  position: absolute;
  left: 0.875rem; /* 14px */
  top: 2.1875rem; /* 35px */
  height: 0;
  width: 2px;
  background-color: #666;
  transition: height 0.5s ease;
}

.progress-step:not(:last-child).active::after,
.progress-step:not(:last-child).completed::after {
  height: 1.875rem; /* 30px */
}

.progress-step.active::after {
  background-color: #66ccff;
}

.progress-step.completed::after {
  background-color: #00cc66;
}

/* Estado de sucesso integrado no fluxo */
.progress-step:last-child.completed .step-label {
  color: #00cc66;
  font-weight: bold;
}

.status-message {
  font-size: 1rem;
  text-align: center;
  color: #ddd;
  margin-top: 0.625rem; /* 10px */
  min-height: 1.5rem; /* 24px */
}

/* Estilo para o alerta de CAPS LOCK */
.caps-lock-warning {
  position: absolute;
  top: 0.75rem;
  right: 2.5rem;
  font-size: 0.75rem;
  color: #ffc107;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 0.1875rem 0.5rem;
  border-radius: 0.25rem;
  animation: fadeIn 0.3s ease-in-out;
  z-index: 5;
}

@media (max-width: 480px) {
  .caps-lock-warning {
    top: auto;
    bottom: -1.5rem;
    right: 0;
    background-color: transparent;
  }
}
</style>
