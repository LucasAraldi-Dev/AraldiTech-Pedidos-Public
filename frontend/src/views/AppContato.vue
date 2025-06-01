<template>
  <main class="contact-page">
    <section class="contact-section">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="AraldiTech" class="logo" onerror="this.src='favicon.ico'">
      </div>
      
      <h1>Entre em Contato</h1>
      <p>Envie sua mensagem e retornaremos em breve</p>
      
      <div class="form-container">
        <form @submit.prevent="enviarMensagem">
          <div class="input-box">
            <input
              type="text"
              v-model="formData.nome"
              placeholder=" "
              required
            />
            <label>Nome Completo</label>
            <div class="input-icon">
              <i class="fas fa-user"></i>
            </div>
          </div>
          
          <div class="input-box">
            <input
              type="email"
              v-model="formData.email"
              placeholder=" "
              required
            />
            <label>E-mail</label>
            <div class="input-icon">
              <i class="fas fa-envelope"></i>
            </div>
          </div>
          
          <div class="input-box">
            <input
              type="text"
              v-model="formData.assunto"
              placeholder=" "
              required
            />
            <label>Assunto</label>
            <div class="input-icon">
              <i class="fas fa-tag"></i>
            </div>
          </div>
          
          <div class="input-box textarea">
            <textarea
              v-model="formData.mensagem"
              placeholder=" "
              required
              rows="5"
            ></textarea>
            <label>Mensagem</label>
            <div class="input-icon">
              <i class="fas fa-comment-alt"></i>
            </div>
          </div>
          
          <button type="submit" class="btn-submit">Enviar Mensagem</button>
        </form>
        
        <div class="contact-info">
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-phone-alt"></i>
            </div>
            <div class="info-text">
              <h3>Telefone</h3>
              <p>(81) 99503-0004</p>
            </div>
          </div>
          
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-envelope"></i>
            </div>
            <div class="info-text">
              <h3>E-mail</h3>
              <p>lucasaraldi.dev@gmail.com</p>
            </div>
          </div>
          
          <div class="info-item">
            <div class="info-icon">
              <i class="fas fa-map-marker-alt"></i>
            </div>
            <div class="info-text">
              <h3>Endereço</h3>
              <p>Rua Sabino Gomes do Nascimento, 54 - Jose Maciel , Belo Jardim - PE</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="action-buttons">
        <router-link to="/" class="btn-secondary">Voltar para Home</router-link>
      </div>
    </section>
  </main>
</template>

<script>
import { useToast } from 'vue-toastification';
import { ref } from 'vue';

export default {
  name: 'AppContato',
  setup() {
    const toast = useToast();
    const formData = ref({
      nome: '',
      email: '',
      assunto: '',
      mensagem: ''
    });
    
    const enviarMensagem = () => {
      // Aqui seria implementado o envio da mensagem para o backend
      toast.success("Mensagem enviada com sucesso! Entraremos em contato em breve.");
      
      // Limpar formulário
      formData.value = {
        nome: '',
        email: '',
        assunto: '',
        mensagem: ''
      };
    };
    
    return {
      formData,
      enviarMensagem
    };
  }
}
</script>

<style scoped>
/* Componentes específicos desta página */
.logo-container {
  margin-bottom: var(--spacing-md);
}

.logo {
  max-width: 9.375rem; /* Convertido de 150px para rem */
  height: auto;
}

.contact-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 75rem; /* Convertido de 1200px para rem */
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-md);
}

/* Sobrescrever estilos específicos */
p {
  text-align: center;
}

.form-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
  width: 100%;
  margin-bottom: var(--spacing-lg);
}

form {
  flex: 1;
  min-width: 18.75rem; /* Convertido de 300px para rem */
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
}

.contact-info {
  flex: 1;
  min-width: 18.75rem; /* Convertido de 300px para rem */
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.input-box {
  position: relative;
  margin-bottom: 1.5625rem; /* Convertido de 25px para rem */
}

.input-box input, 
.input-box textarea {
  width: 100%;
  padding: 0.9375rem 0.9375rem 0.9375rem 2.8125rem; /* Convertido de 15px 15px 15px 45px para rem */
  background-color: #444;
  border: 1px solid #555;
  border-radius: var(--border-radius-md);
  color: #fff;
  font-size: var(--font-size-md);
  transition: all 0.3s ease;
}

.input-box textarea {
  resize: none;
}

.input-box label {
  position: absolute;
  left: 2.8125rem; /* Convertido de 45px para rem */
  top: 0.9375rem; /* Convertido de 15px para rem */
  color: #999;
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-box input:focus, 
.input-box textarea:focus,
.input-box input:not(:placeholder-shown),
.input-box textarea:not(:placeholder-shown) {
  border-color: #66ccff;
  box-shadow: 0 0 0.5rem rgba(102, 204, 255, 0.3);
  outline: none;
}

.input-box input:focus ~ label,
.input-box textarea:focus ~ label,
.input-box input:not(:placeholder-shown) ~ label,
.input-box textarea:not(:placeholder-shown) ~ label {
  top: -0.625rem; /* Convertido de -10px para rem */
  left: 0.9375rem; /* Convertido de 15px para rem */
  background-color: #2c2c2c;
  padding: 0 0.3125rem; /* Convertido de 0 5px para rem */
  font-size: var(--font-size-sm);
  color: #66ccff;
}

.input-icon {
  position: absolute;
  left: 0.9375rem; /* Convertido de 15px para rem */
  top: 1.0625rem; /* Convertido de 17px para rem */
  color: #999;
}

.textarea .input-icon {
  top: 1.0625rem; /* Convertido de 17px para rem */
}

.info-item {
  display: flex;
  align-items: center;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
}

.info-icon {
  font-size: 1.5rem; /* Convertido de 24px para rem */
  width: 3.125rem; /* Convertido de 50px para rem */
  height: 3.125rem; /* Convertido de 50px para rem */
  background: #444;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 0.9375rem; /* Convertido de 15px para rem */
  color: #fff;
}

.info-text h3 {
  font-size: var(--font-size-lg);
  margin-bottom: 0.3125rem; /* Convertido de 5px para rem */
  color: #eee;
}

.info-text p {
  font-size: var(--font-size-md);
  color: #aaa;
  margin: 0;
  text-align: left;
}

.btn-submit {
  width: 100%;
  padding: 0.875rem; /* Convertido de 14px para rem */
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #fff;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 0.3125rem 0.9375rem rgba(0, 0, 0, 0.3);
}

.btn-submit:hover {
  background: linear-gradient(145deg, #444, #333);
  transform: translateY(-0.1875rem); /* Convertido de -3px para rem */
  box-shadow: 0 0.5rem 1.25rem rgba(0, 0, 0, 0.4);
}

.action-buttons {
  margin-top: var(--spacing-md);
}

.btn-secondary {
  display: inline-block;
  padding: 0.875rem 1.875rem; /* Convertido de 14px 30px para rem */
  font-size: var(--font-size-md);
  font-weight: 600;
  text-decoration: none;
  border-radius: var(--border-radius-md);
  transition: all 0.3s ease;
  background: transparent;
  color: #fff;
  border: 2px solid #444;
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-0.1875rem); /* Convertido de -3px para rem */
  box-shadow: 0 0.375rem 0.9375rem rgba(0, 0, 0, 0.3);
}

/* Responsividade */
@media (max-width: 1024px) {
  .contact-section {
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  form, .contact-info {
    min-width: 17.5rem; /* Convertido de 280px para rem */
  }
}

@media (max-width: 768px) {
  .form-container {
    flex-direction: column;
  }
  
  .input-box input, 
  .input-box textarea {
    padding: 0.75rem 0.75rem 0.75rem 2.5rem; /* Convertido de 12px 12px 12px 40px para rem */
    font-size: var(--font-size-md);
  }
  
  .input-box label {
    left: 2.5rem; /* Convertido de 40px para rem */
    top: 0.75rem; /* Convertido de 12px para rem */
  }
  
  .input-icon {
    left: 0.75rem; /* Convertido de 12px para rem */
    top: 0.875rem; /* Convertido de 14px para rem */
  }
  
  .textarea .input-icon {
    top: 0.875rem; /* Convertido de 14px para rem */
  }
}

@media (max-width: 480px) {
  .contact-section {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  .input-box {
    margin-bottom: var(--spacing-md);
  }
  
  .info-icon {
    width: 2.5rem; /* Convertido de 40px para rem */
    height: 2.5rem; /* Convertido de 40px para rem */
    font-size: var(--font-size-lg);
  }
  
  .info-text h3 {
    font-size: var(--font-size-md);
  }
  
  .info-text p {
    font-size: var(--font-size-sm);
  }
  
  .btn-submit {
    padding: 0.75rem; /* Convertido de 12px para rem */
    font-size: var(--font-size-sm);
  }
}
</style>
