<template>
  <main class="login-page">
    <section class="login">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-box">
          <input
            type="text"
            v-model="username"
            placeholder=" "
            required
          />
          <label>Nome de Usuário</label>
        </div>
        <div class="input-box">
          <input
            type="password"
            v-model="password"
            placeholder=" "
            required
          />
          <label>Senha</label>
        </div>
        <button type="submit">Entrar</button>
      </form>
      <p>
        Não tem conta? 
        <span @click="openModal" class="register-link">Cadastre-se</span>
      </p>
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

    const handleLogin = async () => {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/token`,
          {
            username: username.value,
            senha: password.value,
          }
        );

        console.log("Resposta completa do login:", response.data);
        
        const { access_token, token_type, nome, tipo_usuario } = response.data;
        console.log("Tipo de usuário recebido:", tipo_usuario);
        
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("token_type", token_type);
        localStorage.setItem("tipo_usuario", tipo_usuario || "comum");
        
        // Armazenando o modelo completo do usuário
        const userModel = {
          nome: nome,
          tipo_usuario: tipo_usuario || "comum",
          username: username.value
        };
        console.log("Modelo de usuário a ser salvo:", userModel);
        localStorage.setItem("user", JSON.stringify(userModel));
        console.log("LocalStorage após salvar:", localStorage.getItem("user"));

        successMessage.value = "Login bem-sucedido! Redirecionando...";
        toast.success(successMessage.value);

        // Redirecionamento com múltiplas estratégias
        setTimeout(() => {
          console.log("Redirecionando para menu...");
          try {
            // Tenta primeiro com window.location
            window.location.href = '/#/menu';
            
            // Como fallback, recarrega a página após um pequeno atraso
            setTimeout(() => {
              console.log("Recarregando a página...");
              window.location.reload();
            }, 2000);
            
          } catch (navError) {
            console.error("Erro durante navegação:", navError);
            window.location.href = '/';
          }
        }, 1000);
      } catch (error) {
        console.error("Erro ao fazer login:", error);
        errorMessage.value = "Erro ao fazer login. Verifique suas credenciais.";
        toast.error(errorMessage.value);
      }
    };

    const handleSignup = async (userData) => {
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/usuarios/`, {
          ...userData,
          tipo_usuario: "comum",
        });

        // Após o cadastro, armazenar o modelo do usuário
        const userModel = {
          nome: userData.nome,
          tipo_usuario: "comum",
          username: userData.username
        };
        localStorage.setItem("user", JSON.stringify(userModel));

        successMessage.value = "Usuário cadastrado com sucesso! Faça login.";
        toast.success(successMessage.value);
        isModalOpen.value = false;
      } catch (error) {
        console.error(error);
        errorMessage.value = "Erro ao cadastrar usuário. Por favor, tente novamente.";
        toast.error(errorMessage.value);
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
      handleLogin,
      handleSignup,
      openModal,
      closeModal,
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
  max-width: 480px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
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
  padding: 12px 10px;
  border: 1px solid #555;
  border-radius: 8px;
  background: #444;
  color: white;
  outline: none;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.input-box input:focus {
  border-color: #888;
}

.input-box input:not(:placeholder-shown) + label,
.input-box input:focus + label {
  top: -12px;
  left: 10px;
  font-size: 14px;
  color: #66ccff;
}

.input-box label {
  position: absolute;
  top: 27px;
  left: 15px;
  font-size: 16px;
  color: #bbb;
  pointer-events: none;
  transition: all 0.3s ease;
}

input {
  margin: 15px 0;
  padding: 12px 20px;
  width: 100%;
  border: 1px solid #555;
  border-radius: 8px;
  font-size: 16px;
  background-color: #444;
  color: white;
  transition: all 0.3s ease;
}

input::placeholder {
  color: #bbb;
}

input:focus {
  border-color: #888;
  box-shadow: 0 0 8px rgba(136, 136, 136, 0.7);
}

button {
  padding: 12px 20px;
  font-size: 16px;
  background-color: #555;
  color: white;
  border: 2px solid #555;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #444;
  border-color: #444;
  transform: translateY(-3px);
}

.register-link {
  color: #bbb;
  cursor: pointer;
  text-decoration: underline;
}

.register-link:hover {
  color: #888;
}

.error-message {
  color: white;
  background-color: red;
  padding: 10px;
  margin-top: 20px;
  border-radius: 5px;
  font-size: 16px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

p {
  padding-top: 35px;
}

.success-message {
  color: white;
  background-color: green;
  padding: 10px;
  margin-top: 20px;
  border-radius: 5px;
  font-size: 16px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
