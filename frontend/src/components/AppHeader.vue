<template>
  <header>
    <div class="container">
      <router-link to="/" class="logo-link">
        <img src="./favicon_logo_branco.png" alt="Logo AraldiTech" class="logo" />
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
          <li><router-link to="/contato">Contato </router-link></li>
          <li><router-link to="/ajuda">Ajuda </router-link></li>
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
  background-color: #333;
  padding: 20px 0;
  position: relative;
}

header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  width: 150px;
  height: auto;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  cursor: pointer;
  z-index: 10;
}

.menu-toggle span {
  display: block;
  width: 100%;
  height: 3px;
  background-color: #fff;
  border-radius: 3px;
  transition: all 0.3s ease;
}

nav ul {
  list-style: none;
  display: flex;
  gap: 20px;
}

nav ul li {
  margin: 0;
}

nav ul li a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  padding: 10px 15px;
  transition: color 0.3s ease;
}

nav ul li a:hover {
  color: #ccc;
}

/* Responsividade */
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
    background-color: #222;
    padding-top: 80px;
    transition: right 0.3s ease;
    z-index: 9;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.3);
  }
  
  nav.is-active {
    right: 0;
  }
  
  nav ul {
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }
  
  nav ul li {
    width: 100%;
    text-align: center;
  }
  
  nav ul li a {
    display: block;
    padding: 15px;
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .logo {
    width: 120px;
  }
  
  header .container {
    padding: 0 15px;
  }
  
  nav {
    width: 80%;
  }
}

@media (max-width: 390px) {
  .logo {
    width: 100px;
  }
  
  header .container {
    padding: 0 10px;
  }
  
  nav ul li a {
    font-size: 16px;
    padding: 12px;
  }
}

@media (min-width: 769px) and (max-width: 1023px) {
  header .container {
    max-width: 900px;
  }
  
  nav ul {
    gap: 15px;
  }
  
  nav ul li a {
    padding: 8px 12px;
  }
}

@media (min-width: 1024px) and (max-width: 1366px) {
  header .container {
    max-width: 1150px;
  }
}
</style>
