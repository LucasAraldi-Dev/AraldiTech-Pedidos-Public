<template>
  <div class="loading-container" :class="{ 'overlay': overlay, 'inline': !overlay }">
    <div class="loading-indicator" :class="sizeClass">
      <div class="spinner">
        <!-- Círculos animados -->
        <div class="circle"></div>
        <div class="circle"></div>
        <div class="circle"></div>
      </div>
      <!-- Mensagem opcional -->
      <div v-if="message" class="loading-message">{{ message }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    /**
     * Mensagem a ser exibida junto com o indicador
     */
    message: {
      type: String,
      default: ''
    },
    /**
     * Se o indicador deve ser exibido como overlay ou inline
     */
    overlay: {
      type: Boolean,
      default: false
    },
    /**
     * Tamanho do indicador: 'small', 'medium' ou 'large'
     */
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  computed: {
    /**
     * Classe CSS com base no tamanho
     */
    sizeClass() {
      return `size-${this.size}`;
    }
  }
}
</script>

<style scoped>
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-container.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.loading-container.inline {
  display: inline-flex;
  margin: 0 10px;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.7);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.loading-message {
  color: #fff;
  margin-top: 15px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
}

/* Spinner */
.spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.circle {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin: 0 4px;
  border-radius: 50%;
  background-color: #ff6f61;
  animation: bounce 1.4s infinite ease-in-out both;
}

.circle:nth-child(1) {
  animation-delay: -0.32s;
}

.circle:nth-child(2) {
  animation-delay: -0.16s;
}

/* Tamanhos */
.size-small .circle {
  width: 8px;
  height: 8px;
  margin: 0 3px;
}

.size-small .loading-message {
  font-size: 12px;
}

.size-large .circle {
  width: 16px;
  height: 16px;
  margin: 0 5px;
}

.size-large .loading-message {
  font-size: 16px;
}

/* Animação de bounce */
@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0);
  } 
  40% { 
    transform: scale(1.0);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .loading-indicator {
    padding: 12px;
    max-width: 90%;
  }
  
  .loading-message {
    font-size: 13px;
    margin-top: 12px;
  }
}
</style> 