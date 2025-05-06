<template>
  <div class="dashboard-container">
    <h1 class="dashboard-title">Dashboard de Gestão</h1>
    
    <div class="dashboard-sections">
      <!-- Feed de atividades recentes -->
      <div class="dashboard-section">
        <h2>Atividades Recentes</h2>
        <div class="activity-feed">
          <div v-if="isLoading" class="loading">Carregando atividades...</div>
          <div v-else-if="activities.length === 0" class="empty-feed">
            Nenhuma atividade recente encontrada.
          </div>
          <div v-else class="activity-list">
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
      
      <!-- Gráficos e estatísticas -->
      <div class="dashboard-section">
        <h2>Estatísticas de Pedidos</h2>
        <div class="statistics-container">
          <div class="statistics-row">
            <!-- KPIs -->
            <div class="kpi-card">
              <h3>Total de Pedidos</h3>
              <div class="kpi-value">{{ totalPedidos }}</div>
            </div>
            <div class="kpi-card">
              <h3>Tempo Médio de Conclusão</h3>
              <div class="kpi-value">{{ tempoMedioConclusao }}</div>
            </div>
            <div class="kpi-card">
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
        </div>
      </div>
      
      <!-- Geração de Relatórios -->
      <div class="dashboard-section">
        <h2>Relatórios</h2>
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
            <button class="btn-generate" @click="generateReport">Gerar Relatório</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal para detalhes do pedido -->
    <ModalDetalhePedido
      v-if="showOrderDetails"
      :isOpen="showOrderDetails"
      :pedido="selectedOrder"
      @close="closeOrderDetails"
    />
  </div>
</template>

<script>
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';
import authService from '@/api/authService';
import ModalDetalhePedido from '@/components/ModalDetalhePedido.vue';

// Registrar todos os componentes
Chart.register(...registerables);

export default {
  name: 'AppDashboard',
  components: {
    ModalDetalhePedido
  },
  data() {
    return {
      isLoading: true,
      activities: [],
      pedidos: [],
      charts: {
        status: null,
        category: null,
        urgency: null
      },
      totalPedidos: 0,
      tempoMedioConclusao: '0 dias',
      pedidosPendentes: 0,
      reportOptions: {
        tipo: 'pedidos',
        periodo: 'mensal',
        dataInicial: this.getDefaultStartDate(),
        dataFinal: this.formatDateForInput(new Date()),
        formato: 'pdf'
      },
      showOrderDetails: false,
      selectedOrder: null
    };
  },
  created() {
    // Verificar se o usuário é gestor
    const user = authService.getUser();
    if (!user || user.tipo_usuario !== 'gestor' && user.tipo_usuario !== 'admin') {
      this.$router.push({ name: 'Menu' });
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.isLoading = true;
      try {
        // Carrega pedidos
        await this.fetchPedidos();
        
        // Carrega atividades recentes
        await this.fetchActivities();
        
        // Calcula estatísticas
        this.calculateStatistics();
        
        // Inicializa gráficos
        this.initCharts();
        
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchPedidos() {
      try {
        const response = await axios.get('/pedidos/', {
          headers: authService.getAuthHeaders()
        });
        this.pedidos = response.data;
        this.totalPedidos = this.pedidos.length;
        this.pedidosPendentes = this.pedidos.filter(p => p.status === 'Pendente').length;
      } catch (error) {
        console.error('Erro ao carregar pedidos:', error);
      }
    },
    
    async fetchActivities() {
      try {
        const response = await axios.get('/atividades/', {
          headers: authService.getAuthHeaders()
        });
        this.activities = response.data;
      } catch (error) {
        console.error('Erro ao carregar atividades:', error);
      }
    },
    
    calculateStatistics() {
      // Calcula tempo médio de conclusão
      const pedidosConcluidos = this.pedidos.filter(p => p.status === 'Concluído');
      if (pedidosConcluidos.length > 0) {
        let totalDias = 0;
        pedidosConcluidos.forEach(pedido => {
          const dataCriacao = new Date(pedido.criacao_data || pedido.deliveryDate);
          const dataConclusao = new Date(pedido.conclusao_data || new Date());
          const diffTime = Math.abs(dataConclusao - dataCriacao);
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          totalDias += diffDays;
        });
        const mediaDias = totalDias / pedidosConcluidos.length;
        this.tempoMedioConclusao = `${mediaDias.toFixed(1)} dias`;
      }
    },
    
    initCharts() {
      // Inicializa gráficos após o DOM estar pronto
      this.$nextTick(() => {
        this.initStatusChart();
        this.initCategoryChart();
        this.initUrgencyChart();
      });
    },
    
    initStatusChart() {
      const ctx = this.$refs.statusChart.getContext('2d');
      
      // Contagem de pedidos por status
      const statusCounts = {};
      this.pedidos.forEach(pedido => {
        const status = pedido.status || 'Não definido';
        statusCounts[status] = (statusCounts[status] || 0) + 1;
      });
      
      // Cores para cada status
      const statusColors = {
        'Pendente': '#FFD700',
        'Em Andamento': '#1E90FF',
        'Concluído': '#32CD32',
        'Cancelado': '#FF6347',
        'Não definido': '#A9A9A9'
      };
      
      // Prepara dados para o gráfico
      const labels = Object.keys(statusCounts);
      const data = Object.values(statusCounts);
      const colors = labels.map(label => statusColors[label] || '#A9A9A9');
      
      // Cria o gráfico
      this.charts.status = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      });
    },
    
    initCategoryChart() {
      const ctx = this.$refs.categoryChart.getContext('2d');
      
      // Contagem de pedidos por categoria
      const categoryCounts = {};
      this.pedidos.forEach(pedido => {
        const categoria = pedido.categoria || 'Não categorizado';
        categoryCounts[categoria] = (categoryCounts[categoria] || 0) + 1;
      });
      
      // Prepara dados para o gráfico
      const labels = Object.keys(categoryCounts);
      const data = Object.values(categoryCounts);
      
      // Cria o gráfico
      this.charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Pedidos por Categoria',
            data: data,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    },
    
    initUrgencyChart() {
      const ctx = this.$refs.urgencyChart.getContext('2d');
      
      // Contagem de pedidos por urgência
      const urgencyCounts = {};
      this.pedidos.forEach(pedido => {
        const urgencia = pedido.urgencia || 'Não definido';
        urgencyCounts[urgencia] = (urgencyCounts[urgencia] || 0) + 1;
      });
      
      // Cores para cada nível de urgência
      const urgencyColors = {
        'Padrão': '#32CD32',
        'Urgente': '#FFD700',
        'Crítico': '#FF6347',
        'Não definido': '#A9A9A9'
      };
      
      // Prepara dados para o gráfico
      const labels = Object.keys(urgencyCounts);
      const data = Object.values(urgencyCounts);
      const colors = labels.map(label => urgencyColors[label] || '#A9A9A9');
      
      // Cria o gráfico
      this.charts.urgency = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
      });
    },
    
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    getActivityIcon(tipo) {
      return `activity-icon-${tipo}`;
    },
    
    getActivityIconClass(tipo) {
      const iconMap = {
        'criacao': 'fas fa-plus',
        'edicao': 'fas fa-edit',
        'conclusao': 'fas fa-check',
        'cancelamento': 'fas fa-times',
        'login': 'fas fa-sign-in-alt',
        'registro': 'fas fa-user-plus'
      };
      
      return iconMap[tipo] || 'fas fa-info';
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
    
    async generateReport() {
      try {
        // Construir parâmetros do relatório
        const params = {
          tipo: this.reportOptions.tipo,
          periodo: this.reportOptions.periodo,
          formato: this.reportOptions.formato
        };
        
        // Adicionar datas se for personalizado
        if (this.reportOptions.periodo === 'personalizado') {
          params.dataInicial = this.reportOptions.dataInicial;
          params.dataFinal = this.reportOptions.dataFinal;
        }
        
        // Chamar API para gerar relatório
        const response = await axios.get('/relatorios/', {
          params: params,
          headers: {
            ...authService.getAuthHeaders(),
            'Accept': this.reportOptions.formato === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          },
          responseType: 'blob'
        });
        
        // Criar link para download
        const blob = new Blob([response.data], {
          type: this.reportOptions.formato === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Nome do arquivo
        const dataAtual = new Date().toISOString().split('T')[0];
        const extensao = this.reportOptions.formato === 'pdf' ? 'pdf' : 'xlsx';
        a.download = `relatorio_${this.reportOptions.tipo}_${dataAtual}.${extensao}`;
        
        // Disparar download
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        alert('Erro ao gerar relatório. Por favor, tente novamente.');
      }
    },
    
    async openOrderDetails(pedidoId) {
      try {
        const response = await axios.get(`/pedidos/${pedidoId}`, {
          headers: authService.getAuthHeaders()
        });
        this.selectedOrder = response.data;
        this.showOrderDetails = true;
      } catch (error) {
        console.error('Erro ao carregar detalhes do pedido:', error);
      }
    },
    
    closeOrderDetails() {
      this.showOrderDetails = false;
      this.selectedOrder = null;
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.dashboard-section {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.dashboard-section h2 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

/* Feed de Atividades */
.activity-feed {
  max-height: 400px;
  overflow-y: auto;
}

.loading, .empty-feed {
  text-align: center;
  padding: 20px;
  color: #777;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  display: flex;
  gap: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  transition: background-color 0.3s;
}

.activity-item:hover {
  background-color: #f0f0f0;
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
}

.activity-icon-criacao {
  background-color: #4CAF50;
}

.activity-icon-edicao {
  background-color: #2196F3;
}

.activity-icon-conclusao {
  background-color: #9C27B0;
}

.activity-icon-cancelamento {
  background-color: #FF5722;
}

.activity-icon-login {
  background-color: #607D8B;
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
  color: #333;
}

.activity-date {
  color: #777;
  font-size: 0.85em;
}

.activity-description {
  margin-bottom: 5px;
}

.activity-details a {
  color: #0066cc;
  text-decoration: underline;
  cursor: pointer;
}

/* Statistics and Charts */
.statistics-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.statistics-row {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.kpi-card {
  flex: 1;
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.kpi-card h3 {
  font-size: 16px;
  color: #555;
  margin-bottom: 10px;
}

.kpi-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.chart-wrapper {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  height: 300px;
  position: relative;
}

.chart-wrapper h3 {
  text-align: center;
  margin-bottom: 15px;
  font-size: 16px;
  color: #555;
}

canvas {
  width: 100%;
  height: 85%;
}

/* Relatórios */
.reports-container {
  padding: 10px;
}

.report-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 14px;
  color: #555;
}

.form-group select, .form-group input {
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.date-range {
  display: flex;
  gap: 10px;
}

.date-range > div {
  flex: 1;
}

.report-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-generate {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.btn-generate:hover {
  background-color: #388E3C;
}

/* Media queries para responsividade */
@media (max-width: 768px) {
  .statistics-row {
    flex-direction: column;
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .report-options {
    grid-template-columns: 1fr;
  }
  
  .date-range {
    flex-direction: column;
  }
}
</style> 