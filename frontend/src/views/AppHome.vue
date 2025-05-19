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
  margin-bottom: var(--spacing-md);
}

.logo {
  max-width: 11.25rem; /* Convertido de 180px para rem */
  height: auto;
}

.welcome-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--spacing-xl) var(--spacing-md);
}

/* Os estilos de h1 e p estão definidos globalmente, apenas sobrescrevendo o específico */
h1 {
  font-size: var(--font-size-4xl); /* Equivalente a 42px */
}

p {
  font-size: var(--font-size-lg);
  max-width: 37.5rem; /* Convertido de 600px para rem */
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xxl);
}

/* Botões já estão no estilo global, removidos daqui */

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5625rem; /* Convertido de 25px para rem */
  width: 100%;
  max-width: 62.5rem; /* Convertido de 1000px para rem */
}

.feature-card {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  padding: var(--spacing-xl) var(--spacing-md);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.3);
  flex: 1;
  min-width: 15.625rem; /* Convertido de 250px para rem */
  max-width: 18.75rem; /* Convertido de 300px para rem */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-0.3125rem); /* Convertido de -5px para rem */
  box-shadow: 0 0.75rem 1.25rem rgba(0, 0, 0, 0.4);
}

.feature-icon {
  font-size: 2.375rem; /* Convertido de 38px para rem */
  margin-bottom: var(--spacing-md);
  color: #fff;
}

.feature-card h3 {
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-sm);
  color: #fff;
}

.feature-card p {
  font-size: var(--font-size-md);
  color: #aaa;
  margin-bottom: 0;
}

/* Responsividade */
@media (max-width: 1024px) {
  h1 {
    font-size: var(--font-size-3xl);
  }
  
  .features {
    gap: var(--spacing-md);
  }
  
  .feature-card {
    min-width: 13.75rem; /* Convertido de 220px para rem */
  }
}

@media (max-width: 768px) {
  h1 {
    font-size: var(--font-size-xxl);
  }
  
  p {
    font-size: var(--font-size-md);
  }
  
  .action-buttons {
    flex-direction: column;
    gap: var(--spacing-sm);
    width: 100%;
    max-width: 18.75rem; /* Convertido de 300px para rem */
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
    font-size: var(--font-size-xl);
  }
  
  p {
    font-size: var(--font-size-sm);
  }
  
  .feature-card {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  .feature-icon {
    font-size: 2rem; /* Convertido de 32px para rem */
  }
  
  .feature-card h3 {
    font-size: var(--font-size-lg);
  }
  
  .feature-card p {
    font-size: var(--font-size-sm);
  }
}
</style>
