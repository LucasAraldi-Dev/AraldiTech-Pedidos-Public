<template>
  <div id="app">
    <!-- Exibe o AppHeader apenas se não estiver na página do menu -->
    <AppHeader v-if="!isInMenuPage" />
    
    <!-- Aqui vai o conteúdo dinâmico baseado nas rotas -->
    <div class="content">
      <router-view /> <!-- As páginas dinâmicas, como Home, Login, etc., serão criadas aqui -->
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
  background-color: #2c2c2c; 
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.content {
  flex: 1;
  overflow: hidden;
}

@media (max-width: 768px) {
  body {
    overflow-x: hidden;
  }
}
</style>
