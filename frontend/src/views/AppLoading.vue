<template>
  <div class="loading-container">
    <div class="content">
      <h1>AraldiTech</h1>
      <p class="tagline">Sistema de Pedidos</p>
      
      <div class="loading-status">
        <div class="progress-bar">
          <div class="progress" :style="{ width: `${loadingProgress}%` }"></div>
        </div>
        <p class="status-message">{{ currentStatusMessage }}</p>
      </div>
      
      <div class="loading-modules">
        <div v-for="(module, index) in modules" :key="index" class="module-item" :class="{ 'loaded': module.loaded }">
          <div class="module-icon">
            <div class="module-icon-inner">
              <i :class="module.icon"></i>
            </div>
          </div>
          <div class="module-info">
            <span class="module-name">{{ module.name }}</span>
            <span class="module-status">{{ module.loaded ? 'Carregado' : 'Carregando...' }}</span>
          </div>
          <div class="module-check" v-if="module.loaded">✓</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppLoading',
  data() {
    return {
      loadingProgress: 0,
      statusMessages: [
        'Inicializando sistema...',
        'Carregando módulos...',
        'Verificando dados...',
        'Preparando interface...',
        'Carregando preferências do usuário...',
        'Quase pronto!'
      ],
      currentStatusIndex: 0,
      modules: [
        { name: 'Core do Sistema', icon: 'system-icon', loaded: false },
        { name: 'Interface de Usuário', icon: 'ui-icon', loaded: false },
        { name: 'Gestor de Pedidos', icon: 'orders-icon', loaded: false },
        { name: 'Sistema de Relatórios', icon: 'reports-icon', loaded: false },
        { name: 'Banco de Dados', icon: 'database-icon', loaded: false },
      ]
    };
  },
  computed: {
    currentStatusMessage() {
      return this.statusMessages[this.currentStatusIndex];
    }
  },
  mounted() {
    this.startLoading();
  },
  methods: {
    startLoading() {
      // Simulação de carregamento progressivo
      let progress = 0;
      const user = JSON.parse(localStorage.getItem('user')) || {};
      const userName = user.nome || 'usuário';
      
      // Adicionar mensagem personalizada ao final
      this.statusMessages.push(`Preparando ambiente para ${userName}...`);
      
      const interval = setInterval(() => {
        progress += Math.random() * 3;
        this.loadingProgress = Math.min(progress, 100);
        
        // Atualizar mensagem de status conforme o progresso
        this.currentStatusIndex = Math.min(
          Math.floor(this.loadingProgress / (100 / this.statusMessages.length)),
          this.statusMessages.length - 1
        );
        
        // Carregar módulos em ordem
        const moduleIndex = Math.floor(this.loadingProgress / 20);
        for (let i = 0; i <= moduleIndex && i < this.modules.length; i++) {
          if (!this.modules[i].loaded) {
            setTimeout(() => {
              this.modules[i].loaded = true;
            }, i * 400);
          }
        }
        
        // Quando terminar o carregamento
        if (this.loadingProgress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            this.$router.push({ name: 'Menu' });
          }, 1000);
        }
      }, 100);
    }
  }
};
</script>

<style scoped>
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  background-color: #2c2c2c;
}

.content {
  padding: 40px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.4);
}

h1 {
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
}

.tagline {
  font-size: 16px;
  color: #bbb;
  text-align: center;
  margin: 0 0 30px;
}

.loading-status {
  margin-bottom: 30px;
}

.progress-bar {
  height: 6px;
  width: 100%;
  background: #444;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress {
  height: 100%;
  background: #66ccff;
  width: 0;
  transition: width 0.3s ease;
  border-radius: 3px;
}

.status-message {
  font-size: 16px;
  color: #ddd;
  text-align: center;
  margin: 0;
  min-height: 24px;
}

.loading-modules {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.module-item {
  display: flex;
  align-items: center;
  background: #444;
  border-radius: 8px;
  padding: 12px 15px;
  transition: all 0.3s ease;
  border: 1px solid #555;
}

.module-item.loaded {
  background: #444;
  border-left: 3px solid #66ccff;
}

.module-icon {
  margin-right: 15px;
}

.module-icon-inner {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #555;
  display: flex;
  align-items: center;
  justify-content: center;
}

.module-item.loaded .module-icon-inner {
  background: #555;
  border: 1px solid #66ccff;
}

.module-icon i {
  font-size: 16px;
  color: #bbb;
}

.module-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.module-name {
  font-size: 14px;
  font-weight: 500;
}

.module-status {
  font-size: 12px;
  color: #bbb;
}

.module-item.loaded .module-status {
  color: #66ccff;
}

.module-check {
  color: #66ccff;
  font-size: 18px;
  font-weight: bold;
}

/* Icones personalizados com uso de SVG em data-url */
.system-icon::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M4 6h16v10H4V6zm16 12H4a2 2 0 0 1-2-2V6c0-1.1.9-2 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2z' fill='%23bbb'/%3E%3Cpath d='M12 15c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1z' fill='%23bbb'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.ui-icon::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M3 3h18v2H3V3zm0 16h18v2H3v-2zm0-8h18v2H3v-2z' fill='%23bbb'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.orders-icon::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-5-7V8h-2v4H8l4 4 4-4h-2z' fill='%23bbb'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.reports-icon::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7v-7zm4-3h2v10h-2V7zm4 6h2v4h-2v-4z' fill='%23bbb'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

.database-icon::before {
  content: '';
  display: inline-block;
  width: 18px;
  height: 18px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='24' height='24'%3E%3Cpath fill='none' d='M0 0h24v24H0z'/%3E%3Cpath d='M12 2C6.48 2 2 4.02 2 7v10c0 2.98 4.48 5 10 5s10-2.02 10-5V7c0-2.98-4.48-5-10-5zm0 13c-3.31 0-6-1.34-6-3v3c0 1.66 2.69 3 6 3s6-1.34 6-3v-3c0 1.66-2.69 3-6 3zm0-6c-3.31 0-6-1.34-6-3s2.69-3 6-3 6 1.34 6 3-2.69 3-6 3z' fill='%23bbb'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
}

/* Responsividade */
@media (max-width: 768px) {
  .content {
    padding: 30px;
    width: 95%;
    max-width: 450px;
  }
}

@media (max-width: 480px) {
  .content {
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  }
  
  h1 {
    font-size: 22px;
    margin-bottom: 8px;
  }
  
  .tagline {
    font-size: 14px;
    margin-bottom: 25px;
  }
  
  .loading-status {
    margin-bottom: 25px;
  }
  
  .module-item {
    padding: 10px;
  }
  
  .module-icon-inner {
    width: 30px;
    height: 30px;
  }
}

@media (max-width: 320px) {
  .content {
    padding: 20px;
  }
  
  h1 {
    font-size: 20px;
  }
}
</style> 