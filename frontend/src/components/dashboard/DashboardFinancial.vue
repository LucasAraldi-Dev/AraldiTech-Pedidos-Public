<template>
  <div class="financial-container">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <LoadingIndicator message="Carregando dados financeiros..." size="large" />
    </div>

    <div v-else class="financial-content">
      <!-- Financial KPIs -->
      <div class="kpis-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">account_balance_wallet</i>
            Resumo Financeiro
          </h3>
          <button class="refresh-btn" @click="$emit('refresh')" :disabled="isRefreshing">
            <i class="material-icons" :class="{ 'spinning': isRefreshing }">refresh</i>
            <span>Atualizar</span>
          </button>
        </div>

        <div class="kpis-grid">
          <div class="kpi-card">
            <div class="kpi-icon">
              <i class="material-icons">monetization_on</i>
            </div>
            <div class="kpi-content">
              <h4>Orçamento Total</h4>
              <div class="kpi-value">R$ {{ formatCurrency(orcamentoTotal) }}</div>
              <div class="kpi-trend positive">
                <i class="material-icons">trending_up</i>
                <span>+8% este mês</span>
              </div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon spent">
              <i class="material-icons">shopping_cart</i>
            </div>
            <div class="kpi-content">
              <h4>Custo Real</h4>
              <div class="kpi-value">R$ {{ formatCurrency(custoRealTotal) }}</div>
              <div class="kpi-trend neutral">
                <i class="material-icons">trending_flat</i>
                <span>Estável</span>
              </div>
            </div>
          </div>

          <div class="kpi-card" :class="saldoFinanceiro >= 0 ? 'positive' : 'negative'">
            <div class="kpi-icon" :class="saldoFinanceiro >= 0 ? 'savings' : 'deficit'">
              <i class="material-icons">{{ saldoFinanceiro >= 0 ? 'savings' : 'money_off' }}</i>
            </div>
            <div class="kpi-content">
              <h4>{{ saldoFinanceiro >= 0 ? 'Economia' : 'Déficit' }}</h4>
              <div class="kpi-value">R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}</div>
              <div class="kpi-percentage">{{ economiaPercentual }}% do orçamento</div>
            </div>
          </div>

          <div class="kpi-card">
            <div class="kpi-icon efficiency">
              <i class="material-icons">speed</i>
            </div>
            <div class="kpi-content">
              <h4>Eficiência</h4>
              <div class="kpi-value">{{ eficienciaFinanceira }}%</div>
              <div class="kpi-subtitle">Orçamento vs. Realizado</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Budget vs Actual Chart -->
      <div class="chart-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">bar_chart</i>
            Orçamento vs. Realizado
          </h3>
          <div class="chart-controls">
            <select v-model="chartFilter" @change="updateChart">
              <option value="all">Todos os Pedidos</option>
              <option value="top10">Top 10 Maiores</option>
              <option value="recent">Últimos 30 dias</option>
            </select>
          </div>
        </div>

        <div class="chart-container">
          <canvas ref="budgetChart"></canvas>
        </div>
      </div>

      <!-- Financial Breakdown -->
      <div class="breakdown-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">pie_chart</i>
            Distribuição por Categoria
          </h3>
        </div>

        <div class="breakdown-content">
          <div class="breakdown-chart">
            <canvas ref="categoryChart"></canvas>
          </div>
          
          <div class="breakdown-details">
            <div class="category-list">
              <div 
                v-for="category in categoryFinancials" 
                :key="category.name"
                class="category-item"
              >
                <div class="category-header">
                  <span class="category-name">{{ category.name }}</span>
                  <span class="category-total">R$ {{ formatCurrency(category.total) }}</span>
                </div>
                <div class="category-progress">
                  <div class="progress-bar">
                    <div 
                      class="progress-fill" 
                      :style="{ width: category.percentage + '%' }"
                    ></div>
                  </div>
                  <span class="progress-percentage">{{ category.percentage }}%</span>
                </div>
                <div class="category-stats">
                  <span class="stat-item">
                    <i class="material-icons">receipt</i>
                    {{ category.count }} pedidos
                  </span>
                  <span class="stat-item">
                    <i class="material-icons">calculate</i>
                    Média: R$ {{ formatCurrency(category.average) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financial Alerts -->
      <div class="alerts-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">warning</i>
            Alertas Financeiros
          </h3>
        </div>

        <div class="alerts-grid">
          <div v-for="alert in financialAlerts" :key="alert.id" class="alert-card" :class="alert.type">
            <div class="alert-icon">
              <i class="material-icons">{{ alert.icon }}</i>
            </div>
            <div class="alert-content">
              <h4>{{ alert.title }}</h4>
              <p>{{ alert.message }}</p>
              <div class="alert-value" v-if="alert.value">{{ alert.value }}</div>
            </div>
            <div class="alert-actions">
              <button class="alert-action" @click="handleAlert(alert)">
                <i class="material-icons">arrow_forward</i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly Trends -->
      <div class="trends-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">timeline</i>
            Tendências Mensais
          </h3>
        </div>

        <div class="trends-content">
          <div class="trend-chart">
            <canvas ref="trendsChart"></canvas>
          </div>
          
          <div class="trend-summary">
            <div class="summary-item">
              <div class="summary-icon">
                <i class="material-icons">trending_up</i>
              </div>
              <div class="summary-content">
                <h5>Crescimento Mensal</h5>
                <div class="summary-value positive">+15.2%</div>
                <div class="summary-detail">Comparado ao mês anterior</div>
              </div>
            </div>

            <div class="summary-item">
              <div class="summary-icon">
                <i class="material-icons">savings</i>
              </div>
              <div class="summary-content">
                <h5>Economia Acumulada</h5>
                <div class="summary-value">R$ {{ formatCurrency(economiaAcumulada) }}</div>
                <div class="summary-detail">Nos últimos 6 meses</div>
              </div>
            </div>

            <div class="summary-item">
              <div class="summary-icon">
                <i class="material-icons">calculate</i>
              </div>
              <div class="summary-content">
                <h5>Ticket Médio</h5>
                <div class="summary-value">R$ {{ formatCurrency(ticketMedio) }}</div>
                <div class="summary-detail">Por pedido</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="actions-section">
        <div class="actions-grid">
          <button class="action-btn primary" @click="$emit('view-details')">
            <i class="material-icons">visibility</i>
            <span>Ver Detalhes Completos</span>
          </button>
          
          <button class="action-btn secondary" @click="exportFinancialReport">
            <i class="material-icons">file_download</i>
            <span>Exportar Relatório</span>
          </button>
          
          <button class="action-btn secondary" @click="configureBudget">
            <i class="material-icons">settings</i>
            <span>Configurar Orçamento</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

Chart.register(...registerables);

export default {
  name: 'DashboardFinancial',
  components: {
    LoadingIndicator
  },
  emits: ['refresh', 'view-details'],
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
    // Refs para gráficos
    const budgetChart = ref(null);
    const categoryChart = ref(null);
    const trendsChart = ref(null);

    // Estado reativo
    const isRefreshing = ref(false);
    const chartFilter = ref('all');

    // Instâncias dos gráficos
    const charts = ref({
      budget: null,
      category: null,
      trends: null
    });

    // Computed properties financeiros
    const orcamentoTotal = computed(() => {
      return props.pedidos.reduce((total, pedido) => {
        return total + parseFloat(pedido.orcamento_previsto || 0);
      }, 0);
    });

    const custoRealTotal = computed(() => {
      return props.pedidos.reduce((total, pedido) => {
        return total + parseFloat(pedido.custo_real || 0);
      }, 0);
    });

    const saldoFinanceiro = computed(() => {
      return orcamentoTotal.value - custoRealTotal.value;
    });

    const economiaPercentual = computed(() => {
      if (orcamentoTotal.value === 0) return 0;
      return Math.round((Math.abs(saldoFinanceiro.value) / orcamentoTotal.value) * 100);
    });

    const eficienciaFinanceira = computed(() => {
      if (orcamentoTotal.value === 0) return 0;
      const efficiency = (custoRealTotal.value / orcamentoTotal.value) * 100;
      return Math.round(100 - Math.abs(100 - efficiency));
    });

    const categoryFinancials = computed(() => {
      const categoryData = {};
      
      props.pedidos.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        const orcamento = parseFloat(pedido.orcamento_previsto || 0);
        const custo = parseFloat(pedido.custo_real || 0);
        
        if (!categoryData[categoria]) {
          categoryData[categoria] = {
            name: categoria,
            total: 0,
            count: 0,
            orcamento: 0,
            custo: 0
          };
        }
        
        categoryData[categoria].total += orcamento;
        categoryData[categoria].orcamento += orcamento;
        categoryData[categoria].custo += custo;
        categoryData[categoria].count++;
      });

      const total = orcamentoTotal.value;
      
      return Object.values(categoryData)
        .map(category => ({
          ...category,
          percentage: total > 0 ? Math.round((category.total / total) * 100) : 0,
          average: category.count > 0 ? category.total / category.count : 0
        }))
        .sort((a, b) => b.total - a.total);
    });

    const ticketMedio = computed(() => {
      if (props.pedidos.length === 0) return 0;
      return orcamentoTotal.value / props.pedidos.length;
    });

    const economiaAcumulada = computed(() => {
      // Simular economia acumulada dos últimos 6 meses
      return saldoFinanceiro.value * 1.5;
    });

    const financialAlerts = computed(() => {
      const alerts = [];
      
      // Alert para déficit
      if (saldoFinanceiro.value < 0) {
        alerts.push({
          id: 'deficit',
          type: 'danger',
          icon: 'warning',
          title: 'Déficit Orçamentário',
          message: 'Os custos reais estão excedendo o orçamento previsto.',
          value: `R$ ${formatCurrency(Math.abs(saldoFinanceiro.value))}`
        });
      }

      // Alert para pedidos sem orçamento
      const semOrcamento = props.pedidos.filter(p => !p.orcamento_previsto || parseFloat(p.orcamento_previsto) === 0);
      if (semOrcamento.length > 0) {
        alerts.push({
          id: 'no-budget',
          type: 'warning',
          icon: 'info',
          title: 'Pedidos sem Orçamento',
          message: `${semOrcamento.length} pedidos não possuem orçamento definido.`,
          value: null
        });
      }

      // Alert para alta variação
      const altaVariacao = props.pedidos.filter(p => {
        const orcamento = parseFloat(p.orcamento_previsto || 0);
        const custo = parseFloat(p.custo_real || 0);
        return orcamento > 0 && Math.abs(custo - orcamento) / orcamento > 0.2;
      });

      if (altaVariacao.length > 0) {
        alerts.push({
          id: 'high-variance',
          type: 'info',
          icon: 'trending_up',
          title: 'Alta Variação',
          message: `${altaVariacao.length} pedidos com variação >20% entre orçado e realizado.`,
          value: null
        });
      }

      return alerts;
    });

    // Métodos
    const formatCurrency = (value) => {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    const createBudgetChart = () => {
      if (!budgetChart.value) return;

      const ctx = budgetChart.value.getContext('2d');
      
      if (charts.value.budget) {
        charts.value.budget.destroy();
      }

      let filteredPedidos = [...props.pedidos];
      
      // Aplicar filtro
      switch (chartFilter.value) {
        case 'top10':
          filteredPedidos = filteredPedidos
            .sort((a, b) => parseFloat(b.orcamento_previsto || 0) - parseFloat(a.orcamento_previsto || 0))
            .slice(0, 10);
          break;
        case 'recent': {
          const thirtyDaysAgo = new Date();
          thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
          filteredPedidos = filteredPedidos.filter(p => {
            const pedidoDate = new Date(p.deliveryDate);
            return pedidoDate >= thirtyDaysAgo;
          });
          break;
        }
      }

      const labels = filteredPedidos.map(p => `#${p.id}`);
      const orcamentos = filteredPedidos.map(p => parseFloat(p.orcamento_previsto || 0));
      const custos = filteredPedidos.map(p => parseFloat(p.custo_real || 0));

      charts.value.budget = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Orçamento',
              data: orcamentos,
              backgroundColor: '#4DB6AC',
              borderRadius: 4,
              borderSkipped: false
            },
            {
              label: 'Custo Real',
              data: custos,
              backgroundColor: '#FF6F61',
              borderRadius: 4,
              borderSkipped: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#f5f5f5',
                font: { size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: R$ ${formatCurrency(context.raw)}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#f5f5f5' }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: {
                color: '#f5f5f5',
                callback: function(value) {
                  return `R$ ${formatCurrency(value)}`;
                }
              }
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

      const topCategories = categoryFinancials.value.slice(0, 6);

      charts.value.category = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: topCategories.map(c => c.name),
          datasets: [{
            data: topCategories.map(c => c.total),
            backgroundColor: [
              '#FF6F61', '#4DB6AC', '#FFA726', 
              '#42A5F5', '#AB47BC', '#66BB6A'
            ],
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
              callbacks: {
                label: function(context) {
                  return `${context.label}: R$ ${formatCurrency(context.raw)}`;
                }
              }
            }
          }
        }
      });
    };

    const createTrendsChart = () => {
      if (!trendsChart.value) return;

      const ctx = trendsChart.value.getContext('2d');
      
      if (charts.value.trends) {
        charts.value.trends.destroy();
      }

      // Simular dados de tendência mensal
      const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'];
      const orcamentoData = [85000, 92000, 88000, 95000, 102000, 98000];
      const custoData = [82000, 89000, 91000, 93000, 97000, 95000];

      charts.value.trends = new Chart(ctx, {
        type: 'line',
        data: {
          labels: months,
          datasets: [
            {
              label: 'Orçamento',
              data: orcamentoData,
              borderColor: '#4DB6AC',
              backgroundColor: 'rgba(77, 182, 172, 0.1)',
              borderWidth: 2,
              fill: false,
              tension: 0.4
            },
            {
              label: 'Custo Real',
              data: custoData,
              borderColor: '#FF6F61',
              backgroundColor: 'rgba(255, 111, 97, 0.1)',
              borderWidth: 2,
              fill: false,
              tension: 0.4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#f5f5f5',
                font: { size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff'
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#f5f5f5' }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: {
                color: '#f5f5f5',
                callback: function(value) {
                  return `R$ ${(value / 1000).toFixed(0)}k`;
                }
              }
            }
          }
        }
      });
    };

    const initializeCharts = () => {
      setTimeout(() => {
        createBudgetChart();
        createCategoryChart();
        createTrendsChart();
      }, 100);
    };

    const destroyCharts = () => {
      Object.values(charts.value).forEach(chart => {
        if (chart && typeof chart.destroy === 'function') {
          chart.destroy();
        }
      });
      charts.value = { budget: null, category: null, trends: null };
    };

    const updateChart = () => {
      createBudgetChart();
    };

    const handleAlert = (alert) => {
      console.log('Handling alert:', alert);
      // Implementar ação específica para cada tipo de alerta
    };

    const exportFinancialReport = () => {
      console.log('Exportando relatório financeiro');
      // Implementar exportação
    };

    const configureBudget = () => {
      console.log('Configurando orçamento');
      // Implementar configuração de orçamento
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
      budgetChart,
      categoryChart,
      trendsChart,
      
      // Estado
      isRefreshing,
      chartFilter,
      
      // Computed
      orcamentoTotal,
      custoRealTotal,
      saldoFinanceiro,
      economiaPercentual,
      eficienciaFinanceira,
      categoryFinancials,
      ticketMedio,
      economiaAcumulada,
      financialAlerts,
      
      // Methods
      formatCurrency,
      updateChart,
      handleAlert,
      exportFinancialReport,
      configureBudget
    };
  }
};
</script>

<style scoped>
.financial-container {
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

.financial-content {
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

/* KPIs Grid */
.kpis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
}

.kpi-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid #333;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #4DB6AC, #66BB6A);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.kpi-card.positive::before {
  background: linear-gradient(90deg, #66BB6A, #81C784);
}

.kpi-card.negative::before {
  background: linear-gradient(90deg, #EF5350, #E57373);
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.kpi-card:hover::before {
  opacity: 1;
}

.kpi-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4DB6AC, #66BB6A);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-icon.spent {
  background: linear-gradient(135deg, #FF6F61, #FF8A80);
}

.kpi-icon.savings {
  background: linear-gradient(135deg, #66BB6A, #81C784);
}

.kpi-icon.deficit {
  background: linear-gradient(135deg, #EF5350, #E57373);
}

.kpi-icon.efficiency {
  background: linear-gradient(135deg, #42A5F5, #64B5F6);
}

.kpi-icon i {
  color: white;
  font-size: var(--font-size-xl);
}

.kpi-content {
  flex: 1;
}

.kpi-content h4 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #aaa;
  font-weight: 500;
}

.kpi-value {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: var(--spacing-xs);
}

.kpi-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: var(--font-size-xs);
}

.kpi-trend.positive {
  color: #4caf50;
}

.kpi-trend.negative {
  color: #f44336;
}

.kpi-trend.neutral {
  color: #9e9e9e;
}

.kpi-percentage, .kpi-subtitle {
  font-size: var(--font-size-xs);
  color: #888;
}

/* Chart Controls */
.chart-controls select {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Breakdown Section */
.breakdown-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  align-items: start;
}

.breakdown-chart {
  height: 300px;
  position: relative;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.category-item {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.category-name {
  font-size: var(--font-size-sm);
  color: #f5f5f5;
  font-weight: 500;
}

.category-total {
  font-size: var(--font-size-sm);
  color: #ff6f61;
  font-weight: 600;
}

.category-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #ff6f61, #ff8a80);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-percentage {
  font-size: var(--font-size-xs);
  color: #f5f5f5;
  font-weight: 600;
  min-width: 35px;
  text-align: right;
}

.category-stats {
  display: flex;
  gap: var(--spacing-md);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: var(--font-size-xs);
  color: #aaa;
}

.stat-item i {
  font-size: var(--font-size-sm);
}

/* Alerts Grid */
.alerts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.alert-card {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.alert-card.danger {
  border-color: rgba(239, 83, 80, 0.3);
  background: rgba(239, 83, 80, 0.05);
}

.alert-card.warning {
  border-color: rgba(255, 167, 38, 0.3);
  background: rgba(255, 167, 38, 0.05);
}

.alert-card.info {
  border-color: rgba(66, 165, 245, 0.3);
  background: rgba(66, 165, 245, 0.05);
}

.alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.alert-card.danger .alert-icon {
  background: rgba(239, 83, 80, 0.2);
  color: #ef5350;
}

.alert-card.warning .alert-icon {
  background: rgba(255, 167, 38, 0.2);
  color: #ffa726;
}

.alert-card.info .alert-icon {
  background: rgba(66, 165, 245, 0.2);
  color: #42a5f5;
}

.alert-content {
  flex: 1;
}

.alert-content h4 {
  margin: 0 0 0.25rem 0;
  font-size: var(--font-size-sm);
  color: #f5f5f5;
  font-weight: 600;
}

.alert-content p {
  margin: 0 0 0.25rem 0;
  font-size: var(--font-size-xs);
  color: #aaa;
  line-height: 1.4;
}

.alert-value {
  font-size: var(--font-size-sm);
  color: #ff6f61;
  font-weight: 600;
}

.alert-actions {
  flex-shrink: 0;
}

.alert-action {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #f5f5f5;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.alert-action:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Trends Section */
.trends-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-lg);
  align-items: start;
}

.trend-chart {
  height: 250px;
  position: relative;
}

.trend-summary {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.summary-item {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 111, 97, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.summary-icon i {
  color: #ff6f61;
  font-size: var(--font-size-md);
}

.summary-content h5 {
  margin: 0 0 0.25rem 0;
  font-size: var(--font-size-sm);
  color: #aaa;
  font-weight: 500;
}

.summary-value {
  font-size: var(--font-size-md);
  color: #f5f5f5;
  font-weight: 600;
  margin-bottom: 0.125rem;
}

.summary-value.positive {
  color: #4caf50;
}

.summary-detail {
  font-size: var(--font-size-xs);
  color: #888;
}

/* Actions Section */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.action-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: var(--font-size-sm);
  font-weight: 500;
  border: none;
}

.action-btn.primary {
  background: linear-gradient(135deg, #ff6f61, #ff8a80);
  color: white;
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #e74c3c, #ff6f61);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 111, 97, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* Responsividade */
@media (max-width: 768px) {
  .kpis-grid {
    grid-template-columns: 1fr;
  }

  .breakdown-content {
    grid-template-columns: 1fr;
  }

  .trends-content {
    grid-template-columns: 1fr;
  }

  .alerts-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .kpi-card {
    padding: var(--spacing-md);
  }

  .kpi-icon {
    width: 48px;
    height: 48px;
  }
}
</style>