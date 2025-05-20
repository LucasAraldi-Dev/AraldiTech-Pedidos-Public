<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="dashboard-title">Dashboard de Gestão</h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="material-icons">close</i>
        </button>
      </div>
      
      <div class="dashboard-container">
        <!-- Indicador de cache e carregamento -->
        <div v-if="dataFromCache" class="cache-indicator">
          <i class="material-icons">cached</i>
          Dados carregados do cache
        </div>
        
        <div v-if="isLoading" class="dashboard-loading">
          <LoadingIndicator message="Carregando dados do dashboard..." size="large" />
        </div>
        
        <div v-else class="dashboard-sections">
          <!-- KPIs - Cards com métricas principais -->
          <div class="dashboard-section kpi-section">
            <div class="section-header">
              <h3><i class="material-icons section-icon">insights</i>Métricas Principais</h3>
              <div class="section-actions">
                <button class="refresh-btn" @click="fetchData(true)">
                  <i class="material-icons">refresh</i>
                  Atualizar
                </button>
              </div>
            </div>
            
            <div class="dashboard-metrics">
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="material-icons">shopping_cart</i>
                </div>
                <div class="metric-content">
                  <h4 class="metric-title">Total de Pedidos</h4>
                  <div class="metric-value">{{ totalPedidos }}</div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="material-icons">pending_actions</i>
                </div>
                <div class="metric-content">
                  <h4 class="metric-title">Pedidos Pendentes</h4>
                  <div class="metric-value">{{ pedidosPendentes }}</div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="material-icons">timer</i>
                </div>
                <div class="metric-content">
                  <h4 class="metric-title">Tempo Médio</h4>
                  <div class="metric-value">{{ tempoMedioConclusao }}</div>
                </div>
              </div>
              
              <div class="metric-card">
                <div class="metric-icon">
                  <i class="material-icons">account_balance_wallet</i>
                </div>
                <div class="metric-content">
                  <h4 class="metric-title">Orçamento Total</h4>
                  <div class="metric-value">R$ {{ formatCurrency(orcamentoTotal) }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Gráficos e visualizações -->
          <div class="dashboard-section charts-section">
            <div class="section-header">
              <h3><i class="material-icons section-icon">bar_chart</i>Análise de Pedidos</h3>
            </div>
            
            <div v-if="isLoadingCharts" class="charts-loading">
              <LoadingIndicator message="Carregando gráficos..." />
            </div>
            
            <div v-else class="charts-container">
              <div class="chart-wrapper">
                <h4 class="chart-title">Status dos Pedidos</h4>
                <canvas id="statusChart" ref="statusChart"></canvas>
              </div>
              
              <div class="chart-wrapper">
                <h4 class="chart-title">Categorias</h4>
                <canvas id="categoryChart" ref="categoryChart"></canvas>
              </div>
              
              <div class="chart-wrapper">
                <h4 class="chart-title">Urgência</h4>
                <canvas id="urgencyChart" ref="urgencyChart"></canvas>
              </div>
              
              <div class="chart-wrapper">
                <h4 class="chart-title">Orçamento vs. Custo Real</h4>
                <canvas id="budgetChart" ref="budgetChart"></canvas>
              </div>
            </div>
          </div>
          
          <!-- Seção Financeira -->
          <div class="dashboard-section financial-section">
            <div class="section-header">
              <h3><i class="material-icons section-icon">account_balance</i>Resumo Financeiro</h3>
            </div>
            
            <div class="financial-overview">
              <div class="financial-kpis">
                <div class="financial-kpi">
                  <i class="material-icons kpi-icon">monetization_on</i>
                  <div class="kpi-content">
                    <h4>Orçamento Total</h4>
                    <div class="kpi-value">R$ {{ formatCurrency(orcamentoTotal) }}</div>
                  </div>
                </div>
                
                <div class="financial-kpi">
                  <i class="material-icons kpi-icon">shopping_cart</i>
                  <div class="kpi-content">
                    <h4>Custo Real</h4>
                    <div class="kpi-value">R$ {{ formatCurrency(custoRealTotal) }}</div>
                  </div>
                </div>
                
                <div class="financial-kpi" :class="saldoFinanceiro >= 0 ? 'positive-balance' : 'negative-balance'">
                  <i class="material-icons kpi-icon">{{ saldoFinanceiro >= 0 ? 'savings' : 'money_off' }}</i>
                  <div class="kpi-content">
                    <h4>{{ saldoFinanceiro >= 0 ? 'Economia' : 'Déficit' }}</h4>
                    <div class="kpi-value">R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}</div>
                  </div>
                </div>
              </div>
              
              <div class="financial-summary-actions">
                <button class="btn-view-details" @click="viewFinancialDetails">
                  <i class="material-icons">visibility</i>
                  Ver detalhes financeiros
                </button>
              </div>
            </div>
          </div>
          
          <!-- Relatórios -->
          <div class="dashboard-section reports-section">
            <div class="section-header">
              <h3><i class="material-icons section-icon">description</i>Relatórios</h3>
            </div>
            
            <div class="reports-container">
              <div class="report-form">
                <div class="report-form-group">
                  <label for="reportType">Tipo de Relatório:</label>
                  <select id="reportType" v-model="reportOptions.tipo" class="report-select">
                    <option value="pedidos">Pedidos</option>
                    <option value="atividades">Atividades</option>
                  </select>
                </div>
                
                <div class="report-form-group">
                  <label for="reportPeriod">Período:</label>
                  <select id="reportPeriod" v-model="reportOptions.periodo" class="report-select">
                    <option value="diario">Diário</option>
                    <option value="semanal">Semanal</option>
                    <option value="mensal">Mensal</option>
                    <option value="personalizado">Personalizado</option>
                  </select>
                </div>
                
                <div class="report-date-range" v-if="reportOptions.periodo === 'personalizado'">
                  <div class="report-form-group">
                    <label for="startDate">Data Inicial:</label>
                    <input type="date" id="startDate" v-model="reportOptions.dataInicial" class="date-input">
                  </div>
                  <div class="report-form-group">
                    <label for="endDate">Data Final:</label>
                    <input type="date" id="endDate" v-model="reportOptions.dataFinal" class="date-input">
                  </div>
                </div>
                
                <div class="report-form-group">
                  <label for="reportFormat">Formato:</label>
                  <select id="reportFormat" v-model="reportOptions.formato" class="report-select">
                    <option value="pdf">PDF</option>
                    <option value="excel">Excel</option>
                    <option value="csv">CSV</option>
                  </select>
                </div>
                
                <div class="report-actions">
                  <button 
                    class="btn-generate" 
                    @click="generateReport" 
                    :disabled="isDownloadingReport"
                  >
                    <i class="material-icons">file_download</i>
                    {{ isDownloadingReport ? 'Gerando...' : 'Gerar Relatório' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Atividades Recentes -->
          <div class="dashboard-section activities-section">
            <div class="section-header">
              <h3><i class="material-icons section-icon">history</i>Atividades Recentes</h3>
            </div>
            
            <div class="activities-container">
              <div v-if="activities.length === 0" class="empty-state">
                <i class="material-icons empty-icon">info</i>
                <p class="empty-message">Nenhuma atividade recente encontrada</p>
              </div>
              
              <div v-else class="activity-list">
                <div v-for="(activity, index) in activities.slice(0, 5)" :key="index" class="activity-item">
                  <div class="activity-icon">
                    <i class="material-icons">{{ getActivityIcon(activity.tipo) }}</i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-details">{{ activity.descricao }}</div>
                    <div class="activity-time">{{ formatDateTime(activity.data_hora) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Modal para detalhes financeiros -->
  <ModalFinanceiro
    v-if="showFinancialDetails"
    :isOpen="showFinancialDetails"
    @close="closeFinancialDetails"
  />
</template>

<script>
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';
import authService from '@/api/authService';
import { cachedRequest } from '@/utils/cacheService';
import ModalFinanceiro from '@/components/ModalFinanceiro.vue';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';
import { useToast } from 'vue-toastification';

// Registrar todos os componentes
Chart.register(...registerables);

export default {
  name: 'ModalDashboard',
  components: {
    ModalFinanceiro,
    LoadingIndicator
  },
  emits: ['close', 'open-order'],
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isLoading: true,
      isDownloadingReport: false,
      isLoadingCharts: false,
      dataFromCache: false,
      activities: [],
      pedidos: [],
      charts: {
        status: null,
        category: null,
        urgency: null,
        budget: null
      },
      cacheOptions: {
        dashboard: {
          enabled: true,
          ttl: 5 * 60 * 1000 // 5 minutos para dados do dashboard
        },
        activities: {
          enabled: true,
          ttl: 2 * 60 * 1000 // 2 minutos para atividades
        }
      },
      totalPedidos: 0,
      tempoMedioConclusao: '0 dias',
      pedidosPendentes: 0,
      // Dados financeiros
      orcamentoTotal: 0,
      custoRealTotal: 0,
      saldoFinanceiro: 0,
      reportOptions: {
        tipo: 'pedidos',
        periodo: 'mensal',
        dataInicial: this.getDefaultStartDate(),
        dataFinal: this.formatDateForInput(new Date()),
        formato: 'pdf'
      },
      showFinancialDetails: false
    };
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.fetchData();
      }
    }
  },
  mounted() {
    if (this.isOpen) {
      this.fetchData();
    }
  },
  methods: {
    // Método principal para buscar dados
    async fetchData(forceRefresh = false) {
      this.isLoading = true;
      
      try {
        // Buscar pedidos
        await this.fetchPedidos(forceRefresh);
        
        // Buscar atividades recentes
        await this.fetchActivities(forceRefresh);
        
        // Inicializar gráficos depois de obter os dados
        this.initCharts();
      } catch (error) {
        console.error("Erro ao carregar dados do dashboard:", error);
        const toast = useToast();
        toast.error("Erro ao carregar dados. Tente novamente mais tarde.");
      } finally {
        this.isLoading = false;
      }
    },
    
    // Buscar pedidos do backend com suporte a cache
    async fetchPedidos(forceRefresh = false) {
      this.dataFromCache = false;
      
      try {
        // Usar cachedRequest para buscar pedidos com cache
        const cacheKey = 'dashboard_pedidos';
        const { data, fromCache: cached } = await cachedRequest({
          key: cacheKey,
          ttl: this.cacheOptions.dashboard.ttl,
          forceRefresh,
          request: async () => {
            const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
              headers: authService.getAuthHeaders()
            });
            return response.data;
          }
        });
        
        this.pedidos = data || [];
        this.dataFromCache = cached;
        
        // Calcular métricas
        this.calcularMetricas();
      } catch (error) {
        console.error("Erro ao buscar pedidos:", error);
        throw error;
      }
    },
    
    // Buscar atividades recentes
    async fetchActivities(forceRefresh = false) {
      try {
        // Usar cachedRequest para buscar atividades com cache
        const cacheKey = 'dashboard_activities';
        const { data, fromCache: cached } = await cachedRequest({
          key: cacheKey,
          ttl: this.cacheOptions.activities.ttl,
          forceRefresh,
          request: async () => {
            const response = await axios.get(`${process.env.VUE_APP_API_URL}/atividades`, {
              headers: authService.getAuthHeaders()
            });
            return response.data;
          }
        });
        
        this.activities = data || [];
        this.dataFromCache = this.dataFromCache || cached;
      } catch (error) {
        console.error("Erro ao buscar atividades:", error);
        // Não lançamos o erro aqui para que o dashboard ainda funcione sem atividades
        this.activities = [];
      }
    },
    
    // Calcular métricas com base nos pedidos
    calcularMetricas() {
      // Calcular total de pedidos
      this.totalPedidos = this.pedidos.length;
      
      // Calcular pedidos pendentes
      this.pedidosPendentes = this.pedidos.filter(p => p.status === 'Pendente').length;
      
      // Calcular tempo médio de conclusão
      const pedidosConcluidos = this.pedidos.filter(p => p.status === 'Concluído');
      if (pedidosConcluidos.length > 0) {
        let tempoTotal = 0;
        
        pedidosConcluidos.forEach(pedido => {
          const dataInicio = new Date(pedido.data_pedido);
          const dataFim = new Date(pedido.data_conclusao);
          const diffTime = Math.abs(dataFim - dataInicio);
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          tempoTotal += diffDays;
        });
        
        const tempoMedio = tempoTotal / pedidosConcluidos.length;
        this.tempoMedioConclusao = `${tempoMedio.toFixed(1)} dias`;
      } else {
        this.tempoMedioConclusao = 'N/A';
      }
      
      // Calcular dados financeiros
      let orcamento = 0;
      let custo = 0;
      
      this.pedidos.forEach(pedido => {
        orcamento += parseFloat(pedido.orcamento_previsto || 0);
        custo += parseFloat(pedido.custo_real || 0);
      });
      
      this.orcamentoTotal = orcamento;
      this.custoRealTotal = custo;
      this.saldoFinanceiro = orcamento - custo;
    },
    
    // Inicializar gráficos
    async initCharts() {
      this.isLoadingCharts = true;
      
      try {
        // Destruir gráficos existentes para evitar duplicação
        this.destroyCharts();
        
        // Criar novos gráficos
        await this.createStatusChart();
        await this.createCategoryChart();
        await this.createUrgencyChart();
        await this.createBudgetChart();
      } catch (error) {
        console.error("Erro ao inicializar gráficos:", error);
      } finally {
        this.isLoadingCharts = false;
      }
    },
    
    // Destruir gráficos existentes
    destroyCharts() {
      Object.keys(this.charts).forEach(chartKey => {
        if (this.charts[chartKey] instanceof Chart) {
          this.charts[chartKey].destroy();
          this.charts[chartKey] = null;
        }
      });
    },
    
    // Criar gráfico de status
    async createStatusChart() {
      if (!this.$refs.statusChart) return;
      
      const statusCount = {
        Pendente: 0,
        'Em Andamento': 0,
        Concluído: 0,
        Cancelado: 0
      };
      
      this.pedidos.forEach(pedido => {
        if (Object.prototype.hasOwnProperty.call(statusCount, pedido.status)) {
          statusCount[pedido.status]++;
        }
      });
      
      const ctx = this.$refs.statusChart.getContext('2d');
      this.charts.status = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: Object.keys(statusCount),
          datasets: [{
            data: Object.values(statusCount),
            backgroundColor: [
              '#FF6F61', // Vermelho/Coral para Pendente
              '#FFA726', // Laranja para Em Andamento
              '#66BB6A', // Verde para Concluído
              '#78909C'  // Cinza para Cancelado
            ],
            borderWidth: 1
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
              backgroundColor: 'rgba(0, 0, 0, 0.7)'
            }
          }
        }
      });
    },
    
    // Criar gráfico de categorias
    async createCategoryChart() {
      if (!this.$refs.categoryChart) return;
      
      const categoryCount = {};
      
      this.pedidos.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        if (!categoryCount[categoria]) {
          categoryCount[categoria] = 0;
        }
        categoryCount[categoria]++;
      });
      
      // Ordenar por contagem
      const sortedCategories = Object.entries(categoryCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 7); // Limitar a 7 categorias
      
      const ctx = this.$refs.categoryChart.getContext('2d');
      this.charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: sortedCategories.map(item => item[0]),
          datasets: [{
            label: 'Quantidade',
            data: sortedCategories.map(item => item[1]),
            backgroundColor: '#FF6F61',
            borderWidth: 0,
            borderRadius: 4
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
              backgroundColor: 'rgba(0, 0, 0, 0.7)'
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
    },
    
    // Criar gráfico de urgência
    async createUrgencyChart() {
      if (!this.$refs.urgencyChart) return;
      
      const urgencyCount = {
        'Baixa': 0,
        'Média': 0,
        'Alta': 0,
        'Crítica': 0
      };
      
      this.pedidos.forEach(pedido => {
        const urgencia = pedido.urgencia || 'Média';
        if (Object.prototype.hasOwnProperty.call(urgencyCount, urgencia)) {
          urgencyCount[urgencia]++;
        }
      });
      
      const ctx = this.$refs.urgencyChart.getContext('2d');
      this.charts.urgency = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: Object.keys(urgencyCount),
          datasets: [{
            data: Object.values(urgencyCount),
            backgroundColor: [
              '#66BB6A', // Verde para Baixa
              '#FFA726', // Laranja para Média
              '#FF7043', // Laranja mais escuro para Alta
              '#EF5350'  // Vermelho para Crítica
            ],
            borderWidth: 2,
            borderColor: '#2a2a2a'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '70%',
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
              backgroundColor: 'rgba(0, 0, 0, 0.7)'
            }
          }
        }
      });
    },
    
    // Criar gráfico de orçamento vs custo real
    async createBudgetChart() {
      if (!this.$refs.budgetChart) return;
      
      // Filtrar pedidos que têm dados financeiros
      const pedidosFinanceiros = this.pedidos
        .filter(p => (parseFloat(p.orcamento_previsto || 0) > 0) || (parseFloat(p.custo_real || 0) > 0))
        .sort((a, b) => parseFloat(b.orcamento_previsto || 0) - parseFloat(a.orcamento_previsto || 0))
        .slice(0, 6); // Limitando aos 6 maiores para melhor visualização
      
      const ctx = this.$refs.budgetChart.getContext('2d');
      this.charts.budget = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: pedidosFinanceiros.map(p => `#${p.id}`),
          datasets: [
            {
              label: 'Orçamento',
              data: pedidosFinanceiros.map(p => parseFloat(p.orcamento_previsto || 0)),
              backgroundColor: '#4DB6AC',
              borderWidth: 0,
              borderRadius: 4
            },
            {
              label: 'Custo Real',
              data: pedidosFinanceiros.map(p => parseFloat(p.custo_real || 0)),
              backgroundColor: '#FF6F61',
              borderWidth: 0,
              borderRadius: 4
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
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              callbacks: {
                label: function(context) {
                  return `${context.dataset.label}: R$ ${context.raw.toFixed(2)}`;
                }
              }
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
                color: '#f5f5f5',
                callback: function(value) {
                  return `R$ ${value}`;
                }
              }
            }
          }
        }
      });
    },
    
    // Método para gerar relatório
    async generateReport() {
      if (this.isDownloadingReport) return;
      this.isDownloadingReport = true;
      
      try {
        const toast = useToast();
        
        // Verificar datas para período personalizado
        if (this.reportOptions.periodo === 'personalizado') {
          const dataInicial = new Date(this.reportOptions.dataInicial);
          const dataFinal = new Date(this.reportOptions.dataFinal);
          
          if (isNaN(dataInicial.getTime()) || isNaN(dataFinal.getTime())) {
            toast.error('Por favor, selecione datas válidas para o relatório.');
            return;
          }
          
          if (dataFinal < dataInicial) {
            toast.error('A data final não pode ser anterior à data inicial.');
            return;
          }
        }
        
        // Fazer solicitação para gerar o relatório
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/relatorios`,
          {
            tipo: this.reportOptions.tipo,
            periodo: this.reportOptions.periodo,
            data_inicial: this.reportOptions.dataInicial,
            data_final: this.reportOptions.dataFinal,
            formato: this.reportOptions.formato
          },
          {
            headers: authService.getAuthHeaders(),
            responseType: 'blob'
          }
        );
        
        // Criar URL para download
        const blob = new Blob([response.data], { 
          type: this.getMimeType(this.reportOptions.formato) 
        });
        const url = window.URL.createObjectURL(blob);
        
        // Criar link para download e clicar nele automaticamente
        const link = document.createElement('a');
        link.href = url;
        link.download = this.getReportFileName();
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        toast.success('Relatório gerado com sucesso!');
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        const toast = useToast();
        toast.error('Erro ao gerar relatório. Tente novamente mais tarde.');
      } finally {
        this.isDownloadingReport = false;
      }
    },
    
    // Obter nome do arquivo para o relatório
    getReportFileName() {
      const date = new Date();
      const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
      return `relatorio-${this.reportOptions.tipo}-${formattedDate}.${this.getFileExtension(this.reportOptions.formato)}`;
    },
    
    // Obter extensão de arquivo com base no formato
    getFileExtension(formato) {
      switch (formato) {
        case 'excel': return 'xlsx';
        case 'csv': return 'csv';
        case 'pdf':
        default: return 'pdf';
      }
    },
    
    // Obter MIME type com base no formato
    getMimeType(formato) {
      switch (formato) {
        case 'excel': return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
        case 'csv': return 'text/csv';
        case 'pdf':
        default: return 'application/pdf';
      }
    },
    
    // Formatar data para campo de input
    formatDateForInput(date) {
      if (!date) return '';
      
      const d = new Date(date);
      return d.toISOString().split('T')[0];
    },
    
    // Obter data padrão para início (30 dias atrás)
    getDefaultStartDate() {
      const date = new Date();
      date.setDate(date.getDate() - 30);
      return this.formatDateForInput(date);
    },
    
    // Formatar valor monetário
    formatCurrency(value) {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    
    // Formatar data e hora
    formatDateTime(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      
      // Verificar se a data é válida
      if (isNaN(date.getTime())) return dateString;
      
      return new Intl.DateTimeFormat('pt-BR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    
    // Obter ícone para tipo de atividade
    getActivityIcon(tipo) {
      switch (tipo) {
        case 'criar': return 'add_circle';
        case 'editar': return 'edit';
        case 'concluir': return 'check_circle';
        case 'cancelar': return 'cancel';
        case 'financeiro': return 'attach_money';
        case 'comentario': return 'comment';
        default: return 'info';
      }
    },
    
    // Abrir detalhes financeiros
    viewFinancialDetails() {
      this.showFinancialDetails = true;
    },
    
    // Fechar detalhes financeiros
    closeFinancialDetails() {
      this.showFinancialDetails = false;
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Overlay e Modal Base */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-index-modal);
  padding: var(--spacing-md);
  overflow-y: auto;
}

.modal-content {
  background-color: #1f1f1f;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 0.3125rem 1.5625rem rgba(0, 0, 0, 0.5);
  width: var(--modal-width-md);
  max-width: var(--modal-max-width);
  max-height: var(--modal-max-height);
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  color: #f5f5f5;
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
}

.modal-content::-webkit-scrollbar {
  width: 0.5rem;
}

.modal-content::-webkit-scrollbar-track {
  background: #333;
  border-radius: 0.625rem;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 0.625rem;
}

/* Cabeçalho do Modal */
.modal-header {
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 0.0625rem solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: #1f1f1f;
  z-index: 10;
  border-top-left-radius: var(--border-radius-lg);
  border-top-right-radius: var(--border-radius-lg);
}

.dashboard-title {
  font-size: var(--font-size-xl);
  margin: 0;
  color: #f5f5f5;
  display: flex;
  align-items: center;
}

.dashboard-title::before {
  content: 'dashboard';
  font-family: 'Material Icons';
  margin-right: var(--spacing-sm);
  color: #ff6f61;
  font-size: var(--font-size-xxl);
}

.close-btn {
  background: none;
  border: none;
  color: #ff6f61;
  font-size: var(--font-size-xl);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #e74c3c;
}

/* Container principal */
.dashboard-container {
  padding: var(--spacing-md);
}

/* Indicador de Cache */
.cache-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(102, 204, 255, 0.1);
  color: #66ccff;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-sm);
}

.cache-indicator i {
  margin-right: var(--spacing-xs);
  font-size: var(--font-size-md);
}

/* Loading */
.dashboard-loading, .charts-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 18.75rem;
  width: 100%;
}

/* Seções */
.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.dashboard-section {
  background-color: #252525;
  border-radius: var(--border-radius-md);
  box-shadow: 0 0.3125rem 0.9375rem rgba(0, 0, 0, 0.2);
  padding: var(--spacing-md);
  border: 0.0625rem solid #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 0.0625rem solid #333;
}

.section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: #f5f5f5;
  display: flex;
  align-items: center;
}

.section-icon {
  color: #ff6f61;
  margin-right: var(--spacing-xs);
  font-size: var(--font-size-xl);
}

.section-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.refresh-btn {
  background-color: transparent;
  color: #f5f5f5;
  border: 0.0625rem solid #444;
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all 0.3s;
  font-size: var(--font-size-sm);
}

.refresh-btn:hover {
  background-color: rgba(255, 255, 255, 0.05);
  border-color: #555;
}

.refresh-btn i {
  font-size: var(--font-size-md);
}

/* Métricas (KPIs) */
.dashboard-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
}

.metric-card {
  background-color: #2a2a2a;
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  border: 0.0625rem solid #333;
}

.metric-card:hover {
  transform: translateY(-0.3125rem);
  box-shadow: 0 0.5rem 0.9375rem rgba(0, 0, 0, 0.2);
  border-color: #ff6f61;
}

.metric-icon {
  font-size: var(--font-size-xxl);
  margin-right: var(--spacing-sm);
  color: #ff6f61;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-content {
  flex: 1;
}

.metric-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #ddd;
  font-weight: 500;
}

.metric-value {
  font-size: var(--font-size-lg);
  font-weight: bold;
  color: #f5f5f5;
}

/* Gráficos */
.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.chart-wrapper {
  background-color: #2a2a2a;
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.1);
  height: 15.625rem;
  position: relative;
  border: 0.0625rem solid #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.chart-wrapper:hover {
  transform: translateY(-0.1875rem);
  box-shadow: 0 0.5rem 0.9375rem rgba(0, 0, 0, 0.2);
  border-color: #444;
}

.chart-title {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
  color: #ddd;
  text-align: center;
  font-weight: 500;
}

canvas {
  width: 100% !important;
  height: calc(100% - 2.5rem) !important;
}

/* Seção Financeira */
.financial-overview {
  margin-bottom: var(--spacing-md);
}

.financial-kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.financial-kpi {
  background-color: #2a2a2a;
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  border: 0.0625rem solid #333;
}

.financial-kpi:hover {
  transform: translateY(-0.3125rem);
  box-shadow: 0 0.5rem 0.9375rem rgba(0, 0, 0, 0.2);
  border-color: #ff6f61;
}

.kpi-icon {
  font-size: var(--font-size-xxl);
  margin-right: var(--spacing-sm);
  color: #ff6f61;
}

.kpi-content {
  flex: 1;
}

.financial-kpi h4 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #ddd;
  font-weight: 500;
}

.kpi-value {
  font-size: var(--font-size-lg);
  font-weight: bold;
  color: #f5f5f5;
}

.positive-balance .kpi-value {
  color: #2ecc71;
}

.negative-balance .kpi-value {
  color: #e74c3c;
}

.financial-summary-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-view-details {
  background-color: #555555;
  color: #f5f5f5;
  border: none;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.3s;
  font-size: var(--font-size-sm);
}

.btn-view-details:hover {
  background-color: #666666;
  transform: translateY(-0.125rem);
}

/* Relatórios */
.reports-container {
  display: flex;
  flex-direction: column;
}

.report-form {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.report-form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.report-form-group label {
  font-size: var(--font-size-sm);
  color: #ddd;
}

.report-select, .date-input {
  padding: var(--spacing-xs);
  background-color: #333;
  border: 0.0625rem solid #444;
  border-radius: var(--border-radius-sm);
  color: #f5f5f5;
  font-size: var(--font-size-sm);
  height: 2.5rem;
}

.report-date-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
  grid-column: span 2;
}

.report-actions {
  display: flex;
  justify-content: flex-end;
  grid-column: span 3;
}

.btn-generate {
  background-color: #ff6f61;
  color: #f5f5f5;
  border: none;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.3s;
  font-size: var(--font-size-sm);
  font-weight: 500;
  min-width: 10rem;
  min-height: 2.5rem;
  justify-content: center;
}

.btn-generate:hover {
  background-color: #e74c3c;
  transform: translateY(-0.125rem);
}

.btn-generate:disabled {
  background-color: #555;
  cursor: not-allowed;
  transform: none;
}

/* Atividades Recentes */
.activities-container {
  margin-top: var(--spacing-sm);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: var(--spacing-sm);
  background-color: #2a2a2a;
  border-radius: var(--border-radius-sm);
  border: 0.0625rem solid #333;
  transition: all 0.3s;
}

.activity-item:hover {
  background-color: #303030;
  border-color: #444;
  transform: translateX(0.1875rem);
}

.activity-icon {
  color: #ff6f61;
  margin-right: var(--spacing-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-content {
  flex: 1;
}

.activity-details {
  font-size: var(--font-size-sm);
  margin-bottom: 0.3125rem;
  color: #f5f5f5;
}

.activity-time {
  font-size: var(--font-size-xs);
  color: #aaa;
}

/* Estado vazio */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: #777;
  text-align: center;
}

.empty-icon {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-sm);
  color: #555;
}

.empty-message {
  font-size: var(--font-size-sm);
  margin: 0;
}

/* Responsividade */
@media (max-width: 1280px) {
  .dashboard-metrics {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-wrapper {
    height: 18.75rem;
  }
  
  .report-form {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .report-actions {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .modal-overlay {
    align-items: flex-start;
    padding: var(--spacing-sm);
  }
  
  .modal-content {
    width: 100%;
    max-height: 95vh;
    margin-top: var(--spacing-sm);
  }
  
  .dashboard-title {
    font-size: var(--font-size-lg);
  }
  
  .dashboard-metrics {
    grid-template-columns: 1fr;
  }
  
  .financial-kpis {
    grid-template-columns: 1fr;
  }
  
  .report-form {
    grid-template-columns: 1fr;
  }
  
  .report-date-range {
    grid-template-columns: 1fr;
    grid-column: span 1;
  }
  
  .report-actions {
    grid-column: span 1;
  }
  
  .btn-generate {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .modal-header {
    padding: var(--spacing-sm);
  }
  
  .dashboard-container {
    padding: var(--spacing-sm);
  }
  
  .dashboard-section {
    padding: var(--spacing-sm);
  }
  
  .section-header h3 {
    font-size: var(--font-size-md);
  }
  
  .chart-wrapper {
    height: 15.625rem;
  }
  
  .metric-card, .financial-kpi, .activity-item {
    padding: var(--spacing-sm);
  }
  
  .metric-value, .kpi-value {
    font-size: var(--font-size-md);
  }
}

/* Ajustes para telas pequenas */
@media screen and (max-height: 700px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: var(--spacing-sm);
  }
  
  .modal-content {
    max-height: 95vh;
  }
  
  .chart-wrapper {
    height: 12.5rem;
  }
}
</style> 