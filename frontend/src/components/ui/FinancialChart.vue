<template>
  <div class="financial-chart">
    <div class="chart-header">
      <h3 class="chart-title">
        <i class="material-icons">{{ icon }}</i>
        {{ title }}
      </h3>
      <div class="chart-controls" v-if="showControls">
        <select v-model="selectedPeriod" @change="updateChart" class="period-select">
          <option value="7">Últimos 7 dias</option>
          <option value="30">Últimos 30 dias</option>
          <option value="90">Últimos 90 dias</option>
          <option value="365">Último ano</option>
        </select>
        <button @click="refreshChart" class="refresh-btn" :disabled="isLoading">
          <i class="material-icons" :class="{ 'spinning': isLoading }">refresh</i>
        </button>
      </div>
    </div>
    
    <div class="chart-container" :class="{ 'loading': isLoading }">
      <div v-if="isLoading" class="chart-loading">
        <div class="loading-spinner"></div>
        <p>Carregando dados...</p>
      </div>
      
      <div v-else-if="hasData" class="chart-content">
        <!-- Gráfico de Barras -->
        <div v-if="type === 'bar'" class="bar-chart">
          <div class="chart-grid">
            <div 
              v-for="(item, index) in chartData" 
              :key="index"
              class="bar-item"
              :style="{ '--delay': index * 0.1 + 's' }"
            >
              <div class="bar-container">
                <div 
                  class="bar orcamento"
                  :style="{ height: getBarHeight(item.orcamento, maxValue) + '%' }"
                  :title="`Orçamento: R$ ${formatCurrency(item.orcamento)}`"
                ></div>
                <div 
                  class="bar custo"
                  :style="{ height: getBarHeight(item.custo, maxValue) + '%' }"
                  :title="`Custo Real: R$ ${formatCurrency(item.custo)}`"
                ></div>
              </div>
              <div class="bar-label">{{ item.label }}</div>
              <div class="bar-values">
                <span class="value orcamento">R$ {{ formatCurrency(item.orcamento) }}</span>
                <span class="value custo">R$ {{ formatCurrency(item.custo) }}</span>
              </div>
            </div>
          </div>
          
          <div class="chart-legend">
            <div class="legend-item">
              <div class="legend-color orcamento"></div>
              <span>Orçamento Previsto</span>
            </div>
            <div class="legend-item">
              <div class="legend-color custo"></div>
              <span>Custo Real</span>
            </div>
          </div>
        </div>
        
        <!-- Gráfico de Pizza -->
        <div v-else-if="type === 'pie'" class="pie-chart">
          <div class="pie-container">
            <svg class="pie-svg" viewBox="0 0 200 200">
              <circle
                v-for="(segment, index) in pieSegments"
                :key="index"
                :cx="100"
                :cy="100"
                :r="80"
                :stroke="segment.color"
                :stroke-width="20"
                :stroke-dasharray="segment.dashArray"
                :stroke-dashoffset="segment.dashOffset"
                :style="{ '--delay': index * 0.2 + 's' }"
                class="pie-segment"
                fill="transparent"
              />
              <text x="100" y="100" text-anchor="middle" dy="0.3em" class="pie-center-text">
                {{ centerText }}
              </text>
            </svg>
          </div>
          
          <div class="pie-legend">
            <div 
              v-for="(item, index) in chartData" 
              :key="index"
              class="legend-item"
              :style="{ '--delay': index * 0.1 + 's' }"
            >
              <div class="legend-color" :style="{ backgroundColor: item.color }"></div>
              <div class="legend-content">
                <span class="legend-label">{{ item.label }}</span>
                <span class="legend-value">R$ {{ formatCurrency(item.value) }}</span>
                <span class="legend-percentage">{{ item.percentage }}%</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Gráfico de Linha -->
        <div v-else-if="type === 'line'" class="line-chart">
          <div class="line-container">
            <svg class="line-svg" viewBox="0 0 400 200">
              <!-- Grid lines -->
              <defs>
                <pattern id="grid" width="40" height="20" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#grid)" />
              
              <!-- Área do gráfico -->
              <path
                :d="areaPath"
                fill="url(#areaGradient)"
                class="line-area"
              />
              
              <!-- Linha principal -->
              <path
                :d="linePath"
                fill="none"
                stroke="var(--primary-color)"
                stroke-width="3"
                class="line-path"
              />
              
              <!-- Pontos -->
              <circle
                v-for="(point, index) in linePoints"
                :key="index"
                :cx="point.x"
                :cy="point.y"
                r="4"
                fill="var(--primary-color)"
                class="line-point"
                :style="{ '--delay': index * 0.1 + 's' }"
              />
              
              <!-- Gradiente para área -->
              <defs>
                <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:var(--primary-color);stop-opacity:0.3" />
                  <stop offset="100%" style="stop-color:var(--primary-color);stop-opacity:0" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          
          <div class="line-labels">
            <div 
              v-for="(item, index) in chartData" 
              :key="index"
              class="line-label"
            >
              {{ item.label }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="chart-empty">
        <i class="material-icons">bar_chart</i>
        <p>Nenhum dado disponível</p>
        <button @click="refreshChart" class="retry-btn">
          <i class="material-icons">refresh</i>
          Tentar novamente
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FinancialChart',
  props: {
    title: {
      type: String,
      default: 'Gráfico Financeiro'
    },
    icon: {
      type: String,
      default: 'bar_chart'
    },
    type: {
      type: String,
      default: 'bar', // 'bar', 'pie', 'line'
      validator: value => ['bar', 'pie', 'line'].includes(value)
    },
    data: {
      type: Array,
      default: () => []
    },
    showControls: {
      type: Boolean,
      default: true
    },
    centerText: {
      type: String,
      default: 'Total'
    }
  },
  emits: ['period-change', 'refresh'],
  data() {
    return {
      selectedPeriod: 30,
      isLoading: false
    };
  },
  computed: {
    hasData() {
      return this.chartData.length > 0;
    },
    
    chartData() {
      if (!this.data || this.data.length === 0) return [];
      
      // Processar dados baseado no tipo de gráfico
      switch (this.type) {
        case 'pie':
          return this.processPieData();
        case 'line':
          return this.processLineData();
        default:
          return this.processBarData();
      }
    },
    
    maxValue() {
      if (this.type !== 'bar') return 0;
      
      return Math.max(
        ...this.chartData.flatMap(item => [item.orcamento || 0, item.custo || 0])
      );
    },
    
    pieSegments() {
      if (this.type !== 'pie') return [];
      
      const total = this.chartData.reduce((sum, item) => sum + item.value, 0);
      let currentOffset = 0;
      
      return this.chartData.map(item => {
        const percentage = (item.value / total) * 100;
        const circumference = 2 * Math.PI * 80; // raio = 80
        const dashArray = `${(percentage / 100) * circumference} ${circumference}`;
        const dashOffset = -currentOffset;
        
        currentOffset += (percentage / 100) * circumference;
        
        return {
          dashArray,
          dashOffset,
          color: item.color
        };
      });
    },
    
    linePoints() {
      if (this.type !== 'line') return [];
      
      const maxValue = Math.max(...this.chartData.map(item => item.value));
      const width = 400;
      const height = 200;
      const padding = 20;
      
      return this.chartData.map((item, index) => ({
        x: padding + (index * (width - 2 * padding)) / (this.chartData.length - 1),
        y: height - padding - ((item.value / maxValue) * (height - 2 * padding))
      }));
    },
    
    linePath() {
      if (this.linePoints.length === 0) return '';
      
      return this.linePoints.reduce((path, point, index) => {
        const command = index === 0 ? 'M' : 'L';
        return `${path} ${command} ${point.x} ${point.y}`;
      }, '');
    },
    
    areaPath() {
      if (this.linePoints.length === 0) return '';
      
      const firstPoint = this.linePoints[0];
      const lastPoint = this.linePoints[this.linePoints.length - 1];
      
      return `${this.linePath} L ${lastPoint.x} 180 L ${firstPoint.x} 180 Z`;
    }
  },
  methods: {
    processBarData() {
      return this.data.map(item => ({
        label: item.label || item.categoria || 'N/A',
        orcamento: parseFloat(item.orcamento_previsto || item.orcamento || 0),
        custo: parseFloat(item.custo_real || item.custo || 0)
      }));
    },
    
    processPieData() {
      const colors = [
        'var(--primary-color)',
        'var(--secondary-color)',
        'var(--success-color)',
        'var(--warning-color)',
        'var(--info-color)',
        'var(--danger-color)'
      ];
      
      const total = this.data.reduce((sum, item) => sum + parseFloat(item.value || item.custo_real || 0), 0);
      
      return this.data.map((item, index) => {
        const value = parseFloat(item.value || item.custo_real || 0);
        return {
          label: item.label || item.categoria || 'N/A',
          value,
          percentage: total > 0 ? Math.round((value / total) * 100) : 0,
          color: item.color || colors[index % colors.length]
        };
      });
    },
    
    processLineData() {
      return this.data.map(item => ({
        label: item.label || item.data || 'N/A',
        value: parseFloat(item.value || item.total || 0)
      }));
    },
    
    getBarHeight(value, max) {
      if (max === 0) return 0;
      return Math.max((value / max) * 100, 2); // Mínimo de 2% para visibilidade
    },
    
    formatCurrency(value) {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    
    updateChart() {
      this.$emit('period-change', this.selectedPeriod);
    },
    
    async refreshChart() {
      this.isLoading = true;
      this.$emit('refresh');
      
      // Simular delay de carregamento
      setTimeout(() => {
        this.isLoading = false;
      }, 1000);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

:root {
  --primary-color: #ff6f61;
  --secondary-color: #4db6ac;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --danger-color: #e74c3c;
  --info-color: #3498db;
  --card-bg: #2a2a2a;
  --border-color: #333;
  --text-primary: #f5f5f5;
  --text-secondary: #999;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.financial-chart {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--border-color);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.chart-title {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.chart-title i {
  color: var(--primary-color);
  font-size: 20px;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.period-select {
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 12px;
  cursor: pointer;
  transition: var(--transition);
}

.period-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.period-select option {
  background: var(--card-bg);
  color: var(--text-primary);
}

.refresh-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.refresh-btn:hover:not(:disabled) {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refresh-btn .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chart-container {
  flex: 1;
  position: relative;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-container.loading {
  pointer-events: none;
}

.chart-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(42, 42, 42, 0.9);
  border-radius: 8px;
  z-index: 10;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 111, 97, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

.chart-loading p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.chart-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Gráfico de Barras */
.bar-chart {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart-grid {
  flex: 1;
  display: flex;
  align-items: flex-end;
  gap: 16px;
  padding: 20px 0;
  min-height: 200px;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: slideUp 0.6s ease-out var(--delay);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.bar-container {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 150px;
  margin-bottom: 8px;
}

.bar {
  width: 20px;
  border-radius: 4px 4px 0 0;
  transition: var(--transition);
  position: relative;
  cursor: pointer;
}

.bar:hover {
  transform: scaleY(1.05);
  filter: brightness(1.2);
}

.bar.orcamento {
  background: linear-gradient(180deg, var(--secondary-color), #3a9b96);
}

.bar.custo {
  background: linear-gradient(180deg, var(--primary-color), #e55b55);
}

.bar-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 4px;
  font-weight: 500;
}

.bar-values {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: center;
}

.value {
  font-size: 10px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.value.orcamento {
  color: var(--secondary-color);
}

.value.custo {
  color: var(--primary-color);
}

/* Gráfico de Pizza */
.pie-chart {
  flex: 1;
  display: flex;
  gap: 32px;
  align-items: center;
}

.pie-container {
  flex-shrink: 0;
}

.pie-svg {
  width: 200px;
  height: 200px;
  transform: rotate(-90deg);
}

.pie-segment {
  transition: var(--transition);
  animation: drawSegment 1s ease-out var(--delay);
}

@keyframes drawSegment {
  from {
    stroke-dashoffset: 502; /* Circunferência completa */
  }
  to {
    stroke-dashoffset: var(--final-offset);
  }
}

.pie-center-text {
  font-size: 14px;
  font-weight: 600;
  fill: var(--text-primary);
  transform: rotate(90deg);
  transform-origin: center;
}

.pie-legend {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: 6px;
  transition: var(--transition);
  animation: fadeInRight 0.6s ease-out var(--delay);
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.legend-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
}

.legend-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.legend-label {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.legend-value {
  font-size: 12px;
  color: var(--text-secondary);
  font-family: 'Courier New', monospace;
}

.legend-percentage {
  font-size: 11px;
  color: var(--primary-color);
  font-weight: 600;
}

/* Gráfico de Linha */
.line-chart {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.line-container {
  flex: 1;
  margin-bottom: 16px;
}

.line-svg {
  width: 100%;
  height: 200px;
}

.line-area {
  animation: drawArea 1.5s ease-out;
}

.line-path {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: drawLine 2s ease-out forwards;
}

@keyframes drawLine {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes drawArea {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.line-point {
  animation: popIn 0.6s ease-out var(--delay);
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.line-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
}

.line-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-align: center;
}

/* Legenda Geral */
.chart-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.chart-legend .legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.chart-legend .legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.chart-legend .legend-color.orcamento {
  background: var(--secondary-color);
}

.chart-legend .legend-color.custo {
  background: var(--primary-color);
}

/* Estado Vazio */
.chart-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  gap: 16px;
}

.chart-empty i {
  font-size: 48px;
  opacity: 0.5;
}

.chart-empty p {
  margin: 0;
  font-size: 16px;
}

.retry-btn {
  padding: 8px 16px;
  background: var(--primary-color);
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: var(--transition);
}

.retry-btn:hover {
  background: #e55b55;
  transform: translateY(-1px);
}

/* Responsividade */
@media (max-width: 768px) {
  .financial-chart {
    padding: 16px;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chart-grid {
    gap: 8px;
  }
  
  .bar {
    width: 16px;
  }
  
  .pie-chart {
    flex-direction: column;
    gap: 24px;
  }
  
  .pie-svg {
    width: 150px;
    height: 150px;
  }
  
  .chart-legend {
    flex-wrap: wrap;
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .chart-container {
    min-height: 250px;
  }
  
  .chart-grid {
    min-height: 150px;
  }
  
  .bar-container {
    height: 100px;
  }
  
  .pie-svg {
    width: 120px;
    height: 120px;
  }
  
  .line-svg {
    height: 150px;
  }
}
</style> 