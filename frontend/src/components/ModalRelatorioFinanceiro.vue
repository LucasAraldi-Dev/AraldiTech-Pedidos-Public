<template>
  <div class="modal-overlay" v-if="isOpen" @click.self="fecharModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">
          <i class="material-icons">account_balance</i>
          Relatório Financeiro
        </h2>
        <button class="close-button" @click="fecharModal">
          <i class="material-icons">close</i>
        </button>
      </div>
      
      <div class="modal-body">
        <!-- Componente de Resumo Financeiro -->
        <FinancialSummary @edit-pedido="handleEditPedido" />
        
        <!-- Filtros adicionais para relatório -->
        <div class="filters-section">
          <h2>
            <i class="material-icons">filter_list</i>
            Filtros
          </h2>
          <div class="filters-grid">
            <div class="filter-group">
              <label for="periodFilter">Período:</label>
              <select id="periodFilter" v-model="filters.periodo">
                <option value="todos">Todos</option>
                <option value="hoje">Hoje</option>
                <option value="semana">Esta Semana</option>
                <option value="mes">Este Mês</option>
                <option value="trimestre">Este Trimestre</option>
                <option value="ano">Este Ano</option>
                <option value="personalizado">Personalizado</option>
              </select>
            </div>
            
            <div class="filter-group date-range" v-if="filters.periodo === 'personalizado'">
              <div>
                <label for="startDate">De:</label>
                <input type="date" id="startDate" v-model="filters.dataInicial">
              </div>
              <div>
                <label for="endDate">Até:</label>
                <input type="date" id="endDate" v-model="filters.dataFinal">
              </div>
            </div>
            
            <div class="filter-group">
              <label for="categoryFilter">Categoria:</label>
              <select id="categoryFilter" v-model="filters.categoria">
                <option value="todas">Todas</option>
                <option value="Matérias-primas">Matérias-primas</option>
                <option value="Equipamentos e Máquinas">Equipamentos e Máquinas</option>
                <option value="Peças de Reposição">Peças de Reposição</option>
                <option value="Serviços">Serviços</option>
                <option value="Mercadorias diversas">Mercadorias diversas</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label for="statusFilter">Status:</label>
              <select id="statusFilter" v-model="filters.status">
                <option value="todos">Todos</option>
                <option value="Pendente">Pendente</option>
                <option value="Concluído">Concluído</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label for="budgetFilter">Orçamento:</label>
              <select id="budgetFilter" v-model="filters.orcamento">
                <option value="todos">Todos</option>
                <option value="acima">Acima do Orçamento</option>
                <option value="dentro">Dentro do Orçamento</option>
                <option value="abaixo">Abaixo do Orçamento</option>
                <option value="sem">Sem Orçamento</option>
              </select>
            </div>
            
            <div class="filter-actions">
              <button class="btn-apply" @click="aplicarFiltros">
                <i class="material-icons">search</i>
                Aplicar Filtros
              </button>
              <button class="btn-reset" @click="resetFiltros">
                <i class="material-icons">clear</i>
                Limpar
              </button>
            </div>
          </div>
        </div>
        
        <!-- Botões de Ação -->
        <div class="action-buttons">
          <button class="btn-export" @click="exportarRelatorio('pdf')">
            <i class="material-icons">picture_as_pdf</i>
            Exportar como PDF
          </button>
          <button class="btn-export" @click="exportarRelatorio('excel')">
            <i class="material-icons">table_chart</i>
            Exportar como Excel
          </button>
          <button class="btn-export" @click="printReport">
            <i class="material-icons">print</i>
            Imprimir
          </button>
        </div>
        
        <!-- Análise Avançada (opcional) -->
        <div class="advanced-analysis" v-if="showAdvancedAnalysis">
          <h2>
            <i class="material-icons">assessment</i>
            Análise Avançada
          </h2>
          <div class="analysis-charts">
            <div class="chart-wrapper">
              <h3>Tendência de Gastos</h3>
              <canvas ref="trendChart"></canvas>
            </div>
            <div class="chart-wrapper">
              <h3>Distribuição por Categoria</h3>
              <canvas ref="categoryChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Modal de edição de pedido -->
  <ModalEditarPedido 
    v-if="showEditModal"
    :isOpen="showEditModal"
    :pedido="selectedPedido"
    @close="closeEditModal"
    @update-order="handleUpdatedOrder"
  />
</template>

<script>
import FinancialSummary from '@/components/FinancialSummary.vue';
import ModalEditarPedido from '@/components/ModalEditarPedido.vue';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
import { useToast } from 'vue-toastification';

// Registrar componentes Chart.js
Chart.register(...registerables);

export default {
  name: 'ModalRelatorioFinanceiro',
  components: {
    FinancialSummary,
    ModalEditarPedido
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      filters: {
        periodo: 'todos',
        dataInicial: this.getDefaultStartDate(),
        dataFinal: this.formatDateForInput(new Date()),
        categoria: 'todas',
        status: 'todos',
        orcamento: 'todos'
      },
      showAdvancedAnalysis: true,
      showEditModal: false,
      selectedPedido: null,
      charts: {
        trend: null,
        category: null
      },
      pedidos: []
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.fetchPedidos();
        });
      } else {
        // Limpar gráficos quando o modal for fechado
        this.destroyCharts();
      }
    }
  },
  mounted() {
    if (this.isOpen) {
      this.fetchPedidos();
    }
  },
  beforeUnmount() {
    this.destroyCharts();
  },
  methods: {
    destroyCharts() {
      Object.values(this.charts).forEach(chart => {
        if (chart) chart.destroy();
      });
    },
    
    fecharModal() {
      this.$emit('close');
    },
    
    async fetchPedidos() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.toast.error('Sessão expirada. Faça login novamente.');
          this.$router.push('/login');
          return;
        }
        
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.pedidos = response.data || [];
        
        // Inicializar os gráficos após buscar os dados
        this.$nextTick(() => {
          this.initCharts();
        });
      } catch (error) {
        console.error('Erro ao buscar pedidos:', error);
        this.toast.error('Erro ao carregar dados financeiros');
      }
    },
    
    aplicarFiltros() {
      this.updateCharts();
      this.toast.success('Filtros aplicados com sucesso');
    },
    
    resetFiltros() {
      this.filters = {
        periodo: 'todos',
        dataInicial: this.getDefaultStartDate(),
        dataFinal: this.formatDateForInput(new Date()),
        categoria: 'todas',
        status: 'todos',
        orcamento: 'todos'
      };
      this.updateCharts();
      this.toast.info('Filtros redefinidos');
    },
    
    handleEditPedido(pedido) {
      this.selectedPedido = pedido;
      this.showEditModal = true;
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.selectedPedido = null;
    },
    
    handleUpdatedOrder() {
      this.fetchPedidos();
      this.closeEditModal();
      this.toast.success('Pedido atualizado com sucesso');
    },
    
    initCharts() {
      this.destroyCharts();
      this.$nextTick(() => {
        this.initTrendChart();
        this.initCategoryChart();
      });
    },
    
    updateCharts() {
      this.initCharts();
    },
    
    initTrendChart() {
      const ctx = this.$refs.trendChart?.getContext('2d');
      if (!ctx) return;
      
      // Dados filtrados para tendência de gastos
      const pedidosFiltrados = this.aplicarFiltrosAosPedidos();
      
      // Agrupar por mês
      const dadosPorMes = {};
      const meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
      
      pedidosFiltrados.forEach(pedido => {
        const date = new Date(pedido.conclusao_data || pedido.deliveryDate);
        const mes = date.getMonth();
        
        if (!dadosPorMes[mes]) {
          dadosPorMes[mes] = {
            orcamento: 0,
            custo: 0
          };
        }
        
        dadosPorMes[mes].orcamento += parseFloat(pedido.orcamento_previsto || 0);
        dadosPorMes[mes].custo += parseFloat(pedido.custo_real || 0);
      });
      
      // Preparar dados para o gráfico
      const labels = [];
      const orcamentoData = [];
      const custoData = [];
      
      for (let i = 0; i < 12; i++) {
        labels.push(meses[i]);
        orcamentoData.push(dadosPorMes[i]?.orcamento || 0);
        custoData.push(dadosPorMes[i]?.custo || 0);
      }
      
      // Criar o gráfico
      this.charts.trend = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Orçamento Previsto',
              data: orcamentoData,
              borderColor: 'rgba(54, 162, 235, 1)',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              fill: true,
              tension: 0.4
            },
            {
              label: 'Custo Real',
              data: custoData,
              borderColor: 'rgba(255, 99, 132, 1)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              fill: true,
              tension: 0.4
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
                callback: function(value) {
                  return 'R$ ' + value.toLocaleString('pt-BR');
                }
              }
            }
          },
          plugins: {
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
    
    initCategoryChart() {
      const ctx = this.$refs.categoryChart?.getContext('2d');
      if (!ctx) return;
      
      // Dados filtrados
      const pedidosFiltrados = this.aplicarFiltrosAosPedidos();
      
      // Agrupar por categoria
      const dadosPorCategoria = {};
      
      pedidosFiltrados.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        
        if (!dadosPorCategoria[categoria]) {
          dadosPorCategoria[categoria] = {
            orcamento: 0,
            custo: 0
          };
        }
        
        dadosPorCategoria[categoria].orcamento += parseFloat(pedido.orcamento_previsto || 0);
        dadosPorCategoria[categoria].custo += parseFloat(pedido.custo_real || 0);
      });
      
      // Preparar dados para o gráfico
      const labels = Object.keys(dadosPorCategoria);
      const custoData = labels.map(cat => dadosPorCategoria[cat].custo);
      
      // Cores para cada categoria
      const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
      ];
      
      // Criar o gráfico
      this.charts.category = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Custo Real',
              data: custoData,
              backgroundColor: backgroundColors.slice(0, labels.length),
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw;
                  const percentage = Math.round((value / custoData.reduce((a, b) => a + b, 0)) * 100);
                  return `${label}: R$ ${value.toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  })} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    },
    
    aplicarFiltrosAosPedidos() {
      let pedidosFiltrados = [...this.pedidos];
      
      // Filtrar por período
      if (this.filters.periodo !== 'todos') {
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        
        let dataInicial = new Date(hoje);
        let dataFinal = new Date(hoje);
        dataFinal.setHours(23, 59, 59);
        
        switch (this.filters.periodo) {
          case 'hoje':
            // Já definido
            break;
          case 'semana':
            dataInicial.setDate(hoje.getDate() - hoje.getDay()); // Domingo da semana atual
            break;
          case 'mes':
            dataInicial.setDate(1); // Primeiro dia do mês
            break;
          case 'trimestre': {
            const mes = hoje.getMonth();
            dataInicial.setMonth(Math.floor(mes / 3) * 3, 1); // Primeiro dia do trimestre
            break;
          }
          case 'ano':
            dataInicial.setMonth(0, 1); // 1º de janeiro
            break;
          case 'personalizado':
            dataInicial = new Date(this.filters.dataInicial);
            dataFinal = new Date(this.filters.dataFinal);
            dataFinal.setHours(23, 59, 59);
            break;
        }
        
        pedidosFiltrados = pedidosFiltrados.filter(pedido => {
          const dataPedido = new Date(pedido.conclusao_data || pedido.deliveryDate);
          return dataPedido >= dataInicial && dataPedido <= dataFinal;
        });
      }
      
      // Filtrar por categoria
      if (this.filters.categoria !== 'todas') {
        pedidosFiltrados = pedidosFiltrados.filter(pedido => 
          pedido.categoria === this.filters.categoria
        );
      }
      
      // Filtrar por status
      if (this.filters.status !== 'todos') {
        pedidosFiltrados = pedidosFiltrados.filter(pedido => 
          pedido.status === this.filters.status
        );
      }
      
      // Filtrar por orçamento
      if (this.filters.orcamento !== 'todos') {
        switch (this.filters.orcamento) {
          case 'acima':
            pedidosFiltrados = pedidosFiltrados.filter(pedido => 
              parseFloat(pedido.custo_real || 0) > parseFloat(pedido.orcamento_previsto || 0) &&
              parseFloat(pedido.orcamento_previsto || 0) > 0
            );
            break;
          case 'dentro':
            pedidosFiltrados = pedidosFiltrados.filter(pedido => 
              parseFloat(pedido.custo_real || 0) <= parseFloat(pedido.orcamento_previsto || 0) &&
              parseFloat(pedido.orcamento_previsto || 0) > 0 &&
              parseFloat(pedido.custo_real || 0) > 0
            );
            break;
          case 'abaixo':
            pedidosFiltrados = pedidosFiltrados.filter(pedido => 
              parseFloat(pedido.custo_real || 0) < parseFloat(pedido.orcamento_previsto || 0) &&
              parseFloat(pedido.orcamento_previsto || 0) > 0
            );
            break;
          case 'sem':
            pedidosFiltrados = pedidosFiltrados.filter(pedido => 
              parseFloat(pedido.orcamento_previsto || 0) === 0
            );
            break;
        }
      }
      
      return pedidosFiltrados;
    },
    
    async exportarRelatorio(formato) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.toast.error('Sessão expirada. Faça login novamente.');
          this.$router.push('/login');
          return;
        }
        
        // Construir parâmetros do relatório
        const params = new URLSearchParams();
        params.append('tipo', 'financeiro');
        params.append('periodo', this.filters.periodo === 'personalizado' ? 'personalizado' : 'mensal');
        params.append('formato', formato);
        
        if (this.filters.periodo === 'personalizado') {
          params.append('dataInicial', this.filters.dataInicial);
          params.append('dataFinal', this.filters.dataFinal);
        }
        
        // Abrir em nova guia
        window.open(`${process.env.VUE_APP_API_URL}/relatorios/financeiro?${params.toString()}`, '_blank');
        
        this.toast.success(`Relatório sendo gerado em formato ${formato.toUpperCase()}`);
      } catch (error) {
        console.error('Erro ao exportar relatório:', error);
        this.toast.error('Erro ao gerar relatório');
      }
    },
    
    printReport() {
      window.print();
    },
    
    getDefaultStartDate() {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      return this.formatDateForInput(date);
    },
    
    formatDateForInput(date) {
      if (!date) return '';
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: 15px;
  box-sizing: border-box;
}

.modal-content {
  background-color: #1f1f1f;
  border-radius: 10px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  position: relative;
  color: #f5f5f5;
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
}

.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #333;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 4px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #333;
}

.modal-title {
  display: flex;
  align-items: center;
  font-size: 24px;
  color: #f5f5f5;
  margin: 0;
}

.modal-title i {
  font-size: 28px;
  margin-right: 15px;
  color: #ff6f61;
}

.close-button {
  background: none;
  border: none;
  color: #999;
  font-size: 24px;
  cursor: pointer;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.close-button:hover {
  color: #ff6f61;
  background-color: rgba(255, 111, 97, 0.1);
}

.modal-body {
  padding: 20px;
}

/* Filtros */
.filters-section {
  background-color: #2a2a2a;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  border: 1px solid #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.filters-section:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}

.filters-section h2 {
  display: flex;
  align-items: center;
  font-size: 20px;
  margin-top: 0;
  margin-bottom: 15px;
  color: #ff6f61;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.filters-section h2 i {
  margin-right: 10px;
  font-size: 24px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #ff6f61;
  display: flex;
  align-items: center;
}

.filter-group label::before {
  font-family: 'Material Icons';
  content: 'filter_list';
  margin-right: 5px;
  font-size: 18px;
}

.filter-group select,
.filter-group input {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #444;
  background-color: #333;
  color: #f5f5f5;
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #ff6f61;
  box-shadow: 0 0 0 2px rgba(255, 111, 97, 0.2);
}

.date-range {
  display: flex;
  gap: 10px;
}

.date-range > div {
  flex: 1;
}

.filter-actions {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  margin-top: 10px;
}

.btn-apply,
.btn-reset {
  padding: 10px 15px;
  border-radius: 6px;
  border: none;
  font-size: 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-apply {
  background-color: #555555;
  color: #f5f5f5;
}

.btn-apply:hover {
  background-color: #666666;
  transform: translateY(-2px);
}

.btn-reset {
  background-color: #444;
  color: #f5f5f5;
  border: 1px solid #555;
}

.btn-reset:hover {
  background-color: #555;
  transform: translateY(-2px);
}

/* Botões de ação */
.action-buttons {
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 10px;
  margin: 15px 0;
}

.btn-export {
  padding: 10px 15px;
  border-radius: 6px;
  border: none;
  background-color: #555555;
  color: #f5f5f5;
  font-size: 14px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #444;
}

.btn-export:hover {
  background-color: #666666;
  color: #f5f5f5;
  border-color: #666666;
  transform: translateY(-2px);
}

.btn-export i {
  font-size: 18px;
}

/* Análise Avançada */
.advanced-analysis {
  background-color: #2a2a2a;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
  border: 1px solid #333;
  transition: transform 0.3s, box-shadow 0.3s;
}

.advanced-analysis:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  transform: translateY(-3px);
}

.advanced-analysis h2 {
  display: flex;
  align-items: center;
  font-size: 20px;
  margin-top: 0;
  margin-bottom: 15px;
  color: #ff6f61;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.advanced-analysis h2 i {
  margin-right: 10px;
  font-size: 24px;
}

.analysis-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 15px;
}

.chart-wrapper {
  background-color: #333;
  border-radius: 8px;
  padding: 15px;
  height: 300px;
  border: 1px solid #444;
  transition: transform 0.3s;
}

.chart-wrapper:hover {
  transform: translateY(-3px);
  border-color: #ff6f61;
}

.chart-wrapper h3 {
  text-align: center;
  margin-top: 0;
  margin-bottom: 15px;
  color: #ff6f61;
  font-size: 16px;
}

/* Media queries */
@media (max-width: 992px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .analysis-charts {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-height: 95vh;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .date-range {
    flex-direction: column;
  }
  
  .action-buttons {
    justify-content: center;
  }
  
  .btn-export {
    flex: 1;
    justify-content: center;
  }
  
  .filter-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-apply, 
  .btn-reset {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .modal {
    padding: 10px;
  }
  
  .modal-content {
    width: 100%;
  }
  
  .modal-header {
    padding: 15px;
  }
  
  .modal-title {
    font-size: 20px;
  }
  
  .modal-title i {
    font-size: 24px;
  }
  
  .modal-body {
    padding: 15px;
  }
  
  .filters-section, 
  .advanced-analysis {
    padding: 15px;
  }
  
  .filters-section h2, 
  .advanced-analysis h2 {
    font-size: 18px;
  }
  
  .chart-wrapper {
    height: 250px;
  }
}

/* Estilos de impressão */
@media print {
  .filters-section,
  .action-buttons,
  .modal-header .close-button {
    display: none;
  }
  
  .modal {
    position: static;
    background: white;
    padding: 0;
  }
  
  .modal-content {
    box-shadow: none;
    max-height: none;
    width: 100%;
    background-color: white;
    color: black;
  }
  
  .modal-body {
    color: black;
  }
  
  .modal-header {
    border-color: #ccc;
  }
  
  .modal-title {
    color: black;
  }
  
  .modal-title i {
    color: #555;
  }
  
  .advanced-analysis,
  .chart-wrapper {
    background-color: white;
    color: black;
    box-shadow: none;
    border: 1px solid #ccc;
  }
  
  .chart-wrapper h3 {
    color: black;
  }
}
</style> 