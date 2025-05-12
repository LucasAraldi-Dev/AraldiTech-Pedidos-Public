<template>
  <main class="login-page">
    <section class="login" :class="{ 'logging-in': isLoggingIn, 'success': loginSuccess, 'error': loginError }">
      <h1>Login</h1>
      
      <!-- Formulário de login -->
      <div v-if="!isLoggingIn && !loginSuccess && !loginError">
        <form @submit.prevent="startLoginProcess">
          <div class="input-box">
            <input
              type="text"
              v-model="username"
              placeholder=" "
              required
              :disabled="isLoggingIn"
            />
            <label>Nome de Usuário</label>
            <div class="input-icon">
              <i class="fa-user"></i>
            </div>
          </div>
          <div class="input-box">
            <input
              type="password"
              v-model="password"
              placeholder=" "
              required
              :disabled="isLoggingIn"
            />
            <label>Senha</label>
            <div class="input-icon">
              <i class="fa-lock"></i>
            </div>
          </div>
          <button type="submit" :disabled="isLoggingIn">Entrar</button>
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
        <div class="spinner"></div>
        <div class="status-message">{{ statusMessage }}</div>
      </div>

      <!-- Estado de sucesso no login -->
      <div v-if="loginSuccess" class="login-success">
        <div class="success-icon">✓</div>
        <div class="success-message">Login realizado com sucesso!</div>
        <p class="redirect-message">Você será redirecionado em instantes...</p>
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>
      </div>
      
      <!-- Estado de erro no login -->
      <div v-if="loginError" class="login-error">
        <div class="error-icon">
          <span>!</span>
        </div>
        <div class="error-title">{{ errorTitle }}</div>
        <div class="error-message">{{ errorMessage }}</div>
        <div class="error-help">{{ errorHelp }}</div>
        <div class="error-actions">
          <button @click="resetLogin" class="retry-button">Tentar novamente</button>
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
import { ref } from "vue";

export default {
  name: "AppLogin",
  components: {
    RegisterModal,
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
    const loginSuccess = ref(false);
    const currentStep = ref(0);
    const statusMessage = ref("");
    
    // Estados para tratamento de erros
    const loginError = ref(false);
    const errorType = ref(""); // "credentials" ou "connection"
    const errorTitle = ref("");
    const errorHelp = ref("");

    const startLoginProcess = async () => {
      if (!username.value || !password.value) {
        toast.error("Por favor, preencha todos os campos.");
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
        
        // Aguarda 1.5 segundos antes de fazer a requisição real (apenas para efeito de UI)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/token`,
          {
            username: username.value,
            senha: password.value,
          }
        );

        console.log("Resposta completa do login:", response.data);
        
        const { access_token, token_type, nome, tipo_usuario, primeiro_login } = response.data;
        console.log("Tipo de usuário recebido:", tipo_usuario);
        console.log("Primeiro login:", primeiro_login);
        
        // Armazenar informações de autenticação
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("token_type", token_type);
        localStorage.setItem("tipo_usuario", tipo_usuario || "comum");
        
        // Armazenando o modelo completo do usuário
        const userModel = {
          nome: nome,
          tipo_usuario: tipo_usuario || "comum",
          username: username.value,
          primeiro_login: primeiro_login
        };
        
        console.log("Modelo de usuário a ser salvo:", userModel);
        localStorage.setItem("user", JSON.stringify(userModel));
        console.log("LocalStorage após salvar:", localStorage.getItem("user"));

        // Verificar se é a primeira vez que o usuário faz login
        const shouldShowTutorial = userModel.tipo_usuario === 'comum' && primeiro_login;

        // Mostrar tela de sucesso
        isLoggingIn.value = false;
        loginSuccess.value = true;
        
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
      } catch (error) {
        console.error("Erro ao fazer login:", error);
        isLoggingIn.value = false;
        
        // Verificar se é erro de credenciais ou conexão
        if (error.response) {
          // O servidor respondeu com código de erro
          if (error.response.status === 401 || error.response.status === 403) {
            // Erro de credenciais
            showCredentialError();
          } else {
            // Outro erro do servidor
            showServerError(error.response.status);
          }
        } else if (error.request) {
          // Sem resposta do servidor (erro de conexão)
          showConnectionError();
        } else {
          // Erro na configuração da requisição
          showGenericError();
        }
      }
    };
    
    // Funções para mostrar diferentes tipos de erro
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
      errorTitle.value = "Não foi possível conectar ao servidor";
      errorMessage.value = "Verifique sua conexão com a internet ou se o servidor está disponível.";
      errorHelp.value = "Tente novamente em alguns instantes. Se o problema persistir, entre em contato com o suporte.";
    };
    
    const showServerError = (statusCode) => {
      loginError.value = true;
      errorType.value = "server";
      errorTitle.value = "Erro no servidor";
      errorMessage.value = `O servidor retornou um erro (código ${statusCode}).`;
      errorHelp.value = "Tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte.";
    };
    
    const showGenericError = () => {
      loginError.value = true;
      errorType.value = "generic";
      errorTitle.value = "Erro desconhecido";
      errorMessage.value = "Ocorreu um erro durante o processo de login.";
      errorHelp.value = "Tente novamente. Se o problema persistir, atualize a página ou entre em contato com o suporte.";
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
      loginSuccess,
      currentStep,
      statusMessage,
      // Estados para tratamento de erros
      loginError,
      errorType,
      errorTitle,
      errorHelp,
      resetLogin,
      tryOfflineMode
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
  padding: 40px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 550px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
  position: relative;
  overflow: hidden;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
}

.input-box {
  position: relative;
  margin-bottom: 20px;
  width: 100%;
}

.input-box input {
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

.input-box input:focus {
  border-color: #66ccff;
  box-shadow: 0 0 8px rgba(102, 204, 255, 0.3);
}

.input-box input:not(:placeholder-shown) + label,
.input-box input:focus + label {
  top: -10px;
  left: 45px;
  font-size: 12px;
  background-color: #444;
  padding: 0 5px;
  color: #66ccff;
}

.input-box label {
  position: absolute;
  top: 16px;
  left: 45px;
  font-size: 16px;
  color: #bbb;
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-icon {
  position: absolute;
  top: 14px;
  left: 15px;
  font-size: 18px;
  color: #bbb;
  pointer-events: none;
}

.input-icon i::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
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

button {
  padding: 14px 20px;
  font-size: 16px;
  background-color: #555;
  color: white;
  border: 2px solid #555;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 0.5px;
}

button:hover {
  background-color: #444;
  border-color: #444;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

button:active {
  transform: translateY(-1px);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
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
  padding-top: 35px;
}

/* Estilos para o processo de login */
.auth-progress {
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
.login-success {
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
  animation: scaleIn 0.5s ease forwards;
  transform: scale(0);
}

@keyframes scaleIn {
  to { transform: scale(1); }
}

.success-message {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #00cc66;
}

.redirect-message {
  color: #bbb;
  margin-bottom: 20px;
  font-size: 15px;
  padding-top: 0;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: #444;
  border-radius: 2px;
  overflow: hidden;
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
  display: flex;
  gap: 10px;
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

.offline-button {
  flex: 1;
  background-color: transparent;
  border: 1px solid #555;
  color: #ddd;
  margin: 0;
}

.offline-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: #666;
}

/* Media queries para responsividade */
@media (min-width: 1200px) {
  .login {
    max-width: 600px;
    padding: 50px;
  }
  
  h1 {
    font-size: 28px;
    margin-bottom: 30px;
  }
  
  .input-box input {
    padding: 16px 22px;
    padding-left: 50px;
    font-size: 17px;
  }
  
  .input-icon {
    top: 16px;
    left: 18px;
  }
  
  .input-box label {
    top: 18px;
    left: 50px;
    font-size: 17px;
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    top: -12px;
    left: 50px;
    font-size: 13px;
  }
  
  button {
    padding: 16px 22px;
    font-size: 17px;
    margin-top: 15px;
  }
}

@media (max-width: 768px) {
  .login {
    padding: 30px;
    width: 95%;
    max-width: 450px;
  }
  
  .input-box input {
    padding: 12px 15px;
    padding-left: 40px;
  }
  
  .input-icon {
    top: 12px;
    left: 12px;
  }
  
  .input-box label {
    top: 14px;
    left: 40px;
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    top: -10px;
    left: 40px;
  }
}

@media (max-width: 480px) {
  .login {
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  }
  
  h1 {
    font-size: 22px;
    margin-bottom: 15px;
  }
  
  .input-box input {
    padding: 10px 8px;
    padding-left: 36px;
    font-size: 15px;
  }
  
  .input-box label {
    font-size: 15px;
    top: 12px;
    left: 36px;
  }
  
  .input-icon {
    top: 10px;
    left: 10px;
    font-size: 16px;
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    top: -10px;
    left: 36px;
    font-size: 12px;
  }
  
  button {
    padding: 10px 15px;
    font-size: 15px;
  }
  
  p {
    padding-top: 25px;
    font-size: 14px;
  }

  .progress-step {
    margin-bottom: 10px;
  }

  .step-indicator {
    width: 24px;
    height: 24px;
    font-size: 12px;
  }

  .step-label {
    font-size: 14px;
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .error-title {
    font-size: 20px;
  }
  
  .error-message {
    font-size: 15px;
  }
}

@media (max-width: 320px) {
  .login {
    padding: 20px;
  }
  
  h1 {
    font-size: 20px;
  }
  
  .input-box {
    margin-bottom: 15px;
  }
  
  .input-box input {
    padding-left: 32px;
  }
  
  .input-box label {
    left: 32px;
  }
  
  .input-box input:not(:placeholder-shown) + label,
  .input-box input:focus + label {
    left: 32px;
  }
}
</style>
