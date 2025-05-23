<template>
  <div class="overview-container">
    <!-- Métricas Principais -->
    <div class="metrics-section">
      <div class="section-header">
        <h3>
          <i class="material-icons">insights</i>
          Métricas Principais
        </h3>
        <button class="refresh-btn" @click="$emit('refresh')" :disabled="isLoading">
          <i class="material-icons" :class="{ 'spinning': isLoading }">refresh</i>
          <span>Atualizar</span>
        </button>
      </div>

      <div v-if="isLoading" class="loading-container">
        <LoadingIndicator message="Carregando métricas..." />
      </div>

      <div v-else class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon">
            <i class="material-icons">shopping_cart</i>
          </div>
          <div class="metric-content">
            <h4 class="metric-title">Total de Pedidos</h4>
            <div class="metric-value">{{ totalPedidos }}</div>
            <div class="metric-trend" :class="trendClass">
              <i class="material-icons">{{ trendIcon }}</i>
              <span>{{ trendText }}</span>
            </div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon pending">
            <i class="material-icons">pending_actions</i>
          </div>
          <div class="metric-content">
            <h4 class="metric-title">Pedidos Pendentes</h4>
            <div class="metric-value">{{ pedidosPendentes }}</div>
            <div class="metric-subtitle">{{ percentualPendentes }}% do total</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon success">
            <i class="material-icons">check_circle</i>
          </div>
          <div class="metric-content">
            <h4 class="metric-title">Concluídos</h4>
            <div class="metric-value">{{ pedidosConcluidos }}</div>
            <div class="metric-subtitle">{{ percentualConcluidos }}% do total</div>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon time">
            <i class="material-icons">timer</i>
          </div>
          <div class="metric-content">
            <h4 class="metric-title">Tempo Médio</h4>
            <div class="metric-value">{{ tempoMedioConclusao }}</div>
            <div class="metric-subtitle">de conclusão</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Overview -->
    <div class="status-section">
      <div class="section-header">
        <h3>
          <i class="material-icons">donut_large</i>
          Distribuição por Status
        </h3>
      </div>

      <div class="status-overview">
        <div 
          v-for="status in statusDistribution" 
          :key="status.name"
          class="status-item"
          :class="status.class"
        >
          <div class="status-bar">
            <div 
              class="status-fill" 
              :style="{ width: status.percentage + '%' }"
            ></div>
          </div>
          <div class="status-info">
            <span class="status-name">{{ status.name }}</span>
            <span class="status-count">{{ status.count }} ({{ status.percentage }}%)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Atividades Recentes -->
    <div class="activities-section">
      <div class="section-header">
        <h3>
          <i class="material-icons">history</i>
          Atividades Recentes
        </h3>
        <button class="view-all-btn" @click="viewAllActivities">
          <span>Ver todas</span>
          <i class="material-icons">arrow_forward</i>
        </button>
      </div>

      <div v-if="activities.length === 0" class="empty-state">
        <i class="material-icons">info</i>
        <p>Nenhuma atividade recente encontrada</p>
      </div>

      <div v-else class="activities-list">
        <div 
          v-for="(activity, index) in recentActivities" 
          :key="index" 
          class="activity-item"
        >
          <div class="activity-icon">
            <i class="material-icons">{{ getActivityIcon(activity.tipo) }}</i>
          </div>
          <div class="activity-content">
            <div class="activity-description">{{ activity.descricao }}</div>
            <div class="activity-meta">
              <span class="activity-time">{{ formatDateTime(activity.data_hora) }}</span>
              <span class="activity-type">{{ getActivityTypeLabel(activity.tipo) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions-section">
      <div class="section-header">
        <h3>
          <i class="material-icons">flash_on</i>
          Ações Rápidas
        </h3>
      </div>

      <div class="quick-actions-grid">
        <button class="quick-action-btn" @click="createNewOrder">
          <i class="material-icons">add_circle</i>
          <span>Novo Pedido</span>
        </button>
        <button class="quick-action-btn" @click="viewPendingOrders">
          <i class="material-icons">pending_actions</i>
          <span>Ver Pendentes</span>
        </button>
        <button class="quick-action-btn" @click="generateQuickReport">
          <i class="material-icons">description</i>
          <span>Relatório Rápido</span>
        </button>
        <button class="quick-action-btn" @click="viewFinancialSummary">
          <i class="material-icons">account_balance</i>
          <span>Resumo Financeiro</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

export default {
  name: 'DashboardOverview',
  components: {
    LoadingIndicator
  },
  emits: ['refresh'],
  props: {
    pedidos: {
      type: Array,
      default: () => []
    },
    activities: {
      type: Array,
      default: () => []
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    // Computed properties para métricas
    const totalPedidos = computed(() => props.pedidos.length);
    
    const pedidosPendentes = computed(() => 
      props.pedidos.filter(p => p.status === 'Pendente').length
    );
    
    const pedidosConcluidos = computed(() => 
      props.pedidos.filter(p => p.status === 'Concluído').length
    );
    
    const percentualPendentes = computed(() => {
      if (totalPedidos.value === 0) return 0;
      return Math.round((pedidosPendentes.value / totalPedidos.value) * 100);
    });
    
    const percentualConcluidos = computed(() => {
      if (totalPedidos.value === 0) return 0;
      return Math.round((pedidosConcluidos.value / totalPedidos.value) * 100);
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

    // Distribuição por status
    const statusDistribution = computed(() => {
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
      
      const total = totalPedidos.value;
      
      return Object.entries(statusCount).map(([name, count]) => ({
        name,
        count,
        percentage: total > 0 ? Math.round((count / total) * 100) : 0,
        class: name.toLowerCase().replace(' ', '-')
      }));
    });

    // Atividades recentes (últimas 5)
    const recentActivities = computed(() => 
      props.activities.slice(0, 5)
    );

    // Trend indicators (simulado - pode ser implementado com dados históricos)
    const trendClass = computed(() => 'positive');
    const trendIcon = computed(() => 'trending_up');
    const trendText = computed(() => '+12% este mês');

    // Métodos
    const getActivityIcon = (tipo) => {
      const icons = {
        'criar': 'add_circle',
        'editar': 'edit',
        'concluir': 'check_circle',
        'cancelar': 'cancel',
        'financeiro': 'attach_money',
        'comentario': 'comment',
        'default': 'info'
      };
      return icons[tipo] || icons.default;
    };

    const getActivityTypeLabel = (tipo) => {
      const labels = {
        'criar': 'Criação',
        'editar': 'Edição',
        'concluir': 'Conclusão',
        'cancelar': 'Cancelamento',
        'financeiro': 'Financeiro',
        'comentario': 'Comentário'
      };
      return labels[tipo] || 'Atividade';
    };

    const formatDateTime = (dateString) => {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString;
      
      return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };

    // Actions
    const viewAllActivities = () => {
      // Implementar navegação para página de atividades
      console.log('Ver todas as atividades');
    };

    const createNewOrder = () => {
      // Implementar abertura do modal de criar pedido
      console.log('Criar novo pedido');
    };

    const viewPendingOrders = () => {
      // Implementar filtro para pedidos pendentes
      console.log('Ver pedidos pendentes');
    };

    const generateQuickReport = () => {
      // Implementar geração de relatório rápido
      console.log('Gerar relatório rápido');
    };

    const viewFinancialSummary = () => {
      // Implementar abertura do resumo financeiro
      console.log('Ver resumo financeiro');
    };

    return {
      // Computed
      totalPedidos,
      pedidosPendentes,
      pedidosConcluidos,
      percentualPendentes,
      percentualConcluidos,
      tempoMedioConclusao,
      statusDistribution,
      recentActivities,
      trendClass,
      trendIcon,
      trendText,
      
      // Methods
      getActivityIcon,
      getActivityTypeLabel,
      formatDateTime,
      viewAllActivities,
      createNewOrder,
      viewPendingOrders,
      generateQuickReport,
      viewFinancialSummary
    };
  }
};
</script>

<style scoped>
.overview-container {
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

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Loading */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
}

.metric-card {
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

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff6f61, #ff8a80);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6f61, #ff8a80);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.metric-icon.pending {
  background: linear-gradient(135deg, #ffa726, #ffcc02);
}

.metric-icon.success {
  background: linear-gradient(135deg, #66bb6a, #81c784);
}

.metric-icon.time {
  background: linear-gradient(135deg, #42a5f5, #64b5f6);
}

.metric-icon i {
  color: white;
  font-size: var(--font-size-xl);
}

.metric-content {
  flex: 1;
}

.metric-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #aaa;
  font-weight: 500;
}

.metric-value {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: var(--spacing-xs);
}

.metric-subtitle {
  font-size: var(--font-size-xs);
  color: #888;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: var(--font-size-xs);
  margin-top: var(--spacing-xs);
}

.metric-trend.positive {
  color: #4caf50;
}

.metric-trend.negative {
  color: #f44336;
}

.metric-trend i {
  font-size: var(--font-size-sm);
}

/* Status Overview */
.status-overview {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.status-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

.status-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.status-fill {
  height: 100%;
  background: #ff6f61;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.status-item.pendente .status-fill {
  background: linear-gradient(90deg, #ffa726, #ffcc02);
}

.status-item.concluído .status-fill {
  background: linear-gradient(90deg, #66bb6a, #81c784);
}

.status-item.cancelado .status-fill {
  background: linear-gradient(90deg, #78909c, #90a4ae);
}

.status-info {
  display: flex;
  flex-direction: column;
  min-width: 120px;
}

.status-name {
  font-size: var(--font-size-sm);
  color: #f5f5f5;
  font-weight: 500;
}

.status-count {
  font-size: var(--font-size-xs);
  color: #aaa;
}

/* Activities */
.view-all-btn {
  background: none;
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

.view-all-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

.activities-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 111, 97, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.activity-icon i {
  color: #ff6f61;
  font-size: var(--font-size-md);
}

.activity-content {
  flex: 1;
}

.activity-description {
  font-size: var(--font-size-sm);
  color: #f5f5f5;
  margin-bottom: 0.25rem;
}

.activity-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.activity-time {
  font-size: var(--font-size-xs);
  color: #aaa;
}

.activity-type {
  font-size: var(--font-size-xs);
  color: #ff6f61;
  background: rgba(255, 111, 97, 0.1);
  padding: 0.125rem 0.375rem;
  border-radius: 0.75rem;
}

/* Quick Actions */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.quick-action-btn {
  background: linear-gradient(135deg, #333 0%, #2a2a2a 100%);
  border: 1px solid #444;
  color: #f5f5f5;
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.quick-action-btn:hover {
  background: linear-gradient(135deg, #3a3a3a 0%, #333 100%);
  border-color: #ff6f61;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.quick-action-btn i {
  font-size: var(--font-size-xxl);
  color: #ff6f61;
}

.quick-action-btn span {
  font-size: var(--font-size-sm);
  font-weight: 500;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: #777;
  text-align: center;
}

.empty-state i {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-sm);
  color: #555;
}

.empty-state p {
  font-size: var(--font-size-sm);
  margin: 0;
}

/* Responsividade */
@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .metric-card {
    padding: var(--spacing-md);
  }

  .metric-icon {
    width: 48px;
    height: 48px;
  }

  .metric-value {
    font-size: var(--font-size-xl);
  }
}

@media (max-width: 480px) {
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .status-item {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .status-info {
    min-width: auto;
  }
}
</style> 