<template>
  <main>
    <section class="contact">
      <h1>Entre em Contato com a AraldiTech</h1>
      <p>Preencha o formulário abaixo para enviar uma mensagem.</p>
      <form>
        <div class="form-group">
          <label for="name">Seu nome:</label>
          <input id="name" type="text" placeholder="Seu nome" />
        </div>
        <div class="form-group">
          <label for="email">Seu e-mail:</label>
          <input id="email" type="email" placeholder="Seu e-mail" />
        </div>
        <div class="form-group">
          <label for="message">Sua mensagem:</label>
          <textarea id="message" placeholder="Sua mensagem"></textarea>
        </div>
        <div class="form-group">
          <button class="btn-submit" type="submit">Enviar</button>
        </div>
      </form>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AppContato'
}
</script>

<style scoped>

.contact {
  padding: 50px 20px;
  background: #1c1c1c;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.5);
}

.contact h1 {
  font-size: 32px;
  margin-bottom: 15px;
  color: #f0f0f0;
}

.contact p {
  font-size: 18px;
  margin-bottom: 30px;
  color: #ddd;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
  background: #2b2b2b;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.6);
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  font-size: 16px;
  margin-bottom: 8px;
  color: #c0c0c0;
  display: block;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #333;
  color: #f0f0f0;
  font-size: 16px;
  box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.4);
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #777;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #555;
  box-shadow: 0 0 8px rgba(85, 85, 85, 0.7);
  outline: none;
}

.form-group textarea {
  resize: none;
  min-height: 150px;
}

.btn-submit {
  padding: 15px 30px;
  font-size: 16px;
  font-weight: bold;
  color: #f0f0f0;
  background: #444;
  border: 2px solid #555;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  width: 100%;
  max-width: 200px;
}

.btn-submit:hover {
  background: #555;
  transform: translateY(-3px);
}

@media (max-width: 390px) {
  .contact {
    padding: 20px 10px;
  }

  .contact h1 {
    font-size: 20px;
    margin-bottom: 10px;
  }

  .contact p {
    font-size: 12px;
    margin-bottom: 15px;
  }

  form {
    padding: 15px;
  }

  .form-group input,
  .form-group textarea {
    font-size: 12px;
  }

  .btn-submit {
    padding: 8px 15px;
    font-size: 12px;
  }
}
</style>
