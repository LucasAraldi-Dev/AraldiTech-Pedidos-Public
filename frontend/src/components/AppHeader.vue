<template>
  <header>
    <div class="container">
      <router-link to="/" class="logo-link">
        <img src="../assets/logo.png" alt="Logo AraldiTech" class="logo" onerror="this.src='favicon.ico'" />
      </router-link>
      
      <!-- Botão hamburger para menu mobile -->
      <div class="menu-toggle" @click="toggleMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>
      
      <nav :class="{ 'is-active': menuActive }">
        <ul>
          <li><router-link to="/">Início</router-link></li>
          <li><router-link to="/contato">Contato</router-link></li>
          <li><router-link to="/ajuda">Ajuda</router-link></li>
        </ul>
      </nav>
    </div>
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
    }
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

.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 1.875rem; /* Convertido de 30px para rem */
  height: 1.3125rem; /* Convertido de 21px para rem */
  cursor: pointer;
  z-index: 150;
}

.menu-toggle span {
  display: block;
  width: 100%;
  height: 0.1875rem; /* Convertido de 3px para rem */
  background-color: #fff;
  border-radius: 0.1875rem; /* Convertido de 3px para rem */
  transition: all 0.3s ease;
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
  .menu-toggle {
    display: flex;
  }
  
  nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background-color: #2c2c2c;
    padding-top: 5rem; /* Convertido de 80px para rem */
    transition: right 0.3s ease;
    z-index: 90;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3);
  }
  
  nav.is-active {
    right: 0;
  }
  
  nav ul {
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-xs);
  }
  
  nav ul li {
    width: 100%;
    text-align: center;
  }
  
  nav ul li a {
    display: block;
    padding: 0.75rem; /* Convertido de 12px para rem */
    font-size: var(--font-size-md);
    width: 90%;
    margin: 0 auto;
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

  .menu-toggle {
    width: 1.625rem; /* Convertido de 26px para rem */
    height: 1.1875rem; /* Convertido de 19px para rem */
  }
  
  nav ul li a {
    font-size: var(--font-size-sm);
    padding: 0.625rem; /* Convertido de 10px para rem */
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
    font-size: 0.875rem; /* Convertido de 14px para rem */
    padding: 0.5rem; /* Convertido de 8px para rem */
  }
}
</style>
