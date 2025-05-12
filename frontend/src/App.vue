<template>
  <div id="app">
    <!-- Exibe o AppHeader apenas se não estiver na página do menu -->
    <AppHeader v-if="!isInMenuPage" />
    
    <!-- Container principal para o conteúdo -->
    <div class="main-content" :class="{ 'menu-page': isInMenuPage }">
      <!-- Aqui vai o conteúdo dinâmico baseado nas rotas -->
      <router-view />
    </div>
    
    <!-- Exibe o AppFooter apenas se não estiver na página do menu -->
    <AppFooter v-if="!isInMenuPage" />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
  },
  computed: {
    isInMenuPage() {
      // Verifica se a página atual é a do menu, usando $route
      return this.$route.name === 'Menu';
    }
  },
  created() {
    // Redireciona automaticamente para o menu se o usuário já estiver logado
    const token = localStorage.getItem('access_token');
    if (token && this.$route.name === 'Login') {
      this.$router.push({ name: 'Menu' });
    }
  }
}
</script>

<style>
/* Estilos básicos */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  font-family: 'Roboto', sans-serif;
  background-color: #2c2c2c;
  color: #fff;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden; /* Prevenir scrollbars horizontais */
}

/* Container principal para conteúdo */
.main-content {
  flex: 1;
  padding-top: 80px;  /* Altura do header fixo */
  padding-bottom: 70px; /* Altura do footer fixo */
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 150px); /* Altura da viewport menos header e footer */
  overflow-y: auto;
}

.main-content.menu-page {
  padding-top: 0;
  padding-bottom: 0;
  min-height: 100vh;
}

/* Estilos globais para componentes de página */
.home-page, .contact-page, .help-page {
  display: flex;
  flex-direction: column;
  flex: 1;
  background-color: #2c2c2c;
}

/* Container padrão para seções */
.welcome-section, .contact-section, .help-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* Header e Footer consistentes */
.app-footer {
  width: 100%;
  background-color: #2c2c2c;
  color: #fff;
  z-index: 100;
  position: fixed;
  bottom: 0;
  left: 0;
  border-top: 1px solid #444;
}

header {
  width: 100%;
  background-color: #2c2c2c;
  color: #fff;
  z-index: 100;
  position: fixed;
  top: 0;
  left: 0;
  border-bottom: 1px solid #444;
}

/* Estilos globais para botões - semelhantes ao AppLogin */
.btn-primary, .btn-secondary {
  display: inline-block;
  padding: 14px 30px;
  font-size: 17px;
  font-weight: 600;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-align: center;
}

.btn-primary {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #ffffff;
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3), inset 0px 1px 3px rgba(255, 255, 255, 0.1);
}

.btn-primary:hover {
  background: linear-gradient(145deg, #444, #333);
  transform: translateY(-3px);
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.4), inset 0px 1px 3px rgba(255, 255, 255, 0.2);
}

.btn-secondary {
  background: transparent;
  color: #fff;
  border: 2px solid #444;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-3px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
}

/* Estilos para cabeçalhos e textos comuns */
h1 {
  font-size: 36px;
  margin-bottom: 16px;
  font-weight: 700;
  background: linear-gradient(90deg, #fff, #aaa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
}

p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #ccc;
}

/* Estilos comuns de contêiner */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Cores e elementos comuns com o AppLogin */
.card, .modal, .form-container {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: 12px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
}

input, select, textarea {
  background: #444;
  border: 1px solid #555;
  color: white;
  border-radius: 8px;
}

input:focus, select:focus, textarea:focus {
  border-color: #66ccff;
  box-shadow: 0 0 8px rgba(102, 204, 255, 0.3);
}

/* Responsividade consistente */
@media (max-width: 1024px) {
  .welcome-section, .contact-section, .help-section {
    padding: 30px 20px;
  }
  
  .main-content {
    padding-top: 70px; /* Header menor para tablets */
    padding-bottom: 60px;
  }
}

@media (max-width: 768px) {
  .welcome-section, .contact-section, .help-section {
    padding: 25px 15px;
  }
  
  h1 {
    font-size: 30px;
  }
  
  p {
    font-size: 16px;
  }
  
  .btn-primary, .btn-secondary {
    padding: 12px 24px;
    font-size: 16px;
  }
  
  .container {
    padding: 0 15px;
  }
  
  .main-content {
    padding-top: 60px; /* Header menor para mobile */
    padding-bottom: 50px;
  }
}

@media (max-width: 480px) {
  .welcome-section, .contact-section, .help-section {
    padding: 20px 10px;
  }
  
  h1 {
    font-size: 26px;
  }
  
  p {
    font-size: 14px;
  }
  
  .btn-primary, .btn-secondary {
    padding: 10px 20px;
    font-size: 14px;
  }
  
  .container {
    padding: 0 10px;
  }
}
</style>
