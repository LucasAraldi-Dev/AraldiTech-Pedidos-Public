<template>
  <header>
    <div class="container">
      <router-link to="/" class="logo-link">
        <img src="./favicon_logo_branco.png" alt="Logo AraldiTech" class="logo" />
      </router-link>
      
      <nav>
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
  name: 'AppHeader'
}
</script>

<style scoped>


header {
  background-color: #333;
  padding: 20px 0;
}

header .container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.logo {
  width: 150px;
  height: auto;
  margin-right: 20px; 
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
}

nav ul li a:hover {
  color: #ccc;
}
</style>
