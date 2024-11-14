<template>
  <main class="login-page">
    <section class="login">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <input type="email" placeholder="E-mail" v-model="email" required />
        <input type="password" placeholder="Senha" v-model="password" required />
        <button type="submit">Entrar</button>
      </form>

      <p>Não tem conta? <span @click="openModal" class="register-link">Cadastre-se</span></p>
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </section>

    <!-- Componente de modal de cadastro -->
    <RegisterModal
      :isModalOpen="isModalOpen"
      @signup="handleSignup"
      @close-modal="closeModal"
    />
  </main>
</template>

<script>
import axios from 'axios';
import RegisterModal from '../components/RegisterModal.vue';

export default {
  name: 'AppLogin',
  components: {
    RegisterModal,
  },
  data() {
    return {
      email: '',
      password: '',
      isModalOpen: false,
      successMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/token`, {
          email: this.email,
          senha: this.password,
        });

        const { access_token, nome } = response.data;

        if (access_token) {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('user_name', nome);
        
        // Exibe a mensagem de sucesso e redireciona
        this.successMessage = 'Login bem-sucedido!';
        setTimeout(() => {
          this.successMessage = ''; // Limpa a mensagem após 3 segundos
          this.$router.push('/menu');
        }, 3000);
      } else {
        this.errorMessage = 'Erro ao salvar o token. Tente novamente.';
      }
    } catch (error) {
      console.error(error);

      if (error.response && error.response.status === 401) {
        this.errorMessage = 'Credenciais inválidas! Por favor, verifique seu e-mail e senha.';
      } else {
        this.errorMessage = 'Ocorreu um erro ao tentar fazer login. Tente novamente mais tarde.';
      }
    }
  },
    handleSignup(userData) {
      axios
        .post(`${process.env.VUE_APP_API_URL}/users/`, userData)
        .then(() => {
          this.closeModal();
          this.$router.push('/menu');
        })
        .catch((error) => {
          console.error(error);
          this.errorMessage = 'Erro ao criar o usuário. Por favor, tente novamente.';
        });
    },
    openModal() {
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
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
  align-items: center;
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
