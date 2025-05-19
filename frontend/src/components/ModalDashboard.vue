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
        <div class="dashboard-sections">
          <!-- Gráficos e estatísticas de Pedidos (agora no topo) -->
          <div class="dashboard-section full-width">
            <h2><i class="material-icons section-icon">insights</i>Estatísticas de Pedidos</h2>
            <div class="statistics-container">
              <div v-if="isLoadingCharts" class="loading-charts">
                <LoadingIndicator message="Carregando estatísticas..." />
              </div>
              <template v-else>
                <div class="statistics-row">
                  <!-- KPIs -->
                  <div class="kpi-card">
                    <i class="material-icons kpi-icon">assignment</i>
                    <h3>Total de Pedidos</h3>
                    <div class="kpi-value">{{ totalPedidos }}</div>
                  </div>
                  <div class="kpi-card">
                    <i class="material-icons kpi-icon">timer</i>
                    <h3>Tempo Médio de Conclusão</h3>
                    <div class="kpi-value">{{ tempoMedioConclusao }}</div>
                  </div>
                  <div class="kpi-card">
                    <i class="material-icons kpi-icon">pending_actions</i>
                    <h3>Pedidos Pendentes</h3>
                    <div class="kpi-value">{{ pedidosPendentes }}</div>
                  </div>
                </div>
                
                <!-- Gráficos -->
                <div class="charts-container">
                  <div class="chart-wrapper">
                    <h3>Pedidos por Status</h3>
                    <canvas ref="statusChart"></canvas>
                  </div>
                  <div class="chart-wrapper">
                    <h3>Pedidos por Categoria</h3>
                    <canvas ref="categoryChart"></canvas>
                  </div>
                  <div class="chart-wrapper">
                    <h3>Pedidos por Urgência</h3>
                    <canvas ref="urgencyChart"></canvas>
                  </div>
                </div>
              </template>
            </div>
          </div>
          
          <!-- Feed de atividades recentes -->
          <div class="dashboard-section">
            <h2><i class="material-icons section-icon">history</i>Atividades Recentes</h2>
            <div class="activity-feed">
              <div v-if="isLoading" class="loading">
                <LoadingIndicator message="Carregando atividades..." />
              </div>
              <div v-else-if="activities.length === 0" class="empty-feed">
                <i class="material-icons">info</i>
                Nenhuma atividade recente encontrada.
              </div>
              <div v-else class="activity-list">
                <div class="cache-indicator" v-if="dataFromCache">
                  <i class="material-icons">cached</i>
                  Dados carregados do cache
                </div>
                <div v-for="activity in activities" :key="activity.id" class="activity-item">
                  <div class="activity-icon" :class="getActivityIcon(activity.tipo)">
                    <i :class="getActivityIconClass(activity.tipo)"></i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-header">
                      <span class="activity-user">{{ activity.usuario_nome }}</span>
                      <span class="activity-date">{{ formatDate(activity.data) }}</span>
                    </div>
                    <div class="activity-description">{{ activity.descricao }}</div>
                    <div v-if="activity.pedido_id" class="activity-details">
                      <a @click="openOrderDetails(activity.pedido_id)">Ver detalhes do pedido #{{ activity.pedido_id }}</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Geração de Relatórios -->
          <div class="dashboard-section">
            <h2><i class="material-icons section-icon">description</i>Relatórios</h2>
            <div class="reports-container">
              <div class="report-options">
                <div class="form-group">
                  <label for="reportType">Tipo de Relatório:</label>
                  <select id="reportType" v-model="reportOptions.tipo">
                    <option value="pedidos">Pedidos</option>
                    <option value="atividades">Atividades</option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label for="reportPeriod">Período:</label>
                  <select id="reportPeriod" v-model="reportOptions.periodo">
                    <option value="diario">Diário</option>
                    <option value="semanal">Semanal</option>
                    <option value="mensal">Mensal</option>
                    <option value="personalizado">Personalizado</option>
                  </select>
                </div>
                
                <div class="form-group date-range" v-if="reportOptions.periodo === 'personalizado'">
                  <div>
                    <label for="startDate">Data Inicial:</label>
                    <input type="date" id="startDate" v-model="reportOptions.dataInicial">
                  </div>
                  <div>
                    <label for="endDate">Data Final:</label>
                    <input type="date" id="endDate" v-model="reportOptions.dataFinal">
                  </div>
                </div>
                
                <div class="form-group">
                  <label for="reportFormat">Formato:</label>
                  <select id="reportFormat" v-model="reportOptions.formato">
                    <option value="pdf">PDF</option>
                    <option value="excel">Excel</option>
                  </select>
                </div>
              </div>
              
              <div class="report-actions">
                <button class="btn-generate" @click="generateReport" :disabled="isDownloadingReport">
                  <LoadingIndicator v-if="isDownloadingReport" size="small" />
                  <span v-else>Gerar Relatório</span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Componente de Resumo Financeiro (agora no final) -->
          <div class="dashboard-section">
            <h2><i class="material-icons section-icon">account_balance</i>Resumo Financeiro</h2>
            <div class="financial-summary-compact">
              <div class="financial-kpis">
                <div class="financial-kpi">
                  <i class="material-icons kpi-icon">monetization_on</i>
                  <div class="kpi-content">
                    <h3>Orçamento Total</h3>
                    <div class="kpi-value">R$ {{ formatCurrency(orcamentoTotal) }}</div>
                  </div>
                </div>
                
                <div class="financial-kpi">
                  <i class="material-icons kpi-icon">shopping_cart</i>
                  <div class="kpi-content">
                    <h3>Custo Real Total</h3>
                    <div class="kpi-value">R$ {{ formatCurrency(custoRealTotal) }}</div>
                  </div>
                </div>
                
                <div class="financial-kpi" :class="saldoClass">
                  <i class="material-icons kpi-icon">{{ saldoFinanceiro >= 0 ? 'savings' : 'money_off' }}</i>
                  <div class="kpi-content">
                    <h3>{{ saldoFinanceiro >= 0 ? 'Economia' : 'Déficit' }}</h3>
                    <div class="kpi-value">R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}</div>
                  </div>
                </div>
              </div>
              
              <!-- Gráfico de orçamento vs custo real -->
              <div class="chart-wrapper full-width">
                <h3>Orçamento vs Custo Real</h3>
                <canvas id="budgetChart"></canvas>
              </div>
              
              <div class="financial-summary-actions">
                <button class="btn-view-details" @click="viewFinancialDetails">
                  <i class="material-icons">visibility</i>
                  Ver detalhes financeiros
                </button>
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
      </div>
    </div>
  </div>
</template>

<script>
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';
import authService from '@/api/authService';
import axiosService from '@/api/axiosService';
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
    async fetchData() {
      this.isLoading = true;
      this.dataFromCache = false;
      
      try {
        // Carregar dados das atividades usando o cacheService
        const activityResponse = await cachedRequest(
          axiosService.get,
          '/atividades',
          { params: { limit: 10 } },  // Limitar a 10 atividades recentes
          this.cacheOptions.activities
        );
        
        // Marcar se os dados vieram do cache
        if (activityResponse.cached) {
          this.dataFromCache = true;
          console.log('Dados de atividades carregados do cache');
        }
        
        this.activities = activityResponse.data;
        
        // Carregar dados dos pedidos
        this.isLoadingCharts = true;
        const pedidosResponse = await cachedRequest(
          axiosService.get,
          '/pedidos',
          {},
          this.cacheOptions.dashboard
        );
        
        if (pedidosResponse.cached) {
          this.dataFromCache = true;
          console.log('Dados de pedidos carregados do cache');
        }
        
        this.pedidos = pedidosResponse.data;
        
        // Calcular métricas
        this.calculateMetrics();
        
        // Renderizar gráficos
        this.$nextTick(() => {
          this.renderCharts();
        });
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        const toast = useToast();
        toast.error('Erro ao carregar dados do dashboard. Tente novamente.');
      } finally {
        this.isLoading = false;
        this.isLoadingCharts = false;
      }
    },
    
    calculateMetrics() {
      // Total de pedidos
      this.totalPedidos = this.pedidos.length;
      
      // Pedidos pendentes
      this.pedidosPendentes = this.pedidos.filter(p => 
        p.status !== 'Concluído' && p.status !== 'Cancelado'
      ).length;
      
      // Tempo médio de conclusão
      const pedidosConcluidos = this.pedidos.filter(p => p.status === 'Concluído');
      if (pedidosConcluidos.length > 0) {
        const tempoTotal = pedidosConcluidos.reduce((acc, p) => {
          const criacao = new Date(p.data_criacao || p.deliveryDate);
          const conclusao = new Date(p.data_atualizacao || new Date());
          return acc + (conclusao - criacao) / (1000 * 60 * 60 * 24); // Converter para dias
        }, 0);
        const mediaEmDias = Math.round(tempoTotal / pedidosConcluidos.length);
        this.tempoMedioConclusao = `${mediaEmDias} dias`;
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
    
    renderCharts() {
      this.renderStatusChart();
      this.renderCategoryChart();
      this.renderUrgencyChart();
      this.renderBudgetChart();
    },
    
    renderStatusChart() {
      const ctx = this.$refs.statusChart.getContext('2d');
      
      // Contar pedidos por status
      const statusCount = {};
      this.pedidos.forEach(p => {
        statusCount[p.status] = (statusCount[p.status] || 0) + 1;
      });
      
      // Cores para cada status
      const statusColors = {
        'Aguardando Aprovação': '#f39c12',
        'Em Andamento': '#3498db',
        'Concluído': '#2ecc71',
        'Cancelado': '#e74c3c',
        'Em Espera': '#9b59b6'
      };
      
      if (this.charts.status) {
        this.charts.status.destroy();
      }
      
      this.charts.status = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: Object.keys(statusCount),
          datasets: [{
            data: Object.values(statusCount),
            backgroundColor: Object.keys(statusCount).map(status => statusColors[status] || '#95a5a6')
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    },
    
    renderCategoryChart() {
      const ctx = this.$refs.categoryChart.getContext('2d');
      
      // Contar pedidos por categoria
      const categoryCount = {};
      this.pedidos.forEach(p => {
        categoryCount[p.categoria] = (categoryCount[p.categoria] || 0) + 1;
      });
      
      if (this.charts.category) {
        this.charts.category.destroy();
      }
      
      this.charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(categoryCount),
          datasets: [{
            label: 'Pedidos por Categoria',
            data: Object.values(categoryCount),
            backgroundColor: '#ff6f61'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: '#f5f5f5'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: '#f5f5f5'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    },
    
    renderUrgencyChart() {
      const ctx = this.$refs.urgencyChart.getContext('2d');
      
      // Contar pedidos por urgência
      const urgencyCount = {};
      this.pedidos.forEach(p => {
        urgencyCount[p.urgencia] = (urgencyCount[p.urgencia] || 0) + 1;
      });
      
      // Cores para cada nível de urgência
      const urgencyColors = {
        'Padrão': '#3498db',
        'Urgente': '#f39c12',
        'Crítico': '#e74c3c'
      };
      
      if (this.charts.urgency) {
        this.charts.urgency.destroy();
      }
      
      this.charts.urgency = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: Object.keys(urgencyCount),
          datasets: [{
            data: Object.values(urgencyCount),
            backgroundColor: Object.keys(urgencyCount).map(urgency => urgencyColors[urgency] || '#95a5a6')
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    },
    
    renderBudgetChart() {
      // Verificar se o elemento do gráfico existe no DOM
      const chartElement = this.$el.querySelector('#budgetChart');
      if (!chartElement) return;
      
      const ctx = chartElement.getContext('2d');
      
      // Filtrar apenas pedidos com dados financeiros
      const pedidosComOrcamento = this.pedidos.filter(p => 
        (p.orcamento_previsto && p.orcamento_previsto > 0) || 
        (p.custo_real && p.custo_real > 0)
      ).slice(0, 8); // Limitar aos 8 principais para melhor visualização
      
      // Ordenar por orçamento previsto (decrescente)
      pedidosComOrcamento.sort((a, b) => 
        (parseFloat(b.orcamento_previsto || 0) - parseFloat(a.orcamento_previsto || 0))
      );
      
      // Preparar dados para o gráfico
      const labels = pedidosComOrcamento.map(p => `#${p.id}`);
      const orcamentoData = pedidosComOrcamento.map(p => parseFloat(p.orcamento_previsto || 0));
      const custoData = pedidosComOrcamento.map(p => parseFloat(p.custo_real || 0));
      
      if (this.charts.budget) {
        this.charts.budget.destroy();
      }
      
      // Criar o gráfico
      this.charts.budget = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Orçamento Previsto',
              data: orcamentoData,
              backgroundColor: 'rgba(54, 162, 235, 0.6)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: 'Custo Real',
              data: custoData,
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: '#f5f5f5',
                callback: function(value) {
                  return 'R$ ' + value.toLocaleString('pt-BR');
                }
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: '#f5f5f5'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: '#f5f5f5'
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) {
                    label += ': ';
                  }
                  if (context.parsed.y !== null) {
                    label += 'R$ ' + context.parsed.y.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2
                    });
                  }
                  return label;
                }
              }
            }
          }
        }
      });
    },
    
    generateReport() {
      // Implementação da geração de relatório
      console.log('Gerando relatório com as seguintes opções:', this.reportOptions);
      
      this.isDownloadingReport = true;
      
      let url = '';
      const params = new URLSearchParams();
      
      // Adicionar parâmetros comuns
      params.append('periodo', this.reportOptions.periodo);
      params.append('formato', this.reportOptions.formato);
      
      // Adicionar datas se for um período personalizado
      if (this.reportOptions.periodo === 'personalizado') {
        params.append('dataInicial', this.reportOptions.dataInicial);
        params.append('dataFinal', this.reportOptions.dataFinal);
      }
      
      try {
        // Construir a URL baseada no tipo de relatório
        if (this.reportOptions.tipo === 'financeiro') {
          url = `${process.env.VUE_APP_API_URL}/relatorios/financeiro?${params.toString()}`;
        } else {
          url = `${process.env.VUE_APP_API_URL}/relatorios?tipo=${this.reportOptions.tipo}&${params.toString()}`;
        }
        
        // Obter token de autenticação usando authService
        const authToken = authService.getToken();
        if (!authToken) {
          throw new Error('Usuário não autenticado');
        }

        // Método 1: Realizar o download usando Axios com cabeçalhos de autenticação
        axios({
          url: url,
          method: 'GET',
          responseType: 'blob', // importante para receber arquivos
          headers: authService.getAuthHeaders()
        })
        .then(response => {
          // Criar URL para o blob
          const blob = new Blob([response.data], { 
            type: this.reportOptions.formato === 'pdf' ? 'application/pdf' : 'application/vnd.ms-excel' 
          });
          const fileURL = window.URL.createObjectURL(blob);
          
          // Criar link e simular clique para download
          const fileLink = document.createElement('a');
          fileLink.href = fileURL;
          const filename = `relatorio_${this.reportOptions.tipo}_${new Date().toISOString().substring(0, 10)}.${this.reportOptions.formato}`;
          fileLink.setAttribute('download', filename);
          document.body.appendChild(fileLink);
          fileLink.click();
          document.body.removeChild(fileLink);
        })
        .catch(error => {
          console.error('Erro ao baixar relatório:', error);
          alert(`Erro ao baixar relatório: ${error.message || 'Erro desconhecido'}`);
        })
        .finally(() => {
          this.isDownloadingReport = false;
        });
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        alert(`Erro ao gerar relatório: ${error.message}`);
        this.isDownloadingReport = false;
      }
    },
    
    openOrderDetails(pedidoId) {
      console.log(`ModalDashboard: Emitindo evento open-order com pedidoId: ${pedidoId}`);
      
      // Não fechamos mais o modal para que ele possa ser reaberto quando o pedido for fechado
      // this.$emit('close');
      
      // Emitir evento para abrir o modal de impressão do pedido
      this.$emit('open-order', pedidoId);
    },
    
    async fetchOrderById(pedidoId) {
      try {
        // Método mantido para compatibilidade, mas não utilizado diretamente
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos/${pedidoId}`, {
          headers: authService.getAuthHeaders()
        });
        if (response.data) {
          // Emitir evento para abrir o modal de impressão do pedido
          this.$emit('open-order', pedidoId);
        }
      } catch (error) {
        console.error(`Erro ao buscar detalhes do pedido #${pedidoId}:`, error);
        alert('Não foi possível carregar os detalhes do pedido.');
      }
    },
    
    getActivityIcon(tipo) {
      const icons = {
        'criacao': 'create-icon',
        'atualizacao': 'update-icon',
        'aprovacao': 'approve-icon',
        'cancelamento': 'cancel-icon',
        'conclusao': 'complete-icon'
      };
      
      return icons[tipo] || 'default-icon';
    },
    
    getActivityIconClass(tipo) {
      const iconClasses = {
        'criacao': 'material-icons add_circle',
        'atualizacao': 'material-icons update',
        'aprovacao': 'material-icons check_circle',
        'cancelamento': 'material-icons cancel',
        'conclusao': 'material-icons task_alt'
      };
      
      return iconClasses[tipo] || 'material-icons info';
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    
    getDefaultStartDate() {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      return this.formatDateForInput(date);
    },
    
    formatDateForInput(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    
    formatCurrency(value) {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    
    viewFinancialDetails() {
      this.showFinancialDetails = true;
    },
    
    closeFinancialDetails() {
      this.showFinancialDetails = false;
    }
  },
  computed: {
    saldoClass() {
      return this.saldoFinanceiro >= 0 ? 'positive-balance' : 'negative-balance';
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-index-modal);
  overflow-y: auto;
  padding: var(--spacing-md);
  box-sizing: border-box;
}

.modal-content {
  background-color: #1f1f1f;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.5);
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
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #333;
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 10px;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: #1f1f1f;
  z-index: 10;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.close-btn {
  background: none;
  border: none;
  color: #ff6f61;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #e74c3c;
}

.dashboard-container {
  padding: 20px;
}

.dashboard-title {
  font-size: 28px;
  margin: 0;
  color: #f5f5f5;
  display: flex;
  align-items: center;
}

.dashboard-title::before {
  content: 'dashboard';
  font-family: 'Material Icons';
  margin-right: 15px;
  color: #ff6f61;
  font-size: 32px;
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.dashboard-section {
  background-color: #252525;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 20px;
  border: 1px solid #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.dashboard-section h2 {
  font-size: 22px;
  margin-top: 0;
  margin-bottom: 20px;
  color: #ff6f61;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
  display: flex;
  align-items: center;
}

.section-icon {
  margin-right: 10px;
  font-size: 24px;
}

.full-width {
  grid-column: 1 / -1;
}

/* KPI Cards */
.statistics-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-card {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  border: 1px solid #333;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.kpi-card:hover {
  transform: translateY(-5px);
}

.kpi-icon {
  font-size: 36px;
  color: #ff6f61;
  margin-bottom: 10px;
}

.kpi-card h3 {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 10px;
  color: #f5f5f5;
}

.kpi-value {
  font-size: 28px;
  font-weight: bold;
  color: #ff6f61;
}

/* Charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.chart-wrapper {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  height: 300px;
  position: relative;
  border: 1px solid #333;
}

.chart-wrapper.full-width {
  grid-column: 1 / -1;
  height: 350px;
}

.chart-wrapper h3 {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 15px;
  color: #f5f5f5;
  text-align: center;
}

canvas {
  width: 100% !important;
  height: calc(100% - 40px) !important;
}

/* Activity Feed */
.activity-feed {
  background-color: #2a2a2a;
  border-radius: 8px;
  border: 1px solid #333;
  overflow: hidden;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
}

.activity-list::-webkit-scrollbar {
  width: 6px;
}

.activity-list::-webkit-scrollbar-track {
  background: #333;
}

.activity-list::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 3px;
}

.activity-item {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #333;
  transition: background-color 0.3s;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background-color: #303030;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  flex-shrink: 0;
}

.create-icon {
  background-color: #2ecc71;
}

.update-icon {
  background-color: #3498db;
}

.approve-icon {
  background-color: #9b59b6;
}

.cancel-icon {
  background-color: #e74c3c;
}

.complete-icon {
  background-color: #f39c12;
}

.default-icon {
  background-color: #95a5a6;
}

.activity-icon i {
  color: #fff;
  font-size: 20px;
}

.activity-content {
  flex: 1;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.activity-user {
  font-weight: bold;
  color: #ff6f61;
}

.activity-date {
  color: #888;
  font-size: 0.9em;
}

.activity-description {
  margin-bottom: 5px;
  line-height: 1.4;
}

.activity-details a {
  color: #3498db;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9em;
}

.activity-details a:hover {
  text-decoration: underline;
}

.empty-feed {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #888;
}

.empty-feed i {
  margin-right: 10px;
  color: #ff6f61;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #888;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 111, 97, 0.3);
  border-radius: 50%;
  border-top-color: #ff6f61;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Report Section */
.reports-container {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #333;
}

.report-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #f5f5f5;
}

.form-group select,
.form-group input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #2f2f2f;
  color: #f5f5f5;
  font-size: 14px;
}

.date-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.report-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-generate {
  background-color: #555555;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
}

.btn-generate:hover {
  background-color: #666666;
}

.btn-generate::before {
  content: 'description';
  font-family: 'Material Icons';
  margin-right: 10px;
}

.btn-generate:disabled {
  background-color: #888;
  cursor: not-allowed;
}

.loading-spinner-small {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

/* Resumo Financeiro Compacto */
.financial-summary-compact {
  background-color: #252525;
  border-radius: 8px;
  padding: 15px;
}

.financial-kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.financial-kpi {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #333;
}

.financial-kpi:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  border-color: #ff6f61;
}

.kpi-icon {
  font-size: 30px;
  margin-right: 12px;
  color: #ff6f61;
}

.kpi-content {
  flex: 1;
}

.financial-kpi h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #ddd;
}

.kpi-value {
  font-size: 20px;
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
  margin-top: 15px;
}

.btn-view-details {
  background-color: #555555;
  color: #f5f5f5;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-view-details:hover {
  background-color: #666666;
  transform: translateY(-2px);
}

/* Responsividade */
@media (max-width: 1280px) {
  .dashboard-container {
    width: var(--modal-width-md);
    max-width: var(--modal-max-width);
  }
  
  .dashboard-header h2 {
    font-size: var(--font-size-xl);
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding: var(--spacing-md);
  }
  
  .dashboard-header {
    padding: var(--spacing-md);
  }
  
  .dashboard-header h2 {
    font-size: var(--font-size-lg);
  }
  
  .dashboard-content {
    padding: var(--spacing-md);
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .metric-card {
    padding: var(--spacing-md);
  }
  
  .period-selector {
    flex-direction: column;
    align-items: stretch;
  }
  
  .period-buttons {
    margin-top: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding: var(--spacing-sm);
  }
  
  .dashboard-header {
    padding: var(--spacing-sm);
  }
  
  .dashboard-header h2 {
    font-size: var(--font-size-md);
  }
  
  .dashboard-content {
    padding: var(--spacing-sm);
  }
  
  .chart-container, .metric-card {
    padding: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
  }
  
  .metric-value {
    font-size: var(--font-size-xl);
  }
  
  .metric-change {
    font-size: var(--font-size-xs);
  }
}

/* Ajustes específicos para notebooks com zoom */
@media screen and (min-resolution: 1.25dppx) {
  .dashboard-container {
    max-height: var(--modal-max-height);
  }
  
  .dashboard-content {
    padding: var(--spacing-md);
  }
}

/* Ajustes para telas 720p */
@media (min-height: 720px) and (max-height: 768px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: 2vh;
  }
  
  .dashboard-container {
    max-height: 85vh;
  }
}

/* Ajustes para monitores pequenos de 14 polegadas */
@media screen and (max-width: 1366px) and (max-height: 768px) {
  .dashboard-container {
    width: var(--modal-width-md);
    padding: var(--spacing-md);
  }
  
  .metrics-grid {
    gap: var(--spacing-sm);
  }
}

.cache-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(102, 204, 255, 0.1);
  color: #66ccff;
  padding: 5px 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.cache-indicator i {
  margin-right: 5px;
  font-size: 18px;
}

.loading-charts {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  width: 100%;
}

.btn-generate {
  min-width: 160px;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style> 