<template>
  <header>
    <div class="container">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo.png" alt="Logo AraldiTech" class="logo" onerror="this.src='favicon.ico'" />
      </router-link>
      
      <!-- Botão hamburger com design moderno e animação especial -->
      <div class="hamburger-menu" @click="toggleMenu" :class="{ 'is-active': menuActive }">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      
      <nav :class="{ 'is-active': menuActive }">
        <ul>
          <li><router-link :to="{ path: '/', query: { fromMenu: 'true' } }">Início</router-link></li>
          <li><router-link to="/contato">Contato</router-link></li>
          <li><router-link to="/ajuda">Ajuda</router-link></li>
        </ul>
      </nav>
    </div>
    <!-- Backdrop/overlay quando menu está ativo -->
    <div class="nav-backdrop" :class="{ 'is-active': menuActive }" @click="toggleMenu"></div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      menuActive: false
    }
  },
  methods: {
    toggleMenu() {
      this.menuActive = !this.menuActive;
      
      // Impedir scroll quando o menu está aberto
      if (this.menuActive) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
  },
  // Garantir que o scroll seja restaurado quando o componente for destruído
  beforeUnmount() {
    document.body.style.overflow = '';
  }
}
</script>

<style scoped>
header {
  background-color: #2c2c2c;
  padding: var(--spacing-sm) 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  border-bottom: 1px solid #444;
  z-index: var(--z-index-header);
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 75rem; /* Convertido de 1200px para rem */
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.logo {
  width: 8.75rem; /* Convertido de 140px para rem */
  height: auto;
}

.logo-link {
  display: block;
}

/* Novo design do hamburger menu com animação especial */
.hamburger-menu {
  display: none;
  width: 30px;
  height: 25px;
  position: relative;
  cursor: pointer;
  z-index: 150;
  transform: rotate(0deg);
  transition: 0.5s ease-in-out;
}

.hamburger-menu span {
  display: block;
  position: absolute;
  height: 3px;
  width: 100%;
  background: #66ccff;
  border-radius: 3px;
  opacity: 1;
  left: 0;
  transform: rotate(0deg);
  transition: .25s ease-in-out;
  box-shadow: 0 0 8px rgba(102, 204, 255, 0.5);
}

.hamburger-menu span:nth-child(1) {
  top: 0px;
  transform-origin: left center;
}

.hamburger-menu span:nth-child(2),
.hamburger-menu span:nth-child(3) {
  top: 10px;
  transform-origin: left center;
}

.hamburger-menu span:nth-child(4) {
  top: 20px;
  transform-origin: left center;
}

.hamburger-menu.is-active span:nth-child(1) {
  transform: rotate(45deg);
  top: -3px;
  left: 4px;
}

.hamburger-menu.is-active span:nth-child(2) {
  width: 0%;
  opacity: 0;
}

.hamburger-menu.is-active span:nth-child(3) {
  transform: rotate(-45deg);
  top: 22px;
  left: 4px;
}

.hamburger-menu.is-active span:nth-child(4) {
  width: 0%;
  opacity: 0;
}

/* Efeito de glow no hover */
.hamburger-menu:hover span {
  background: #8adfff;
  box-shadow: 0 0 12px rgba(102, 204, 255, 0.8);
}

nav ul {
  list-style: none;
  display: flex;
  gap: var(--spacing-md);
}

nav ul li {
  margin: 0;
}

nav ul li a {
  color: #ccc;
  text-decoration: none;
  font-weight: bold;
  padding: 0.625rem 0.9375rem; /* Convertido de 10px 15px para rem */
  transition: color 0.3s ease, background-color 0.3s ease;
  border-radius: var(--border-radius-sm);
}

nav ul li a:hover {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

nav ul li a.router-link-active {
  color: #66ccff;
}

/* Responsividade */
@media (max-width: 1024px) {
  .logo {
    width: 8.125rem; /* Convertido de 130px para rem */
  }
  
  nav ul {
    gap: var(--spacing-sm);
  }
  
  nav ul li a {
    padding: 0.5rem 0.75rem; /* Convertido de 8px 12px para rem */
    font-size: var(--font-size-sm);
  }
}

@media (max-width: 768px) {
  .hamburger-menu {
    display: block;
  }
  
  /* Backdrop/overlay visível apenas em mobile */
  .nav-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 80;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.4s ease, visibility 0.4s ease;
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
  }
  
  .nav-backdrop.is-active {
    opacity: 1;
    visibility: visible;
  }
  
  nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background: linear-gradient(135deg, #2c2c2c, #222);
    /* Movendo o menu mais para cima conforme solicitado */
    padding-top: 2rem; 
    transition: all 0.5s cubic-bezier(0.65, 0, 0.35, 1);
    z-index: 90;
    box-shadow: -5px 0 25px rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: flex-start;
    justify-content: center;
  }
  
  nav.is-active {
    right: 0;
  }
  
  nav ul {
    flex-direction: column;
    align-items: center;
    gap: 1.25rem; /* 20px */
    width: 100%;
    padding: 0;
    margin-top: 2rem;
  }
  
  nav ul li {
    width: 100%;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.5s ease, transform 0.5s ease;
  }
  
  nav.is-active ul li {
    opacity: 1;
    transform: translateY(0);
  }
  
  /* Atrasar a animação para cada item do menu - timing aprimorado */
  nav.is-active ul li:nth-child(1) {
    transition-delay: 0.2s;
  }
  
  nav.is-active ul li:nth-child(2) {
    transition-delay: 0.3s;
  }
  
  nav.is-active ul li:nth-child(3) {
    transition-delay: 0.4s;
  }
  
  nav ul li a {
    display: block;
    padding: 0.875rem 1.25rem; /* 14px 20px */
    font-size: var(--font-size-lg);
    width: 80%;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    background: linear-gradient(145deg, #333, #292929);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
  }
  
  nav ul li a:hover {
    transform: translateY(-3px);
    background: linear-gradient(145deg, #383838, #303030);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
  }
  
  /* Novo efeito de borda brilhante */
  nav ul li a::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: #66ccff;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  nav ul li a:hover::before,
  nav ul li a.router-link-active::before {
    transform: translateX(0);
    box-shadow: 0 0 15px rgba(102, 204, 255, 0.6);
  }
  
  nav ul li a.router-link-active {
    background: linear-gradient(145deg, #333, #292929);
    color: #66ccff;
    font-weight: bold;
  }
}

@media (max-width: 480px) {
  .logo {
    width: 6.875rem; /* Convertido de 110px para rem */
  }
  
  .container {
    padding: 0 var(--spacing-sm);
  }
  
  nav {
    width: 80%;
  }
  
  header {
    padding: 0.625rem 0; /* Convertido de 10px para rem */
  }
  
  nav ul li a {
    font-size: var(--font-size-md);
    padding: 0.75rem 1rem; /* Convertido para rem */
    width: 85%;
  }
}

@media (max-width: 390px) {
  .logo {
    width: 6.25rem; /* Convertido de 100px para rem */
  }
  
  .container {
    padding: 0 var(--spacing-xs);
  }
  
  nav ul li a {
    font-size: var(--font-size-md);
    padding: 0.625rem 0.875rem; /* Convertido para rem */
    width: 90%;
  }
}

/* Estilo para o backdrop/overlay */
@media (max-width: 768px) {
  .nav-backdrop {
    display: block;
  }
}
</style>
