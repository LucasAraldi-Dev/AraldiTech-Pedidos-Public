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
}
</script>

<style scoped>
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
