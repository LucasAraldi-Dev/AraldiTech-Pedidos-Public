<template>
  <main>
    <section class="help">
      <h1>Ajuda</h1>
      <p>Encontre as informações que você precisa aqui.</p>
      <ul class="faq-list">
        <li class="faq-item"><a href="#">SERÁ IMPLEMENTADO DEPOIS</a></li>
        <li class="faq-item"><a href="#">SERÁ IMPLEMENTADO DEPOIS</a></li>
        <li class="faq-item"><a href="#">SERÁ IMPLEMENTADO DEPOIS</a></li>
      </ul>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AppAjuda'
}
</script>

<style scoped>

.help {
  padding: 50px 20px;
  text-align: center;
  background-color: #1c1c1c;
  border-radius: 10px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.5);
}

.help h1 {
  font-size: 32px;
  margin-bottom: 15px;
  color: #f0f0f0;
}

.help p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #ddd;
}

.faq-list {
  list-style: none;
  padding: 0;
  max-width: 700px;
  margin: 0 auto;
  text-align: left;
}

.faq-item {
  margin-bottom: 20px;
}

.faq-item a {
  font-size: 18px;
  color: #f0f0f0;
  text-decoration: none;
  font-weight: bold;
  padding: 10px 15px;
  display: block;
  border-radius: 8px;
  background-color: #2b2b2b;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
}

.faq-item a:hover {
  background-color: #444;
  color: #fff;
  transform: translateY(-3px);
}

/* Responsividade */
@media (max-width: 768px) {
  .help {
    padding: 30px 15px;
  }

  .help h1 {
    font-size: 28px;
  }

  .help p {
    font-size: 16px;
  }

  .faq-item a {
    font-size: 16px;
    padding: 8px 12px;
  }
  
}
</style>
