<template>
  <main class="home-page">
    <!-- Splash Screen - Não exibir quando usuário navega pelo menu hamburguer -->
    <div class="splash-screen" v-if="shouldShowSplash" :class="{'fade-out': splashFadeOut}">
      <div class="splash-logo">
        <!-- Logo da empresa - aumentado para desktop -->
        <img src="../assets/logo.png" alt="AraldiTech" onerror="this.src='favicon.ico'">
      </div>
      <div class="splash-text">AraldiTech Pedidos</div>
      <div class="splash-loader"></div>
    </div>

    <!-- O conteúdo principal agora é sempre renderizado, mas inicialmente invisível -->
    <section class="welcome-section" :class="{'animate-in': !isLoading, 'hidden': isLoading && shouldShowSplash}">
      <div class="logo-container animate-item">
        <img src="../assets/logo.png" alt="AraldiTech" class="logo" onerror="this.src='favicon.ico'">
      </div>
      <h1 class="animate-item">AraldiTech Pedidos</h1>
      <p class="animate-item">Gerencie seus pedidos de forma rápida e eficiente</p>
      
      <div class="action-buttons animate-item">
        <router-link to="/login" class="btn-primary pulse">Entrar</router-link>
        <router-link to="/contato" class="btn-secondary">Contato</router-link>
      </div>
      
      <div class="features">
        <div class="feature-card animate-item" style="--delay: 0.1s">
          <div class="feature-icon">
            <i class="fas fa-clipboard-list"></i>
          </div>
          <h3>Gerenciamento</h3>
          <p>Controle todos os seus pedidos em um só lugar</p>
        </div>
        
        <div class="feature-card animate-item" style="--delay: 0.2s">
          <div class="feature-icon">
            <i class="fas fa-chart-bar"></i>
          </div>
          <h3>Relatórios</h3>
          <p>Analise seus dados com relatórios detalhados</p>
        </div>
        
        <div class="feature-card animate-item" style="--delay: 0.3s">
          <div class="feature-icon">
            <i class="fas fa-users"></i>
          </div>
          <h3>Colaboração</h3>
          <p>Trabalhe em equipe com diferentes níveis de acesso</p>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'AppHome',
  setup(props, { emit }) {
    // Estados para splash screen
    const isLoading = ref(true);
    const splashFadeOut = ref(false);
    const fromMenu = ref(false);
    
    // Usar o objeto route para verificar a rota anterior
    const route = useRoute();

    // Verificar se o menu hamburguer está aberto ou se a navegação veio do menu
    const shouldShowSplash = computed(() => {
      // Verifica se veio do menu hamburguer
      if (fromMenu.value) return false;
      
      // Verifica se existe o localStorage com a flag visitedHome
      const hasVisitedHome = localStorage.getItem('visitedHome');
      
      // Se já visitou a home antes e está navegando entre páginas, não mostrar splash
      if (hasVisitedHome && (route.query.fromMenu === 'true' || document.querySelector('.hamburger-menu.is-active'))) {
        return false;
      }
      
      return isLoading.value;
    });
    
    onMounted(() => {
      // Verificar se a navegação veio do menu
      if (route.query.fromMenu === 'true' || document.querySelector('.hamburger-menu.is-active')) {
        fromMenu.value = true;
        isLoading.value = false;
        emit('splash-loading', false);
        return;
      }
      
      // Marcar que já visitou a home
      localStorage.setItem('visitedHome', 'true');
      
      // Pré-renderizar conteúdo principal enquanto mostra splash screen
      document.body.classList.add('loading');
      
      // Emitir evento para o componente pai
      emit('splash-loading', true);
      
      // Simular tempo de carregamento para splash screen
      setTimeout(() => {
        splashFadeOut.value = true;
        
        // Remover splash screen após a transição
        setTimeout(() => {
          isLoading.value = false;
          document.body.classList.remove('loading');
          emit('splash-loading', false);
        }, 500);
      }, 1500);
    });
    
    return {
      isLoading,
      splashFadeOut,
      shouldShowSplash
    };
  }
}
</script>

<style scoped>
/* Splash screen */
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #1a1a1a; /* Fundo mais escuro para aparência mais séria */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  z-index: 9999;
  transition: opacity 0.5s ease;
}

.splash-screen.fade-out {
  opacity: 0;
  pointer-events: none;
}

.splash-logo {
  width: 140px;
  height: auto;
  margin-bottom: 2rem;
  filter: drop-shadow(0px 4px 10px rgba(0, 0, 0, 0.5));
  transform-origin: center;
  animation: logoReveal 1.2s ease-out;
}

/* Logo maior para desktop */
@media (min-width: 769px) {
  .splash-logo {
    width: 240px;
  }
}

.splash-logo img {
  width: 100%;
  height: auto;
}

.splash-text {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  animation: fadeIn 1s ease-in;
}

.splash-loader {
  width: 100px;
  height: 3px;
  background: #333;
  border-radius: 2px;
  margin-top: 1.5rem;
  overflow: hidden;
  position: relative;
}

.splash-loader:after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 30%;
  background: #fff; /* Loader branco para aparência mais séria */
  border-radius: 2px;
  animation: loading 1.5s infinite ease-in-out;
}

/* Esconder conteúdo principal enquanto splash está ativo */
.hidden {
  opacity: 0;
  visibility: hidden;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
  100% { transform: translateX(300%); }
}

@keyframes logoReveal {
  0% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Animações para entrada de elementos */
.animate-in .animate-item {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s forwards;
  animation-delay: calc(0.1s + var(--delay, 0s));
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animação de "pulse" para botão primário */
.btn-primary.pulse {
  position: relative;
  animation: buttonPulse 2s infinite;
}

@keyframes buttonPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 204, 255, 0.6);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(102, 204, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 204, 255, 0);
  }
}

/* Componentes específicos desta página */
.logo-container {
  margin-bottom: var(--spacing-md);
}

.logo {
  max-width: 11.25rem; /* Convertido de 180px para rem */
  height: auto;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.welcome-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--spacing-xl) var(--spacing-md);
  min-height: calc(100vh - 120px); /* Ajuste para cabeçalho/rodapé fixos */
  transition: opacity 0.5s ease, visibility 0.5s ease;
}

/* Os estilos de h1 e p estão definidos globalmente, apenas sobrescrevendo o específico */
h1 {
  font-size: var(--font-size-4xl); /* Equivalente a 42px */
  margin-bottom: 1rem;
  color: #fff; /* Cor sólida em vez de gradiente */
  font-weight: 600;
}

p {
  font-size: var(--font-size-lg);
  max-width: 37.5rem; /* Convertido de 600px para rem */
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xxl);
}

/* Botões já estão no estilo global, removidos daqui */

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5625rem; /* Convertido de 25px para rem */
  width: 100%;
  max-width: 62.5rem; /* Convertido de 1000px para rem */
}

.feature-card {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: var(--spacing-xl) var(--spacing-md);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
  flex: 1;
  min-width: 15.625rem; /* Convertido de 250px para rem */
  max-width: 18.75rem; /* Convertido de 300px para rem */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-0.3125rem); /* Convertido de -5px para rem */
  box-shadow: 0 0.75rem 1.25rem rgba(0, 0, 0, 0.4);
}

.feature-card:after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.03) 40%,
    rgba(255, 255, 255, 0.04) 50%,
    rgba(255, 255, 255, 0.03) 60%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  transition: transform 0.7s;
  z-index: 1;
}

.feature-card:hover:after {
  transform: rotate(30deg) translate(10%, 10%);
}

.feature-icon {
  font-size: 2.375rem; /* Convertido de 38px para rem */
  margin-bottom: var(--spacing-md);
  color: #fff;
  position: relative;
  z-index: 2;
}

.feature-card h3 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-sm);
  color: #fff;
  position: relative;
  z-index: 2;
}

.feature-card p {
  font-size: var(--font-size-md);
  color: #aaa;
  margin-bottom: 0;
  position: relative;
  z-index: 2;
}

/* Responsividade */
@media (max-width: 1024px) {
  h1 {
    font-size: var(--font-size-3xl);
  }
  
  .features {
    gap: var(--spacing-md);
  }
  
  .feature-card {
    min-width: 13.75rem; /* Convertido de 220px para rem */
  }
}

@media (max-width: 768px) {
  .welcome-section {
    min-height: calc(100vh - 100px);
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
  
  h1 {
    font-size: var(--font-size-xxl);
  }
  
  p {
    font-size: var(--font-size-md);
  }
  
  .action-buttons {
    flex-direction: column;
    gap: var(--spacing-sm);
    width: 100%;
    max-width: 18.75rem; /* Convertido de 300px para rem */
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    text-align: center;
  }
  
  .features {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-card {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .welcome-section {
    min-height: calc(100vh - 80px);
    padding: 1rem 0.5rem;
    justify-content: flex-start;
    padding-top: 2rem;
  }
  
  h1 {
    font-size: var(--font-size-xl);
    margin-bottom: 0.5rem;
  }
  
  p {
    font-size: var(--font-size-sm);
    margin-bottom: 1rem;
  }
  
  .feature-card {
    padding: var(--spacing-md) var(--spacing-sm);
    margin-bottom: 1rem;
  }
  
  .feature-icon {
    font-size: 2rem; /* Convertido de 32px para rem */
  }
  
  .feature-card h3 {
    font-size: var(--font-size-lg);
  }
  
  .feature-card p {
    font-size: var(--font-size-sm);
  }
  
  .action-buttons {
    margin-bottom: 1.5rem;
  }
  
  .logo {
    max-width: 9rem;
  }
}

/* Ajuste para telas pequenas em altura */
@media (max-height: 700px) {
  .welcome-section {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
  
  .feature-card {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
  
  .logo-container {
    margin-bottom: 0.5rem;
  }
  
  h1 {
    margin-bottom: 0.5rem;
  }
  
  p {
    margin-bottom: 0.5rem;
  }
  
  .action-buttons {
    margin-bottom: 1rem;
  }
}

/* Estilos para o corpo durante o carregamento */
:global(body.loading) {
  overflow: hidden;
}
</style>
