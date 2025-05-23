<template>
  <div class="dynamic-reports">
    <!-- Cabeçalho -->
    <div class="reports-header">
      <h2 class="reports-title">
        <i class="fas fa-chart-line"></i>
        Relatórios Dinâmicos
      </h2>
      <p class="reports-subtitle">Análise interativa em tempo real</p>
    </div>

    <!-- Filtros -->
    <div class="filters-section">
      <div class="filters-grid">
        <!-- Tipo de Relatório -->
        <div class="filter-group">
          <label>Tipo de Relatório</label>
          <select v-model="filters.tipo" @change="loadData">
            <option value="pedidos">Pedidos</option>
            <option value="atividades">Atividades</option>
          </select>
        </div>

        <!-- Período -->
        <div class="filter-group">
          <label>Período</label>
          <select v-model="filters.periodo" @change="loadData">
            <option value="diario">Hoje</option>
            <option value="semanal">Últimos 7 dias</option>
            <option value="mensal">Este mês</option>
            <option value="personalizado">Personalizado</option>
          </select>
        </div>

        <!-- Datas Personalizadas -->
        <div v-if="filters.periodo === 'personalizado'" class="filter-group date-range">
          <label>Data Inicial</label>
          <input type="date" v-model="filters.dataInicial" @change="loadData">
          <label>Data Final</label>
          <input type="date" v-model="filters.dataFinal" @change="loadData">
        </div>

        <!-- Filtros específicos para Pedidos -->
        <template v-if="filters.tipo === 'pedidos'">
          <div class="filter-group">
            <label>Status</label>
            <select v-model="filters.status" @change="loadData">
              <option value="">Todos</option>
              <option value="Pendente">Pendente</option>
              <option value="Concluído">Concluído</option>
              <option value="Cancelado">Cancelado</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Categoria</label>
            <select v-model="filters.categoria" @change="loadData">
              <option value="">Todas</option>
              <option value="Equipamentos">Equipamentos</option>
              <option value="Matérias-primas">Matérias-primas</option>
              <option value="Peças de Reposição">Peças de Reposição</option>
              <option value="Serviços">Serviços</option>
              <option value="Material de Escritório">Material de Escritório</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Urgência</label>
            <select v-model="filters.urgencia" @change="loadData">
              <option value="">Todas</option>
              <option value="Normal">Normal</option>
              <option value="Urgente">Urgente</option>
              <option value="Crítico">Crítico</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Setor</label>
            <select v-model="filters.setor" @change="loadData">
              <option value="">Todos</option>
              <option value="Escritório">Escritório</option>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="CPO">CPO</option>
              <option value="Granjas">Granjas</option>
              <option value="Abatedouro">Abatedouro</option>
            </select>
          </div>
        </template>

        <!-- Filtro de Usuário -->
        <div class="filter-group">
          <label>Usuário</label>
          <select v-model="filters.usuario" @change="loadData">
            <option value="">Todos</option>
            <option v-for="user in availableUsers" :key="user" :value="user">
              {{ user }}
            </option>
          </select>
        </div>
      </div>

      <!-- Botões de Ação -->
      <div class="action-buttons">
        <button @click="clearFilters" class="btn-secondary">
          <i class="fas fa-eraser"></i>
          Limpar Filtros
        </button>
        <button @click="exportReport('pdf')" class="btn-primary">
          <i class="fas fa-file-pdf"></i>
          Exportar PDF
        </button>
        <button @click="exportReport('excel')" class="btn-primary">
          <i class="fas fa-file-excel"></i>
          Exportar Excel
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-section">
      <div class="spinner"></div>
      <p>Carregando dados...</p>
    </div>

    <!-- Métricas -->
    <div v-if="!loading && reportData" class="metrics-section">
      <div class="metrics-grid">
        <!-- Métrica Total -->
        <div class="metric-card total">
          <div class="metric-icon">
            <i class="fas fa-database"></i>
          </div>
          <div class="metric-content">
            <h3>{{ reportData.metricas.total_registros }}</h3>
            <p>Total de Registros</p>
          </div>
        </div>

        <!-- Métricas específicas para Pedidos -->
        <template v-if="filters.tipo === 'pedidos'">
          <div class="metric-card success">
            <div class="metric-icon">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="metric-content">
              <h3>{{ reportData.metricas.taxa_conclusao }}%</h3>
              <p>Taxa de Conclusão</p>
            </div>
          </div>

          <div class="metric-card warning">
            <div class="metric-icon">
              <i class="fas fa-clock"></i>
            </div>
            <div class="metric-content">
              <h3>{{ getPendingCount() }}</h3>
              <p>Pedidos Pendentes</p>
            </div>
          </div>

          <div class="metric-card info">
            <div class="metric-icon">
              <i class="fas fa-chart-pie"></i>
            </div>
            <div class="metric-content">
              <h3>{{ getTopCategory() }}</h3>
              <p>Categoria Principal</p>
            </div>
          </div>
        </template>

        <!-- Métricas específicas para Atividades -->
        <template v-if="filters.tipo === 'atividades'">
          <div class="metric-card info">
            <div class="metric-icon">
              <i class="fas fa-plus-circle"></i>
            </div>
            <div class="metric-content">
              <h3>{{ getActivityCount('criacao') }}</h3>
              <p>Criações</p>
            </div>
          </div>

          <div class="metric-card warning">
            <div class="metric-icon">
              <i class="fas fa-edit"></i>
            </div>
            <div class="metric-content">
              <h3>{{ getActivityCount('atualizacao') }}</h3>
              <p>Atualizações</p>
            </div>
          </div>

          <div class="metric-card success">
            <div class="metric-icon">
              <i class="fas fa-eye"></i>
            </div>
            <div class="metric-content">
              <h3>{{ getActivityCount('consulta') }}</h3>
              <p>Consultas</p>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Gráficos -->
    <div v-if="!loading && reportData" class="charts-section">
      <div class="charts-grid">
        <!-- Gráfico de Status/Tipo -->
        <div class="chart-card">
          <h3>{{ filters.tipo === 'pedidos' ? 'Distribuição por Status' : 'Distribuição por Tipo' }}</h3>
          <canvas ref="statusChart"></canvas>
        </div>

        <!-- Gráfico de Categorias/Usuários -->
        <div class="chart-card">
          <h3>{{ filters.tipo === 'pedidos' ? 'Top Categorias' : 'Top Usuários' }}</h3>
          <canvas ref="categoryChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Tabela de Dados -->
    <div v-if="!loading && reportData" class="data-section">
      <div class="data-header">
        <h3>
          <i class="fas fa-table"></i>
          Dados Detalhados
        </h3>
        <div class="data-info">
          <span>{{ reportData.periodo_info.label }}</span>
          <span class="separator">•</span>
          <span>{{ reportData.paginacao.total_registros }} registros</span>
        </div>
      </div>

      <!-- Tabela -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th v-for="column in tableColumns" :key="column.key">
                {{ column.label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in reportData.data" :key="item.id">
              <td v-for="column in tableColumns" :key="column.key">
                <span v-if="column.key === 'status'" :class="getStatusClass(item[column.key])">
                  {{ item[column.key] }}
                </span>
                <span v-else-if="column.key === 'urgencia'" :class="getUrgencyClass(item[column.key])">
                  {{ item[column.key] }}
                </span>
                <span v-else>
                  {{ item[column.key] || '-' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginação -->
      <div class="pagination">
        <button 
          @click="changePage(reportData.paginacao.pagina_atual - 1)"
          :disabled="reportData.paginacao.pagina_atual <= 1"
          class="btn-pagination"
        >
          <i class="fas fa-chevron-left"></i>
          Anterior
        </button>
        
        <span class="pagination-info">
          Página {{ reportData.paginacao.pagina_atual }} de {{ reportData.paginacao.total_paginas }}
        </span>
        
        <button 
          @click="changePage(reportData.paginacao.pagina_atual + 1)"
          :disabled="reportData.paginacao.pagina_atual >= reportData.paginacao.total_paginas"
          class="btn-pagination"
        >
          Próxima
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
    </div>

    <!-- Estado Vazio -->
    <div v-if="!loading && (!reportData || reportData.data.length === 0)" class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-chart-line"></i>
      </div>
      <h3>Nenhum dado encontrado</h3>
      <p>Tente ajustar os filtros para encontrar dados no período selecionado.</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Chart from 'chart.js/auto'

export default {
  name: 'DynamicReports',
  setup() {
    const authStore = useAuthStore()
    const loading = ref(false)
    const reportData = ref(null)
    const availableUsers = ref([])
    const currentPage = ref(1)
    
    // Charts
    const statusChart = ref(null)
    const categoryChart = ref(null)
    let statusChartInstance = null
    let categoryChartInstance = null

    const filters = reactive({
      tipo: 'pedidos',
      periodo: 'mensal',
      dataInicial: '',
      dataFinal: '',
      status: '',
      categoria: '',
      urgencia: '',
      setor: '',
      usuario: ''
    })

    const tableColumns = computed(() => {
      if (filters.tipo === 'pedidos') {
        return [
          { key: 'id', label: 'ID' },
          { key: 'descricao', label: 'Descrição' },
          { key: 'quantidade', label: 'Qtd' },
          { key: 'status', label: 'Status' },
          { key: 'urgencia', label: 'Urgência' },
          { key: 'categoria', label: 'Categoria' },
          { key: 'setor', label: 'Setor' },
          { key: 'deliveryDate', label: 'Data Entrega' }
        ]
      } else {
        return [
          { key: 'id', label: 'ID' },
          { key: 'tipo', label: 'Tipo' },
          { key: 'descricao', label: 'Descrição' },
          { key: 'usuario_nome', label: 'Usuário' },
          { key: 'data', label: 'Data/Hora' }
        ]
      }
    })

    const loadData = async () => {
      loading.value = true
      try {
        const params = new URLSearchParams({
          tipo: filters.tipo,
          periodo: filters.periodo,
          page: currentPage.value,
          limit: 50
        })

        // Adicionar filtros opcionais
        if (filters.dataInicial) params.append('dataInicial', filters.dataInicial)
        if (filters.dataFinal) params.append('dataFinal', filters.dataFinal)
        if (filters.status) params.append('status', filters.status)
        if (filters.categoria) params.append('categoria', filters.categoria)
        if (filters.urgencia) params.append('urgencia', filters.urgencia)
        if (filters.setor) params.append('setor', filters.setor)
        if (filters.usuario) params.append('usuario', filters.usuario)

        const response = await fetch(`/api/relatorios/dados?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`,
            'Content-Type': 'application/json'
          }
        })

        if (!response.ok) {
          throw new Error('Erro ao carregar dados')
        }

        const data = await response.json()
        reportData.value = data

        // Atualizar gráficos
        await nextTick()
        updateCharts()

      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        // Mostrar notificação de erro
      } finally {
        loading.value = false
      }
    }

    const updateCharts = () => {
      if (!reportData.value) return

      // Destruir gráficos existentes
      if (statusChartInstance) {
        statusChartInstance.destroy()
      }
      if (categoryChartInstance) {
        categoryChartInstance.destroy()
      }

      // Gráfico de Status/Tipo
      if (statusChart.value) {
        const ctx = statusChart.value.getContext('2d')
        const data = filters.tipo === 'pedidos' 
          ? reportData.value.metricas.status_distribution
          : reportData.value.metricas.tipo_distribution

        statusChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: data.map(item => item.label),
            datasets: [{
              data: data.map(item => item.value),
              backgroundColor: [
                '#4CAF50', // Verde
                '#FF9800', // Laranja
                '#F44336', // Vermelho
                '#2196F3', // Azul
                '#9C27B0'  // Roxo
              ]
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        })
      }

      // Gráfico de Categorias/Usuários
      if (categoryChart.value) {
        const ctx = categoryChart.value.getContext('2d')
        const data = filters.tipo === 'pedidos' 
          ? reportData.value.metricas.categoria_top
          : reportData.value.metricas.usuario_top

        categoryChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.map(item => item.label),
            datasets: [{
              label: 'Quantidade',
              data: data.map(item => item.value),
              backgroundColor: '#2196F3'
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
    }

    const clearFilters = () => {
      filters.status = ''
      filters.categoria = ''
      filters.urgencia = ''
      filters.setor = ''
      filters.usuario = ''
      currentPage.value = 1
      loadData()
    }

    const changePage = (page) => {
      currentPage.value = page
      loadData()
    }

    const exportReport = async (format) => {
      try {
        const params = new URLSearchParams({
          tipo: filters.tipo,
          periodo: filters.periodo,
          formato: format
        })

        // Adicionar filtros
        if (filters.dataInicial) params.append('dataInicial', filters.dataInicial)
        if (filters.dataFinal) params.append('dataFinal', filters.dataFinal)
        if (filters.status) params.append('status', filters.status)
        if (filters.categoria) params.append('categoria', filters.categoria)
        if (filters.urgencia) params.append('urgencia', filters.urgencia)
        if (filters.setor) params.append('setor', filters.setor)
        if (filters.usuario) params.append('usuario', filters.usuario)

        const response = await fetch(`/api/relatorios/?${params}`, {
          headers: {
            'Authorization': `Bearer ${authStore.token}`
          }
        })

        if (!response.ok) {
          throw new Error('Erro ao exportar relatório')
        }

        // Download do arquivo
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `relatorio_${filters.tipo}_${new Date().toISOString().split('T')[0]}.${format === 'excel' ? 'xlsx' : format}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)

      } catch (error) {
        console.error('Erro ao exportar:', error)
      }
    }

    // Métodos auxiliares
    const getPendingCount = () => {
      if (!reportData.value?.metricas?.status_distribution) return 0
      const pending = reportData.value.metricas.status_distribution.find(item => item.label === 'Pendente')
      return pending ? pending.value : 0
    }

    const getTopCategory = () => {
      if (!reportData.value?.metricas?.categoria_top?.length) return '-'
      return reportData.value.metricas.categoria_top[0].label
    }

    const getActivityCount = (tipo) => {
      if (!reportData.value?.metricas?.tipo_distribution) return 0
      const activity = reportData.value.metricas.tipo_distribution.find(item => item.label === tipo)
      return activity ? activity.value : 0
    }

    const getStatusClass = (status) => {
      const classes = {
        'Pendente': 'status-pending',
        'Concluído': 'status-completed',
        'Cancelado': 'status-cancelled'
      }
      return classes[status] || ''
    }

    const getUrgencyClass = (urgencia) => {
      const classes = {
        'Normal': 'urgency-normal',
        'Urgente': 'urgency-urgent',
        'Crítico': 'urgency-critical'
      }
      return classes[urgencia] || ''
    }

    onMounted(() => {
      loadData()
    })

    return {
      loading,
      reportData,
      availableUsers,
      filters,
      tableColumns,
      statusChart,
      categoryChart,
      loadData,
      clearFilters,
      changePage,
      exportReport,
      getPendingCount,
      getTopCategory,
      getActivityCount,
      getStatusClass,
      getUrgencyClass
    }
  }
}
</script>

<style scoped>
.dynamic-reports {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.reports-header {
  text-align: center;
  margin-bottom: 30px;
}

.reports-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
}

.reports-title i {
  margin-right: 15px;
  color: #2196F3;
}

.reports-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.filters-section {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.filter-group.date-range {
  grid-column: span 2;
  display: grid;
  grid-template-columns: auto 1fr auto 1fr;
  gap: 10px;
  align-items: end;
}

.filter-group label {
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.filter-group select,
.filter-group input {
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #2196F3;
}

.action-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.btn-primary:hover {
  background: #1976D2;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.loading-section {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.metrics-section {
  margin-bottom: 30px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.metric-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s;
}

.metric-card:hover {
  transform: translateY(-5px);
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.metric-card.total .metric-icon { background: #2196F3; }
.metric-card.success .metric-icon { background: #4CAF50; }
.metric-card.warning .metric-icon { background: #FF9800; }
.metric-card.info .metric-icon { background: #9C27B0; }

.metric-content h3 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0 0 5px 0;
  color: #333;
}

.metric-content p {
  margin: 0;
  color: #666;
  font-weight: 500;
}

.charts-section {
  margin-bottom: 30px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-card h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 1.2rem;
}

.data-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.data-header {
  padding: 25px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.data-header h3 {
  margin: 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.data-info {
  color: #666;
  font-size: 0.9rem;
}

.separator {
  margin: 0 10px;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f8f9fa;
  padding: 15px 12px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #e0e0e0;
}

.data-table td {
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.data-table tr:hover {
  background: #f8f9fa;
}

.status-pending { color: #FF9800; font-weight: 600; }
.status-completed { color: #4CAF50; font-weight: 600; }
.status-cancelled { color: #F44336; font-weight: 600; }

.urgency-normal { color: #2196F3; }
.urgency-urgent { color: #FF9800; font-weight: 600; }
.urgency-critical { color: #F44336; font-weight: 600; }

.pagination {
  padding: 20px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e0e0e0;
}

.btn-pagination {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.btn-pagination:hover:not(:disabled) {
  background: #f5f5f5;
  border-color: #2196F3;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 500;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  font-size: 1.5rem;
}

.empty-state p {
  margin: 0;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .dynamic-reports {
    padding: 15px;
  }
  
  .reports-title {
    font-size: 2rem;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-group.date-range {
    grid-column: span 1;
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .data-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .pagination {
    flex-direction: column;
    gap: 15px;
  }
}
</style> 