<template>
  <div class="analytics-container">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <LoadingIndicator message="Carregando análises..." size="large" />
    </div>

    <div v-else class="analytics-content">
      <!-- Charts Grid -->
      <div class="charts-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">bar_chart</i>
            Análise Visual
          </h3>
          <button class="refresh-btn" @click="$emit('refresh')" :disabled="isRefreshing">
            <i class="material-icons" :class="{ 'spinning': isRefreshing }">refresh</i>
            <span>Atualizar</span>
          </button>
        </div>

        <div class="charts-grid">
          <!-- Status Chart -->
          <div class="chart-card">
            <div class="chart-header">
              <h4>Status dos Pedidos</h4>
              <div class="chart-legend">
                <div 
                  v-for="item in statusChartData" 
                  :key="item.label"
                  class="legend-item"
                >
                  <div class="legend-color" :style="{ backgroundColor: item.color }"></div>
                  <span>{{ item.label }} ({{ item.value }})</span>
                </div>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="statusChart"></canvas>
            </div>
          </div>

          <!-- Category Chart -->
          <div class="chart-card">
            <div class="chart-header">
              <h4>Pedidos por Categoria</h4>
              <div class="chart-info">
                <span>{{ categoriesCount }} categorias ativas</span>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="categoryChart"></canvas>
            </div>
          </div>

          <!-- Urgency Chart -->
          <div class="chart-card">
            <div class="chart-header">
              <h4>Distribuição por Urgência</h4>
              <div class="urgency-summary">
                <span class="critical-count">{{ urgencyStats.critico }} críticos</span>
              </div>
            </div>
            <div class="chart-container">
              <canvas ref="urgencyChart"></canvas>
            </div>
          </div>

          <!-- Timeline Chart -->
          <div class="chart-card full-width">
            <div class="chart-header">
              <h4>Pedidos ao Longo do Tempo</h4>
              <div class="timeline-controls">
                <select v-model="timelineFilter" @change="updateTimelineChart">
                  <option value="7">Últimos 7 dias</option>
                  <option value="30">Últimos 30 dias</option>
                  <option value="90">Últimos 90 dias</option>
                </select>
              </div>
            </div>
            <div class="chart-container timeline">
              <canvas ref="timelineChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Summary -->
      <div class="summary-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">insights</i>
            Insights e Tendências
          </h3>
        </div>

        <div class="insights-grid">
          <div class="insight-card">
            <div class="insight-icon">
              <i class="material-icons">trending_up</i>
            </div>
            <div class="insight-content">
              <h4>Categoria Mais Solicitada</h4>
              <div class="insight-value">{{ topCategory.name }}</div>
              <div class="insight-detail">{{ topCategory.count }} pedidos ({{ topCategory.percentage }}%)</div>
            </div>
          </div>

          <div class="insight-card">
            <div class="insight-icon warning">
              <i class="material-icons">warning</i>
            </div>
            <div class="insight-content">
              <h4>Pedidos Críticos</h4>
              <div class="insight-value">{{ urgencyStats.critico }}</div>
              <div class="insight-detail">Requerem atenção imediata</div>
            </div>
          </div>

          <div class="insight-card">
            <div class="insight-icon success">
              <i class="material-icons">speed</i>
            </div>
            <div class="insight-content">
              <h4>Taxa de Conclusão</h4>
              <div class="insight-value">{{ completionRate }}%</div>
              <div class="insight-detail">{{ completedThisMonth }} concluídos este mês</div>
            </div>
          </div>

          <div class="insight-card">
            <div class="insight-icon info">
              <i class="material-icons">schedule</i>
            </div>
            <div class="insight-content">
              <h4>Tempo Médio</h4>
              <div class="insight-value">{{ tempoMedioConclusao }}</div>
              <div class="insight-detail">Para conclusão de pedidos</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Analytics -->
      <div class="details-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">table_chart</i>
            Análise Detalhada
          </h3>
        </div>

        <div class="details-tabs">
          <button 
            v-for="tab in detailTabs" 
            :key="tab.id"
            class="detail-tab"
            :class="{ 'active': activeDetailTab === tab.id }"
            @click="activeDetailTab = tab.id"
          >
            <i class="material-icons">{{ tab.icon }}</i>
            <span>{{ tab.label }}</span>
          </button>
        </div>

        <div class="details-content">
          <!-- Performance Tab -->
          <div v-if="activeDetailTab === 'performance'" class="detail-panel">
            <div class="performance-metrics">
              <div class="metric-row">
                <span class="metric-label">Pedidos por dia (média):</span>
                <span class="metric-value">{{ dailyAverage }}</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Pico de atividade:</span>
                <span class="metric-value">{{ peakActivity.day }} ({{ peakActivity.count }} pedidos)</span>
              </div>
              <div class="metric-row">
                <span class="metric-label">Eficiência de conclusão:</span>
                <span class="metric-value">{{ completionEfficiency }}%</span>
              </div>
            </div>
          </div>

          <!-- Categories Tab -->
          <div v-if="activeDetailTab === 'categories'" class="detail-panel">
            <div class="categories-breakdown">
              <div 
                v-for="category in categoryBreakdown" 
                :key="category.name"
                class="category-item"
              >
                <div class="category-info">
                  <span class="category-name">{{ category.name }}</span>
                  <span class="category-count">{{ category.count }} pedidos</span>
                </div>
                <div class="category-bar">
                  <div 
                    class="category-fill" 
                    :style="{ width: category.percentage + '%' }"
                  ></div>
                </div>
                <span class="category-percentage">{{ category.percentage }}%</span>
              </div>
            </div>
          </div>

          <!-- Trends Tab -->
          <div v-if="activeDetailTab === 'trends'" class="detail-panel">
            <div class="trends-analysis">
              <div class="trend-item">
                <div class="trend-header">
                  <h5>Crescimento Mensal</h5>
                  <span class="trend-indicator positive">+15%</span>
                </div>
                <p>Aumento significativo no número de pedidos comparado ao mês anterior.</p>
              </div>
              <div class="trend-item">
                <div class="trend-header">
                  <h5>Sazonalidade</h5>
                  <span class="trend-indicator neutral">Estável</span>
                </div>
                <p>Padrão consistente de pedidos ao longo da semana, com picos nas terças e quartas.</p>
              </div>
              <div class="trend-item">
                <div class="trend-header">
                  <h5>Urgência</h5>
                  <span class="trend-indicator warning">Atenção</span>
                </div>
                <p>Aumento de 8% em pedidos críticos nas últimas duas semanas.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

// Registrar componentes do Chart.js
Chart.register(...registerables);

export default {
  name: 'DashboardAnalytics',
  components: {
    LoadingIndicator
  },
  emits: ['refresh'],
  props: {
    pedidos: {
      type: Array,
      default: () => []
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    // Refs para os gráficos
    const statusChart = ref(null);
    const categoryChart = ref(null);
    const urgencyChart = ref(null);
    const timelineChart = ref(null);

    // Estado reativo
    const isRefreshing = ref(false);
    const timelineFilter = ref('30');
    const activeDetailTab = ref('performance');

    // Instâncias dos gráficos
    const charts = ref({
      status: null,
      category: null,
      urgency: null,
      timeline: null
    });

    // Configuração das abas de detalhes
    const detailTabs = [
      { id: 'performance', label: 'Performance', icon: 'speed' },
      { id: 'categories', label: 'Categorias', icon: 'category' },
      { id: 'trends', label: 'Tendências', icon: 'trending_up' }
    ];

    // Computed properties para dados dos gráficos
    const statusChartData = computed(() => {
      const statusCount = {
        'Pendente': 0,
        'Concluído': 0,
        'Cancelado': 0
      };
      
      props.pedidos.forEach(pedido => {
        if (pedido.status in statusCount) {
          statusCount[pedido.status]++;
        }
      });
      
      const colors = {
        'Pendente': '#ffa726',
        'Concluído': '#66bb6a',
        'Cancelado': '#78909c'
      };

      return Object.entries(statusCount).map(([label, value]) => ({
        label,
        value,
        color: colors[label]
      }));
    });

    const categoryBreakdown = computed(() => {
      const categoryCount = {};
      
      props.pedidos.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        categoryCount[categoria] = (categoryCount[categoria] || 0) + 1;
      });

      const total = props.pedidos.length;
      
      return Object.entries(categoryCount)
        .map(([name, count]) => ({
          name,
          count,
          percentage: total > 0 ? Math.round((count / total) * 100) : 0
        }))
        .sort((a, b) => b.count - a.count);
    });

    const urgencyStats = computed(() => {
      const urgencyCount = {
        'Padrão': 0,
        'Urgente': 0,
        'Crítico': 0
      };

      props.pedidos.forEach(pedido => {
        const urgencia = pedido.urgencia || 'Padrão';
        if (urgencia in urgencyCount) {
          urgencyCount[urgencia]++;
        }
      });

      return {
        padrao: urgencyCount['Padrão'],
        urgente: urgencyCount['Urgente'],
        critico: urgencyCount['Crítico']
      };
    });

    const topCategory = computed(() => {
      if (categoryBreakdown.value.length === 0) {
        return { name: 'N/A', count: 0, percentage: 0 };
      }
      return categoryBreakdown.value[0];
    });

    const categoriesCount = computed(() => categoryBreakdown.value.length);

    const completionRate = computed(() => {
      const total = props.pedidos.length;
      if (total === 0) return 0;
      
      const completed = props.pedidos.filter(p => p.status === 'Concluído').length;
      return Math.round((completed / total) * 100);
    });

    const completedThisMonth = computed(() => {
      const now = new Date();
      const thisMonth = now.getMonth();
      const thisYear = now.getFullYear();
      
      return props.pedidos.filter(pedido => {
        if (pedido.status !== 'Concluído' || !pedido.conclusao_data) return false;
        
        const conclusaoDate = new Date(pedido.conclusao_data);
        return conclusaoDate.getMonth() === thisMonth && 
               conclusaoDate.getFullYear() === thisYear;
      }).length;
    });

    const tempoMedioConclusao = computed(() => {
      const concluidos = props.pedidos.filter(p => 
        p.status === 'Concluído' && p.deliveryDate && p.conclusao_data
      );
      
      if (concluidos.length === 0) return 'N/A';
      
      let tempoTotal = 0;
      concluidos.forEach(pedido => {
        const dataInicio = new Date(pedido.deliveryDate);
        const dataFim = new Date(pedido.conclusao_data);
        const diffTime = Math.abs(dataFim - dataInicio);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        tempoTotal += diffDays;
      });
      
      const tempoMedio = tempoTotal / concluidos.length;
      return `${tempoMedio.toFixed(1)} dias`;
    });

    const dailyAverage = computed(() => {
      if (props.pedidos.length === 0) return 0;
      
      // Calcular média dos últimos 30 dias
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      
      const recentPedidos = props.pedidos.filter(pedido => {
        const pedidoDate = new Date(pedido.deliveryDate);
        return pedidoDate >= thirtyDaysAgo;
      });
      
      return (recentPedidos.length / 30).toFixed(1);
    });

    const peakActivity = computed(() => {
      // Simular dados de pico de atividade
      return {
        day: 'Terça-feira',
        count: Math.max(...Object.values(statusChartData.value).map(item => item.value))
      };
    });

    const completionEfficiency = computed(() => {
      // Calcular eficiência baseada em pedidos concluídos vs. tempo médio
      const efficiency = Math.min(100, Math.max(0, 100 - (parseFloat(tempoMedioConclusao.value) || 0) * 2));
      return Math.round(efficiency);
    });

    // Métodos para criar gráficos
    const createStatusChart = () => {
      if (!statusChart.value) return;

      const ctx = statusChart.value.getContext('2d');
      
      if (charts.value.status) {
        charts.value.status.destroy();
      }

      charts.value.status = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: statusChartData.value.map(item => item.label),
          datasets: [{
            data: statusChartData.value.map(item => item.value),
            backgroundColor: statusChartData.value.map(item => item.color),
            borderWidth: 2,
            borderColor: '#1a1a1a'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '60%',
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#ff6f61',
              borderWidth: 1
            }
          }
        }
      });
    };

    const createCategoryChart = () => {
      if (!categoryChart.value) return;

      const ctx = categoryChart.value.getContext('2d');
      
      if (charts.value.category) {
        charts.value.category.destroy();
      }

      const topCategories = categoryBreakdown.value.slice(0, 6);

      charts.value.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: topCategories.map(item => item.name),
          datasets: [{
            label: 'Pedidos',
            data: topCategories.map(item => item.count),
            backgroundColor: '#ff6f61',
            borderRadius: 4,
            borderSkipped: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff'
            }
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              },
              ticks: {
                color: '#f5f5f5'
              }
            },
            y: {
              grid: {
                display: false
              },
              ticks: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    };

    const createUrgencyChart = () => {
      if (!urgencyChart.value) return;

      const ctx = urgencyChart.value.getContext('2d');
      
      if (charts.value.urgency) {
        charts.value.urgency.destroy();
      }

      charts.value.urgency = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Padrão', 'Urgente', 'Crítico'],
          datasets: [{
            data: [
              urgencyStats.value.padrao,
              urgencyStats.value.urgente,
              urgencyStats.value.critico
            ],
            backgroundColor: [
              '#66bb6a',
              '#ffa726',
              '#ef5350'
            ],
            borderWidth: 2,
            borderColor: '#1a1a1a'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: '#f5f5f5',
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff'
            }
          }
        }
      });
    };

    const createTimelineChart = () => {
      if (!timelineChart.value) return;

      const ctx = timelineChart.value.getContext('2d');
      
      if (charts.value.timeline) {
        charts.value.timeline.destroy();
      }

      // Simular dados de timeline
      const days = parseInt(timelineFilter.value);
      const labels = [];
      const data = [];

      for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }));
        
        // Simular dados baseados nos pedidos reais
        const dayPedidos = props.pedidos.filter(pedido => {
          const pedidoDate = new Date(pedido.deliveryDate);
          return pedidoDate.toDateString() === date.toDateString();
        }).length;
        
        data.push(dayPedidos);
      }

      charts.value.timeline = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Pedidos',
            data,
            borderColor: '#ff6f61',
            backgroundColor: 'rgba(255, 111, 97, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff'
            }
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              },
              ticks: {
                color: '#f5f5f5'
              }
            },
            y: {
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              },
              ticks: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    };

    const initializeCharts = () => {
      // Aguardar próximo tick para garantir que os elementos estejam renderizados
      setTimeout(() => {
        createStatusChart();
        createCategoryChart();
        createUrgencyChart();
        createTimelineChart();
      }, 100);
    };

    const destroyCharts = () => {
      Object.values(charts.value).forEach(chart => {
        if (chart && typeof chart.destroy === 'function') {
          chart.destroy();
        }
      });
      charts.value = {
        status: null,
        category: null,
        urgency: null,
        timeline: null
      };
    };

    const updateTimelineChart = () => {
      createTimelineChart();
    };

    // Watchers
    watch(() => props.pedidos, () => {
      if (props.pedidos.length > 0) {
        initializeCharts();
      }
    }, { deep: true });

    // Lifecycle
    onMounted(() => {
      if (props.pedidos.length > 0) {
        initializeCharts();
      }
    });

    onUnmounted(() => {
      destroyCharts();
    });

    return {
      // Refs
      statusChart,
      categoryChart,
      urgencyChart,
      timelineChart,
      
      // Estado
      isRefreshing,
      timelineFilter,
      activeDetailTab,
      detailTabs,
      
      // Computed
      statusChartData,
      categoryBreakdown,
      urgencyStats,
      topCategory,
      categoriesCount,
      completionRate,
      completedThisMonth,
      tempoMedioConclusao,
      dailyAverage,
      peakActivity,
      completionEfficiency,
      
      // Methods
      updateTimelineChart
    };
  }
};
</script>

<style scoped>
.analytics-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.analytics-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Section Headers */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid #333;
}

.section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: #f5f5f5;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.section-header h3 i {
  color: #ff6f61;
  font-size: var(--font-size-xl);
}

/* Refresh Button */
.refresh-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: var(--font-size-sm);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
}

.refresh-btn .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.chart-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  border: 1px solid #333;
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.chart-header h4 {
  margin: 0;
  font-size: var(--font-size-md);
  color: #f5f5f5;
  font-weight: 600;
}

.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: var(--font-size-xs);
  color: #aaa;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.chart-info {
  font-size: var(--font-size-xs);
  color: #aaa;
}

.urgency-summary .critical-count {
  color: #ef5350;
  font-weight: 600;
}

.timeline-controls select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
}

.chart-container {
  height: 250px;
  position: relative;
}

.chart-container.timeline {
  height: 300px;
}

/* Insights Grid */
.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
}

.insight-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid #333;
  transition: all 0.3s ease;
}

.insight-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.insight-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6f61, #ff8a80);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.insight-icon.warning {
  background: linear-gradient(135deg, #ffa726, #ffcc02);
}

.insight-icon.success {
  background: linear-gradient(135deg, #66bb6a, #81c784);
}

.insight-icon.info {
  background: linear-gradient(135deg, #42a5f5, #64b5f6);
}

.insight-icon i {
  color: white;
  font-size: var(--font-size-lg);
}

.insight-content {
  flex: 1;
}

.insight-content h4 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #aaa;
  font-weight: 500;
}

.insight-value {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: 0.25rem;
}

.insight-detail {
  font-size: var(--font-size-xs);
  color: #888;
}

/* Detail Tabs */
.details-tabs {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid #333;
}

.detail-tab {
  background: none;
  border: none;
  color: #aaa;
  padding: var(--spacing-sm) var(--spacing-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
  font-size: var(--font-size-sm);
}

.detail-tab:hover {
  color: #f5f5f5;
  background: rgba(255, 255, 255, 0.05);
}

.detail-tab.active {
  color: #ff6f61;
  border-bottom-color: #ff6f61;
}

.detail-tab i {
  font-size: var(--font-size-md);
}

/* Detail Panels */
.detail-panel {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.performance-metrics {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.metric-row:last-child {
  border-bottom: none;
}

.metric-label {
  color: #aaa;
  font-size: var(--font-size-sm);
}

.metric-value {
  color: #f5f5f5;
  font-weight: 600;
  font-size: var(--font-size-sm);
}

.categories-breakdown {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.category-info {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.category-name {
  color: #f5f5f5;
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.category-count {
  color: #aaa;
  font-size: var(--font-size-xs);
}

.category-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.category-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6f61, #ff8a80);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.category-percentage {
  color: #f5f5f5;
  font-size: var(--font-size-sm);
  font-weight: 600;
  min-width: 40px;
  text-align: right;
}

.trends-analysis {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.trend-item {
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.trend-header h5 {
  margin: 0;
  color: #f5f5f5;
  font-size: var(--font-size-md);
}

.trend-indicator {
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.trend-indicator.positive {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.trend-indicator.negative {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.trend-indicator.warning {
  background: rgba(255, 167, 38, 0.2);
  color: #ffa726;
}

.trend-indicator.neutral {
  background: rgba(158, 158, 158, 0.2);
  color: #9e9e9e;
}

.trend-item p {
  margin: 0;
  color: #aaa;
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

/* Responsividade */
@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }

  .insights-grid {
    grid-template-columns: 1fr;
  }

  .chart-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .chart-legend {
    justify-content: center;
  }

  .details-tabs {
    flex-direction: column;
  }

  .detail-tab {
    justify-content: center;
  }

  .metric-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.25rem;
  }

  .category-item {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .category-info {
    min-width: auto;
  }
}
</style> 