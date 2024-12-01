<template>
  <footer>
    <div class="container">
      <p>&copy; 2024 AraldiTech. Todos os direitos reservados.</p>
      <ul class="footer-links">
        <li><a href="#">Política de Privacidade</a></li>
        <li><a href="#">Termos de Uso</a></li>
      </ul>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
/* Estilos Gerais */
footer {
  background-color: #333;
  color: #fff;
  padding: 20px 0;
  width: 100%;
}

footer .container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center; 
  gap: 10px; 
}

footer p {
  margin: 0;
  font-size: 14px; 
}

.footer-links {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin: 0;
  padding: 0;
}

.footer-links li a {
  color: #fff;
  text-decoration: none;
  font-size: 14px;
}

.footer-links li a:hover {
  color: #ccc;
}

/* Garantir que o footer esteja fixo no final */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
}

main {
  flex: 1; 
}
</style>
