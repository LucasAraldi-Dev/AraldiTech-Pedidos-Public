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
  padding: 15px 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  border-bottom: 1px solid #444;
  z-index: 100;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  width: 140px;
  height: auto;
}

.logo-link {
  display: block;
}

.menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  cursor: pointer;
  z-index: 150;
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
  color: #ccc;
  text-decoration: none;
  font-weight: bold;
  padding: 10px 15px;
  transition: color 0.3s ease, background-color 0.3s ease;
  border-radius: 6px;
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
    width: 130px;
  }
  
  nav ul {
    gap: 15px;
  }
  
  nav ul li a {
    padding: 8px 12px;
    font-size: 15px;
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
    padding-top: 80px;
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
    gap: 10px;
  }
  
  nav ul li {
    width: 100%;
    text-align: center;
  }
  
  nav ul li a {
    display: block;
    padding: 12px;
    font-size: 16px;
    width: 90%;
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .logo {
    width: 110px;
  }
  
  .container {
    padding: 0 15px;
  }
  
  nav {
    width: 80%;
  }
  
  header {
    padding: 10px 0;
  }

  .menu-toggle {
    width: 26px;
    height: 19px;
  }
  
  nav ul li a {
    font-size: 15px;
    padding: 10px;
  }
}

@media (max-width: 390px) {
  .logo {
    width: 100px;
  }
  
  .container {
    padding: 0 10px;
  }
  
  nav ul li a {
    font-size: 14px;
    padding: 8px;
  }
}
</style>
