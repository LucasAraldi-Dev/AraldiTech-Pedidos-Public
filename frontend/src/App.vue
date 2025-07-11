<template>
  <div id="app">
    <!-- Envolvendo todo o conteúdo em uma única transição -->
    <router-view v-slot="{ Component }">
      <transition name="router-view-transition" mode="out-in" appear>
        <div class="page-wrapper" :key="$route.fullPath">
          <!-- Exibe o AppHeader apenas se não estiver na página do menu -->
          <AppHeader v-if="!isInMenuPage && !isLoadingSplash" />
          
          <!-- Container principal para o conteúdo -->
          <div class="main-content" :class="{ 'menu-page': isInMenuPage }">
            <component :is="Component" @splash-loading="updateSplashStatus" />
          </div>
          
          <!-- Exibe o AppFooter apenas se não estiver na página do menu -->
          <AppFooter v-if="!isInMenuPage && !isLoadingSplash" />
        </div>
      </transition>
    </router-view>
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
  data() {
    return {
      isLoadingSplash: false
    }
  },
  computed: {
    isInMenuPage() {
      // Verifica se a página atual é a do menu, usando $route
      return this.$route.name === 'Menu';
    }
  },
  methods: {
    updateSplashStatus(isLoading) {
      this.isLoadingSplash = isLoading;
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

/* Importar arquivo de responsividade para garantir acesso global às variáveis */
@import url('./assets/responsive.css');

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden; /* Prevenir scrollbars horizontais */
}

/* Wrapper para a página inteira */
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

/* Container principal para conteúdo */
.main-content {
  flex: 1;
  padding-top: var(--spacing-xxl); /* Usa variável em vez de 80px */
  padding-bottom: var(--spacing-xl); /* Usa variável em vez de 70px */
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 9.375rem); /* Convertido de 150px para rem */
  overflow-y: auto;
  transition: opacity 0.3s ease;
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
  padding: var(--spacing-xl) var(--spacing-md); /* Usa variáveis em vez de 40px 20px */
  max-width: 75rem; /* Convertido de 1200px para rem */
  margin: 0 auto;
  width: 100%;
}

/* Header e Footer consistentes */
.app-footer {
  width: 100%;
  background-color: #2c2c2c;
  color: #fff;
  z-index: var(--z-index-footer);
  position: fixed;
  bottom: 0;
  left: 0;
  border-top: 1px solid #444;
}

header {
  width: 100%;
  background-color: #2c2c2c;
  color: #fff;
  z-index: var(--z-index-header);
  position: fixed;
  top: 0;
  left: 0;
  border-bottom: 1px solid #444;
}

/* Estilos globais para botões - semelhantes ao AppLogin */
.btn-primary, .btn-secondary {
  display: inline-block;
  padding: 0.875rem 1.875rem; /* Convertido de 14px 30px para rem */
  font-size: var(--font-size-md); /* Usa variável em vez de 17px */
  font-weight: 600;
  text-decoration: none;
  border-radius: var(--border-radius-md); /* Usa variável em vez de 8px */
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
  font-size: var(--font-size-3xl); /* Usa variável em vez de 36px */
  margin-bottom: 1rem; /* Convertido de 16px para rem */
  font-weight: 700;
  background: linear-gradient(90deg, #fff, #aaa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3);
  text-align: center;
}

p {
  font-size: var(--font-size-lg); /* Usa variável em vez de 18px */
  margin-bottom: 1.875rem; /* Convertido de 30px para rem */
  color: #ccc;
}

/* Estilos comuns de contêiner */
.container {
  width: 100%;
  max-width: 75rem; /* Convertido de 1200px para rem */
  margin: 0 auto;
  padding: 0 var(--spacing-md); /* Usa variável em vez de 20px */
}

/* Cores e elementos comuns com o AppLogin */
.card, .modal, .form-container {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: var(--border-radius-lg); /* Usa variável em vez de 12px */
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
}

input, select, textarea {
  background: #444;
  border: 1px solid #555;
  color: white;
  border-radius: var(--border-radius-md); /* Usa variável em vez de 8px */
}

input:focus, select:focus, textarea:focus {
  border-color: #66ccff;
  box-shadow: 0 0 0.5rem rgba(102, 204, 255, 0.3); /* Convertido de 8px para rem */
}

/* Responsividade consistente */
@media (max-width: 1024px) {
  .welcome-section, .contact-section, .help-section {
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  .main-content {
    padding-top: 4.375rem; /* Convertido de 70px para rem */
    padding-bottom: 3.75rem; /* Convertido de 60px para rem */
  }
}

@media (max-width: 768px) {
  .welcome-section, .contact-section, .help-section {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  h1 {
    font-size: var(--font-size-xl);
  }
  
  p {
    font-size: var(--font-size-md);
  }
  
  .btn-primary, .btn-secondary {
    padding: 0.75rem 1.5rem; /* Convertido de 12px 24px para rem */
    font-size: var(--font-size-md);
  }
  
  .container {
    padding: 0 var(--spacing-sm);
  }
  
  .main-content {
    padding-top: 3.75rem; /* Convertido de 60px para rem */
    padding-bottom: 3.125rem; /* Convertido de 50px para rem */
  }
}

@media (max-width: 480px) {
  .welcome-section, .contact-section, .help-section {
    padding: var(--spacing-sm) var(--spacing-xs);
  }
  
  h1 {
    font-size: var(--font-size-lg);
  }
  
  p {
    font-size: var(--font-size-sm);
  }
  
  .btn-primary, .btn-secondary {
    padding: 0.625rem 1.25rem; /* Convertido de 10px 20px para rem */
    font-size: var(--font-size-sm);
  }
  
  .container {
    padding: 0 var(--spacing-xs);
  }
}

/* Regras globais para modais */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85); 
  z-index: var(--z-index-modal);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: var(--spacing-md);
  box-sizing: border-box;
}

.order-form,
.print-modal,
.dashboard-container,
.modal-content,
.modal-responsive {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: var(--spacing-lg); 
  border-radius: var(--border-radius-lg);
  width: var(--modal-width-md);
  max-width: var(--modal-max-width); 
  max-height: var(--modal-max-height);
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

/* Ajustes globais de responsividade para todos os modais */
@media (max-width: 1024px) {
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    width: var(--modal-width-md);
    max-width: var(--modal-max-width);
    padding: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: var(--spacing-xs);
  }
  
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding: var(--spacing-sm);
  }
}

/* Ajustes para telas com zoom (notebooks, etc) */
@media screen and (min-resolution: 1.25dppx) {
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    max-height: var(--modal-max-height);
  }
}

/* Ajustes para telas 720p */
@media (min-height: 720px) and (max-height: 768px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: 2vh;
  }
  
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    max-height: 85vh;
  }
}

/* Ajustes para monitores pequenos de 14 polegadas */
@media screen and (max-width: 1366px) and (max-height: 768px) {
  .order-form,
  .print-modal,
  .dashboard-container,
  .modal-content,
  .modal-responsive {
    padding: var(--spacing-md);
  }
}

/* Estilos para o corpo durante o carregamento */
body.loading {
  overflow: hidden;
}

/* Efeito de transição suave para toda a aplicação */
.router-view-transition-enter-active,
.router-view-transition-leave-active {
  transition: opacity 0.3s ease;
}

.router-view-transition-enter-from,
.router-view-transition-leave-to {
  opacity: 0;
}
</style>
