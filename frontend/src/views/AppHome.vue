<template>
  <main>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <section class="intro">
      <h1>AraldiTech  Pedidos</h1>
      <p>Faça login para acessar seu painel de controle.</p>
      <router-link to="/login" class="btn-login" id="loginbtn">Entrar</router-link>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AppHome'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  overflow: hidden; 
}

body {
  font-family: 'Roboto', sans-serif; 
  background-color: #fafafa;
  color: #333333;
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

header {
  background-color: #333;
  padding: 20px 0;
}

header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  width: 150px;
  height: auto;
}

nav ul {
  list-style: none;
  display: flex;
}

nav ul li {
  margin-left: 20px;
}

nav ul li a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
}

nav ul li a:hover {
  color: #ccc;
}

main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh; 
  background-color: #222;
  color: #fff;
}

.intro {
  text-align: center;
}

.intro h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.intro p {
  font-size: 18px;
  margin-bottom: 30px;
}

.btn-login {
  display: inline-block;
  padding: 16px 32px;
  font-size: 20px;
  font-weight: bold;
  color: #ffffff;
  background: linear-gradient(145deg, #333, #555);
  border: none;
  border-radius: 12px;
  text-decoration: none;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.4), inset 0px 4px 8px rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.btn-login:hover {
  background: linear-gradient(145deg, #555, #777);
  box-shadow: 0px 10px 18px rgba(0, 0, 0, 0.5), inset 0px 4px 8px rgba(255, 255, 255, 0.15);
  transform: translateY(-4px);
}

.btn-login:active {
  background: linear-gradient(145deg, #222, #444);
  box-shadow: inset 0px 6px 10px rgba(0, 0, 0, 0.6);
}


footer {
  background-color: #333;
  padding: 20px 0;
  color: #fff;
}

footer .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

footer p {
  margin: 0;
}

.footer-links {
  list-style: none;
  display: flex;
}

.footer-links li {
  margin-left: 20px;
}

.footer-links li a {
  color: #fff;
  text-decoration: none;
}

.footer-links li a:hover {
  color: #ccc;
}



</style>
