<template>
  <div class="modal-overlay" v-if="isModalOpen">
    <div class="modal">
      <h2>Cadastro</h2>
      <form @submit.prevent="handleSignup">
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <div v-else>
          <div class="form-group">
            <label for="name">Nome</label>
            <input
              id="name"
              type="text"
              v-model="name"
              placeholder="Digite seu nome"
              required
            />
          </div>

          <div class="form-group">
            <label for="signupEmail">E-mail</label>
            <input
              id="signupEmail"
              type="email"
              v-model="signupEmail"
              placeholder="Digite seu e-mail"
              required
            />
          </div>

          <div class="form-group">
            <label for="signupPassword">Senha</label>
            <input
              id="signupPassword"
              type="password"
              v-model="signupPassword"
              placeholder="Digite sua senha"
              required
            />
          </div>

          <div class="form-group">
            <label for="setor">Setor</label>
            <select v-model="setor" id="setor" required>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="Oficina">Oficina</option>
              <option value="Escritório">Escritório</option>
            </select>
          </div>

          <button type="submit" class="submit-button">Cadastrar</button>
        </div>
        <button v-if="!successMessage" @click="closeModal" class="close-modal">
          Fechar
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
export default {
  props: {
    isModalOpen: Boolean,
  },
  data() {
    return {
      name: "",
      signupEmail: "",
      signupPassword: "",
      setor: "Escritório",
      successMessage: "", 
    };
  },
  methods: {
    handleSignup() {
      const toast = useToast();
      this.$emit("signup", {
        nome: this.name,
        email: this.signupEmail,
        senha: this.signupPassword,
        setor: this.setor,
      });

      toast.success("Usuário cadastrado com sucesso!");
      setTimeout(() => {
        this.closeModal(); // Fecha o modal após exibir a mensagem
      }, 2000);
    },
    closeModal() {
      this.successMessage = ""; // Reseta a mensagem ao fechar
      this.$emit("close-modal");
    },
  },
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
  }
  
  .modal {
    background-color: #2c2c2c;
    padding: 40px;
    border-radius: 12px;
    width: 90%;
    max-width: 450px;
    color: white;
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
  }
  
  h2 {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    font-size: 14px;
    color: #bbb;
    margin-bottom: 8px;
    display: inline-block;
  }
  
  input,
  select {
    width: 100%;
    padding: 12px;
    background-color: #444;
    border: 1px solid #555;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    transition: all 0.3s ease;
  }
  
  input::placeholder,
  select {
    color: #bbb;
  }
  
  input:focus,
  select:focus {
    border-color: #888;
    box-shadow: 0 0 8px rgba(136, 136, 136, 0.7);
  }
  
  .submit-button {
    width: 100%;
    padding: 12px 20px;
    background-color: #555;
    border: 2px solid #555;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .submit-button:hover {
    background-color: #444;
    border-color: #444;
    transform: translateY(-3px);
  }
  
  .close-modal {
    display: block;
    margin: 20px auto 0;
    padding: 10px 20px;
    background-color: transparent;
    border: none;
    color: #bbb;
    font-size: 16px;
    cursor: pointer;
    text-decoration: underline;
  }
  
  .close-modal:hover {
    color: #888;
  }

  .success-message {
  color: green;
  margin-bottom: 10px;
  font-weight: bold;
}

  </style>
  