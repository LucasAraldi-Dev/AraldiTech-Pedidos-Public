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
  z-index: var(--z-index-overlay);
  backdrop-filter: blur(0.125rem);
}

.loading-container.inline {
  display: inline-flex;
  margin: 0 var(--spacing-xs);
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  background-color: rgba(0, 0, 0, 0.7);
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.loading-message {
  color: #fff;
  margin-top: var(--spacing-sm);
  text-align: center;
  font-size: var(--font-size-sm);
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
  width: 0.75rem;
  height: 0.75rem;
  margin: 0 0.25rem;
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
  width: 0.5rem;
  height: 0.5rem;
  margin: 0 0.1875rem;
}

.size-small .loading-message {
  font-size: var(--font-size-xs);
}

.size-large .circle {
  width: 1rem;
  height: 1rem;
  margin: 0 0.3125rem;
}

.size-large .loading-message {
  font-size: var(--font-size-md);
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
    padding: 0.75rem;
    max-width: 90%;
  }
  
  .loading-message {
    font-size: var(--font-size-xs);
    margin-top: 0.75rem;
  }
}
</style> 