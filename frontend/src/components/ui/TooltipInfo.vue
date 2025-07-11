<template>
  <div class="tooltip-container" ref="container">
    <!-- Ícone de informação que ativa o tooltip -->
    <div 
      class="tooltip-trigger"
      @mouseenter="showTooltip" 
      @mouseleave="hideTooltip"
      @click="toggleTooltip"
    >
      <slot name="trigger">
        <i class="material-icons info-icon">info</i>
      </slot>
    </div>
    
    <!-- Conteúdo do tooltip -->
    <div 
      v-if="isVisible" 
      class="tooltip-content"
      :class="[positionClass, { 'mobile-tooltip': isMobile }]"
      :style="computedStyle"
      ref="tooltip"
    >
      <!-- Cabeçalho do tooltip para dispositivos móveis -->
      <div class="tooltip-header">
        <div class="tooltip-title">{{ title }}</div>
        <button class="tooltip-close" @click="hideTooltip">
          <i class="material-icons">close</i>
        </button>
      </div>
      
      <!-- Conteúdo personalizado via slot -->
      <div class="tooltip-body">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TooltipInfo',
  props: {
    /**
     * Título do tooltip (exibido no cabeçalho em dispositivos móveis)
     */
    title: {
      type: String,
      default: 'Informação'
    },
    /**
     * Posição do tooltip em relação ao trigger
     * Valores possíveis: 'top', 'bottom', 'left', 'right'
     */
    position: {
      type: String,
      default: 'right',
      validator: (value) => ['top', 'right', 'bottom', 'left'].includes(value)
    },
    /**
     * Largura máxima do tooltip em pixels
     */
    maxWidth: {
      type: Number,
      default: 250
    }
  },
  data() {
    return {
      isVisible: false,
      isMobile: false,
      adjustedPosition: this.position,
      tooltipOffset: { top: 0, left: 0 }
    };
  },
  computed: {
    positionClass() {
      return `tooltip-${this.adjustedPosition}`;
    },
    computedStyle() {
      return {
        maxWidth: `${this.maxWidth}px`,
        top: `${this.tooltipOffset.top}px`,
        left: `${this.tooltipOffset.left}px`
      };
    }
  },
  mounted() {
    // Verificar se é dispositivo móvel
    this.isMobile = window.innerWidth < 768;
    
    // Adicionar listener para resize da janela
    window.addEventListener('resize', this.checkMobile);
  },
  beforeUnmount() {
    // Remover listener quando o componente for desmontado
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    /**
     * Mostrar o tooltip
     */
    showTooltip() {
      if (this.isMobile) return; // Em móvel, só mostra ao clicar
      this.isVisible = true;
      this.$nextTick(() => this.adjustPosition());
    },
    
    /**
     * Esconder o tooltip
     */
    hideTooltip() {
      this.isVisible = false;
    },
    
    /**
     * Alternar a visibilidade do tooltip
     */
    toggleTooltip() {
      this.isVisible = !this.isVisible;
      if (this.isVisible) {
        this.$nextTick(() => this.adjustPosition());
      }
    },
    
    /**
     * Verificar se o dispositivo é móvel
     */
    checkMobile() {
      this.isMobile = window.innerWidth < 768;
    },
    
    adjustPosition() {
      if (!this.$refs.tooltip || !this.$refs.container) return;
      
      const tooltip = this.$refs.tooltip;
      const container = this.$refs.container;
      const triggerRect = container.getBoundingClientRect();
      
      // Reset position to calculate correct dimensions
      tooltip.style.top = '0px';
      tooltip.style.left = '0px';
      
      const tooltipRect = tooltip.getBoundingClientRect();
      
      // Get viewport dimensions
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      
      // Default positions
      let top = 0;
      let left = 0;
      
      // Espaçamento entre o tooltip e o trigger (em pixels)
      const spacing = 0.625; // 10px em rem
      
      // Margem de segurança da borda da tela (em pixels)
      const safetyMargin = 1.25; // 20px em rem
      
      // Calculate best position based on available space
      // First, try the requested position
      this.adjustedPosition = this.position;
      
      // Calculate positions based on preferred direction
      if (this.position === 'right') {
        left = triggerRect.right + spacing * 16; // Convertendo rem para px aproximado
        top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
        
        // Check if tooltip would go off-screen to the right
        if (left + tooltipRect.width > viewportWidth - safetyMargin * 16) {
          // Try left position instead
          this.adjustedPosition = 'left';
          left = triggerRect.left - tooltipRect.width - spacing * 16;
        }
      } else if (this.position === 'left') {
        left = triggerRect.left - tooltipRect.width - spacing * 16;
        top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
        
        // Check if tooltip would go off-screen to the left
        if (left < safetyMargin * 16) {
          // Try right position instead
          this.adjustedPosition = 'right';
          left = triggerRect.right + spacing * 16;
          
          // If still off-screen, try bottom
          if (left + tooltipRect.width > viewportWidth - safetyMargin * 16) {
            this.adjustedPosition = 'bottom';
            left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
            top = triggerRect.bottom + spacing * 16;
          }
        }
      } else if (this.position === 'top') {
        left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
        top = triggerRect.top - tooltipRect.height - spacing * 16;
        
        // Check if tooltip would go off-screen to the top
        if (top < safetyMargin * 16) {
          // Try bottom position instead
          this.adjustedPosition = 'bottom';
          top = triggerRect.bottom + spacing * 16;
        }
      } else if (this.position === 'bottom') {
        left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
        top = triggerRect.bottom + spacing * 16;
        
        // Check if tooltip would go off-screen to the bottom
        if (top + tooltipRect.height > viewportHeight - safetyMargin * 16) {
          // Try top position instead
          this.adjustedPosition = 'top';
          top = triggerRect.top - tooltipRect.height - spacing * 16;
        }
      }
      
      // Horizontal boundary adjustments
      if (left < safetyMargin * 16) {
        left = safetyMargin * 16;
      } else if (left + tooltipRect.width > viewportWidth - safetyMargin * 16) {
        left = viewportWidth - tooltipRect.width - safetyMargin * 16;
      }
      
      // Vertical boundary adjustments
      if (top < safetyMargin * 16) {
        top = safetyMargin * 16;
      } else if (top + tooltipRect.height > viewportHeight - safetyMargin * 16) {
        top = viewportHeight - tooltipRect.height - safetyMargin * 16;
      }
      
      // Update position
      this.tooltipOffset = { top, left };
    }
  }
};
</script>

<style scoped>
.tooltip-container {
  position: relative;
  display: inline-block;
  z-index: 10;
}

.tooltip-trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.info-icon {
  color: #66ccff;
  font-size: var(--font-size-md);
  opacity: 0.8;
  transition: opacity 0.2s;
}

.info-icon:hover {
  opacity: 1;
}

/* Conteúdo do tooltip */
.tooltip-content {
  position: fixed;
  background-color: #2c2c2c;
  color: #f5f5f5;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm);
  z-index: var(--z-index-modal);
  box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.5);
  border: 1px solid #444;
  width: 100%;
  pointer-events: auto;
}

/* Posições */
.tooltip-right::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -0.625rem;
  transform: translateY(-50%);
  border-width: 0.625rem 0.625rem 0.625rem 0;
  border-style: solid;
  border-color: transparent #2c2c2c transparent transparent;
}

.tooltip-left::before {
  content: '';
  position: absolute;
  top: 50%;
  right: -0.625rem;
  transform: translateY(-50%);
  border-width: 0.625rem 0 0.625rem 0.625rem;
  border-style: solid;
  border-color: transparent transparent transparent #2c2c2c;
}

.tooltip-top::before {
  content: '';
  position: absolute;
  bottom: -0.625rem;
  left: 50%;
  transform: translateX(-50%);
  border-width: 0.625rem 0.625rem 0;
  border-style: solid;
  border-color: #2c2c2c transparent transparent;
}

.tooltip-bottom::before {
  content: '';
  position: absolute;
  top: -0.625rem;
  left: 50%;
  transform: translateX(-50%);
  border-width: 0 0.625rem 0.625rem;
  border-style: solid;
  border-color: transparent transparent #2c2c2c;
}

/* Cabeçalho em dispositivos móveis */
.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
  padding-bottom: var(--spacing-xs);
  border-bottom: 1px solid #444;
}

.tooltip-title {
  font-weight: bold;
  color: #66ccff;
}

.tooltip-close {
  background: transparent;
  border: none;
  color: #999;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 50%;
}

.tooltip-close:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.tooltip-body {
  font-size: var(--font-size-sm);
  line-height: 1.4;
}

/* Mobile styling */
.mobile-tooltip {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  width: 80% !important;
  max-height: 80vh !important;
  overflow-y: auto !important;
  z-index: 2000 !important;
}

.mobile-tooltip::before {
  display: none !important;
}

/* Material icons */
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
</style> 