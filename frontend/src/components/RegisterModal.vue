<template>
  <transition name="expand-modal">
    <div class="modal-overlay" v-if="isModalOpen">
      <div class="modal">
        <h2>Cadastro</h2>
        <form @submit.prevent="handleSignup">
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>

          <div v-else>
            <div class="form-group">
              <label for="name">Nome Completo</label>
              <input
                id="name"
                type="text"
                v-model="name"
                placeholder="Digite seu nome completo"
                required
              />
            </div>

            <div class="form-group">
              <label for="username">Nome de Usuário</label>
              <input
                id="username"
                type="text"
                v-model="username"
                placeholder="Digite seu nome de usuário"
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
                @input="checkPasswordStrength"
              />
              <div class="password-strength" :class="passwordStrengthClass">
                {{ passwordStrengthMessage }}
              </div>
            </div>

            <div class="form-group">
              <label for="confirmPassword">Repetir Senha</label>
              <input
                id="confirmPassword"
                type="password"
                v-model="confirmPassword"
                placeholder="Repita sua senha"
                required
                @input="checkPasswordMatch"
              />
              <div v-if="!passwordsMatch" class="password-error">
                As senhas não coincidem
              </div>
            </div>

            <div class="form-group">
              <label for="setor">Setor</label>
              <select v-model="setor" id="setor" required>
                <option value="Fábrica de Ração">Fábrica de Ração</option>
                <option value="Oficina">Oficina</option>
                <option value="Escritório">Escritório</option>
              </select>
            </div>

            <button type="submit" class="submit-button" :disabled="!isFormValid">Cadastrar</button>
          </div>
          <button v-if="!successMessage" @click="closeModal" class="close-modal">
            Fechar
          </button>
        </form>
      </div>
    </div>
  </transition>
</template>

<script>
import { useToast } from 'vue-toastification';

export default {
  props: {
    isModalOpen: Boolean,
  },
  data() {
    return {
      name: "",
      username: "",
      signupEmail: "",
      signupPassword: "",
      confirmPassword: "",
      setor: "Escritório",
      successMessage: "",
      passwordStrength: 0,
      passwordStrengthMessage: "",
      passwordsMatch: true
    };
  },
  computed: {
    passwordStrengthClass() {
      return {
        'weak': this.passwordStrength < 2,
        'medium': this.passwordStrength === 2,
        'strong': this.passwordStrength > 2
      };
    },
    isFormValid() {
      return this.name && 
             this.username && 
             this.signupEmail && 
             this.signupPassword && 
             this.confirmPassword && 
             this.passwordsMatch;
    }
  },
  setup() {
    const toast = useToast(); 
    return { toast }; 
  },
  methods: {
    checkPasswordStrength() {
      let strength = 0;
      let message = "Senha fraca";

      // Verifica comprimento
      if (this.signupPassword.length >= 8) strength++;
      
      // Verifica se contém números
      if (/\d/.test(this.signupPassword)) strength++;
      
      // Verifica se contém letras maiúsculas e minúsculas
      if (/[a-z]/.test(this.signupPassword) && /[A-Z]/.test(this.signupPassword)) strength++;
      
      // Verifica se contém caracteres especiais
      if (/[!@#$%^&*(),.?":{}|<>]/.test(this.signupPassword)) strength++;

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

      this.passwordStrength = strength;
      this.passwordStrengthMessage = message;
    },
    checkPasswordMatch() {
      this.passwordsMatch = this.signupPassword === this.confirmPassword;
    },
    handleSignup() {
      if (this.isFormValid) {
        this.$emit("signup", {
          nome: this.name,
          username: this.username,
          email: this.signupEmail,
          senha: this.signupPassword,
          setor: this.setor,
        });
        setTimeout(() => {
          this.closeModal(); 
        }, 1000);
      } else {
        this.toast.error("Por favor, preencha todos os campos corretamente!"); 
      }
    },
    closeModal() {
      this.successMessage = ""; 
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
  backdrop-filter: blur(8px);
  transition: backdrop-filter 0.3s ease;
}

.modal {
  background-color: #2c2c2c;
  padding: 40px;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  color: white;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
  transform: scale(0.9);
  transition: transform 0.4s ease, opacity 0.4s ease;
}

h2 {
  text-align: center;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 30px;
}

label {
  font-size: 18px;
  color: #bbb;
  margin-bottom: 10px;
  display: inline-block;
}

input,
select {
  width: 100%;
  padding: 14px;
  background-color: #444;
  border: 1px solid #555;
  border-radius: 8px;
  color: white;
  font-size: 18px;
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

select {
  appearance: none;
  background-color: #444;
  color: white;
  padding: 14px;
  font-size: 18px;
  border-radius: 8px;
  border: 1px solid #555;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s ease;
}

select:focus {
  border-color: #888;
  box-shadow: 0 0 8px rgba(136, 136, 136, 0.7);
}

.submit-button {
  width: 100%;
  padding: 14px 20px;
  background-color: #555;
  border: 2px solid #555;
  border-radius: 8px;
  color: white;
  font-size: 18px;
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
  font-size: 18px;
  cursor: pointer;
  text-decoration: underline;
}

.close-modal:hover {
  color: #888;
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
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .modal {
    padding: 30px;
    max-width: 500px;
  }
  
  h2 {
    font-size: 24px;
    margin-bottom: 15px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  label {
    font-size: 16px;
  }
  
  input,
  select,
  .submit-button {
    padding: 12px;
    font-size: 16px;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .modal {
    padding: 25px;
    max-width: 90%;
  }
  
  h2 {
    font-size: 22px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-size: 15px;
  }
  
  input,
  select,
  .submit-button {
    padding: 10px;
    font-size: 15px;
  }
  
  .close-modal {
    font-size: 16px;
    margin-top: 15px;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal {
    padding: 20px;
    max-width: 95%;
  }
  
  h2 {
    font-size: 20px;
    margin-bottom: 12px;
  }
  
  .form-group {
    margin-bottom: 12px;
  }
  
  label {
    font-size: 14px;
    margin-bottom: 5px;
  }
  
  input,
  select,
  .submit-button {
    padding: 8px;
    font-size: 14px;
  }
  
  .close-modal {
    font-size: 14px;
    margin-top: 12px;
  }
}

.password-strength {
  margin-top: 5px;
  font-size: 14px;
  padding: 5px;
  border-radius: 4px;
  text-align: center;
}

.password-strength.weak {
  background-color: #ff6b6b;
  color: white;
}

.password-strength.medium {
  background-color: #ffd93d;
  color: black;
}

.password-strength.strong {
  background-color: #6bff6b;
  color: black;
}

.password-error {
  color: #ff6b6b;
  font-size: 14px;
  margin-top: 5px;
}

.submit-button:disabled {
  background-color: #666;
  cursor: not-allowed;
  transform: none;
}

.submit-button:disabled:hover {
  background-color: #666;
  transform: none;
}
</style>
