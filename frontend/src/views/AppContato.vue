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
  margin-bottom: 20px;
}

.logo {
  max-width: 150px;
  height: auto;
}

.contact-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Sobrescrever estilos específicos */
p {
  text-align: center;
}

.form-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  width: 100%;
  margin-bottom: 30px;
}

form {
  flex: 1;
  min-width: 300px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.contact-info {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-box {
  position: relative;
  margin-bottom: 25px;
}

.input-box input, 
.input-box textarea {
  width: 100%;
  padding: 15px 15px 15px 45px;
  background-color: #444;
  border: 1px solid #555;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s ease;
}

.input-box textarea {
  resize: none;
}

.input-box label {
  position: absolute;
  left: 45px;
  top: 15px;
  color: #999;
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-box input:focus, 
.input-box textarea:focus,
.input-box input:not(:placeholder-shown),
.input-box textarea:not(:placeholder-shown) {
  border-color: #66ccff;
  box-shadow: 0 0 8px rgba(102, 204, 255, 0.3);
  outline: none;
}

.input-box input:focus ~ label,
.input-box textarea:focus ~ label,
.input-box input:not(:placeholder-shown) ~ label,
.input-box textarea:not(:placeholder-shown) ~ label {
  top: -10px;
  left: 15px;
  background-color: #2c2c2c;
  padding: 0 5px;
  font-size: 14px;
  color: #66ccff;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 17px;
  color: #999;
}

.textarea .input-icon {
  top: 17px;
}

.info-item {
  display: flex;
  align-items: center;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.info-icon {
  font-size: 24px;
  width: 50px;
  height: 50px;
  background: #444;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 15px;
  color: #fff;
}

.info-text h3 {
  font-size: 18px;
  margin-bottom: 5px;
  color: #eee;
}

.info-text p {
  font-size: 16px;
  color: #aaa;
  margin: 0;
  text-align: left;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.btn-submit:hover {
  background: linear-gradient(145deg, #444, #333);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.action-buttons {
  margin-top: 20px;
}

.btn-secondary {
  display: inline-block;
  padding: 14px 30px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: transparent;
  color: #fff;
  border: 2px solid #444;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

/* Responsividade */
@media (max-width: 1024px) {
  .contact-section {
    padding: 30px 20px;
  }
  
  form, .contact-info {
    min-width: 280px;
  }
}

@media (max-width: 768px) {
  .form-container {
    flex-direction: column;
  }
  
  .input-box input, 
  .input-box textarea {
    padding: 12px 12px 12px 40px;
    font-size: 15px;
  }
  
  .input-box label {
    left: 40px;
    top: 12px;
  }
  
  .input-icon {
    left: 12px;
    top: 14px;
  }
  
  .textarea .input-icon {
    top: 14px;
  }
}

@media (max-width: 480px) {
  .contact-section {
    padding: 20px 15px;
  }
  
  .input-box {
    margin-bottom: 20px;
  }
  
  .info-icon {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
  
  .info-text h3 {
    font-size: 16px;
  }
  
  .info-text p {
    font-size: 14px;
  }
  
  .btn-submit {
    padding: 12px;
    font-size: 14px;
  }
}
</style>
