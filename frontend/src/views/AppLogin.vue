<template>
  <main class="login-page">
    <section class="login">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-box">
          <input
            type="email"
            v-model="email"
            placeholder=" "
            required
          />
          <label>E-mail</label>
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
import axios from "axios";
import RegisterModal from "../components/RegisterModal.vue";
import { useToast } from "vue-toastification";

export default {
  name: "AppLogin",
  components: {
    RegisterModal,
  },
  data() {
    return {
      email: "",
      password: "",
      isModalOpen: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  setup() {
    const toast = useToast();
    return { toast }; 
  },
  methods: {
    async handleLogin() {
      this.clearMessages();
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/token`,
          {
            email: this.email,
            senha: this.password,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const { access_token, token_type, nome, email } = response.data;

        if (access_token) {
          localStorage.setItem("access_token", access_token);
          localStorage.setItem("token_type", token_type);
          localStorage.setItem("user_name", nome);
          localStorage.setItem("user_email", email);
          const user = { nome, tipo_usuario: "comum" };
          localStorage.setItem("user", JSON.stringify(user));

          this.successMessage = "Login bem-sucedido! Redirecionando..";
          this.toast.success(this.successMessage); 

          setTimeout(() => {
            this.$router.push("/menu");
          }, 2000);
        }
      } catch (error) {
        console.error(error);

        if (error.response?.status === 401) {
          this.errorMessage = "Credenciais inválidas! Verifique seu e-mail e senha.";
          this.toast.error(this.errorMessage); 
        } else {
          this.errorMessage = "Erro ao tentar fazer login. Tente novamente mais tarde.";
          this.toast.error(this.errorMessage); 
        }
      }
    },
    async handleSignup(userData) {
      this.clearMessages();
      try {
        await axios.post(`${process.env.VUE_APP_API_URL}/usuarios/`, {
          ...userData,
          tipo_usuario: "comum",
        });

        this.successMessage = "Usuário cadastrado com sucesso! Faça login.";
        this.toast.success(this.successMessage); 
        this.closeModal();
      } catch (error) {
        console.error(error);
        this.errorMessage = "Erro ao cadastrar usuário. Por favor, tente novamente.";
        this.toast.error(this.errorMessage); 
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    clearMessages() {
      this.successMessage = "";
      this.errorMessage = "";
    },
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
