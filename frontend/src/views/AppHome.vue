<template>
  <main class="home-page">
    <section class="welcome-section">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="AraldiTech" class="logo" onerror="this.src='favicon.ico'">
      </div>
      <h1>AraldiTech Pedidos</h1>
      <p>Gerencie seus pedidos de forma rápida e eficiente</p>
      
      <div class="action-buttons">
        <router-link to="/login" class="btn-primary">Entrar</router-link>
        <router-link to="/contato" class="btn-secondary">Contato</router-link>
      </div>
      
      <div class="features">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-clipboard-list"></i>
          </div>
          <h3>Gerenciamento</h3>
          <p>Controle todos os seus pedidos em um só lugar</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-chart-bar"></i>
          </div>
          <h3>Relatórios</h3>
          <p>Analise seus dados com relatórios detalhados</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <i class="fas fa-users"></i>
          </div>
          <h3>Colaboração</h3>
          <p>Trabalhe em equipe com diferentes níveis de acesso</p>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: 'AppHome'
}
</script>

<style scoped>
/* Componentes específicos desta página */
.logo-container {
  margin-bottom: 20px;
}

.logo {
  max-width: 180px;
  height: auto;
}

.welcome-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 40px 20px;
}

/* Os estilos de h1 e p estão definidos globalmente, apenas sobrescrevendo o específico */
h1 {
  font-size: 42px;
}

p {
  font-size: 18px;
  max-width: 600px;
}

.action-buttons {
  display: flex;
  gap: 20px;
  margin-bottom: 50px;
}

/* Botões já estão no estilo global, removidos daqui */

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 25px;
  width: 100%;
  max-width: 1000px;
}

.feature-card {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: 30px 20px;
  border-radius: 12px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  flex: 1;
  min-width: 250px;
  max-width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.4);
}

.feature-icon {
  font-size: 38px;
  margin-bottom: 16px;
  color: #fff;
}

.feature-card h3 {
  font-size: 22px;
  margin-bottom: 12px;
  color: #fff;
}

.feature-card p {
  font-size: 15px;
  color: #aaa;
  margin-bottom: 0;
}

/* Responsividade */
@media (max-width: 1024px) {
  h1 {
    font-size: 38px;
  }
  
  .features {
    gap: 20px;
  }
  
  .feature-card {
    min-width: 220px;
  }
}

@media (max-width: 768px) {
  h1 {
    font-size: 36px;
  }
  
  p {
    font-size: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 15px;
    width: 100%;
    max-width: 300px;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    text-align: center;
  }
  
  .features {
    flex-direction: column;
    align-items: center;
  }
  
  .feature-card {
    width: 100%;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 28px;
  }
  
  p {
    font-size: 15px;
  }
  
  .feature-card {
    padding: 20px 15px;
  }
  
  .feature-icon {
    font-size: 32px;
  }
  
  .feature-card h3 {
    font-size: 18px;
  }
  
  .feature-card p {
    font-size: 14px;
  }
}
</style>
