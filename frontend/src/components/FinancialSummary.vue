<template>
  <div class="financial-summary">
    <div class="summary-header">
      <h3>
        <i class="material-icons">account_balance</i>
        Resumo Financeiro
      </h3>
    </div>

    <div class="summary-cards">
      <div class="summary-card">
        <div class="card-icon">
          <i class="material-icons">monetization_on</i>
        </div>
        <div class="card-content">
          <h4>Orçamento Total</h4>
          <div class="card-value">R$ {{ formatCurrency(orcamentoTotal) }}</div>
        </div>
      </div>

      <div class="summary-card">
        <div class="card-icon spent">
          <i class="material-icons">shopping_cart</i>
        </div>
        <div class="card-content">
          <h4>Custo Real</h4>
          <div class="card-value">R$ {{ formatCurrency(custoRealTotal) }}</div>
        </div>
      </div>

      <div class="summary-card" :class="saldoFinanceiro >= 0 ? 'positive' : 'negative'">
        <div class="card-icon" :class="saldoFinanceiro >= 0 ? 'savings' : 'deficit'">
          <i class="material-icons">{{ saldoFinanceiro >= 0 ? 'savings' : 'money_off' }}</i>
        </div>
        <div class="card-content">
          <h4>{{ saldoFinanceiro >= 0 ? 'Economia' : 'Déficit' }}</h4>
          <div class="card-value">R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}</div>
        </div>
      </div>
    </div>

    <div class="summary-details" v-if="pedidos.length > 0">
      <h4>Detalhes por Pedido</h4>
      <div class="details-table">
        <div class="table-header">
          <span>Pedido</span>
          <span>Categoria</span>
          <span>Orçamento</span>
          <span>Custo Real</span>
          <span>Diferença</span>
          <span>Ações</span>
        </div>
        <div 
          v-for="pedido in pedidos.slice(0, 10)" 
          :key="pedido.id"
          class="table-row"
        >
          <span>#{{ pedido.id }}</span>
          <span>{{ pedido.categoria || 'N/A' }}</span>
          <span>R$ {{ formatCurrency(pedido.orcamento_previsto || 0) }}</span>
          <span>R$ {{ formatCurrency(pedido.custo_real || 0) }}</span>
          <span :class="getDifferenceClass(pedido)">
            R$ {{ formatCurrency(getDifference(pedido)) }}
          </span>
          <span>
            <button class="edit-btn" @click="$emit('edit-pedido', pedido)">
              <i class="material-icons">edit</i>
            </button>
          </span>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <i class="material-icons">info</i>
      <p>Nenhum dado financeiro disponível</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'FinancialSummary',
  emits: ['edit-pedido'],
  props: {
    pedidos: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
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

    const formatCurrency = (value) => {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    const getDifference = (pedido) => {
      const orcamento = parseFloat(pedido.orcamento_previsto || 0);
      const custo = parseFloat(pedido.custo_real || 0);
      return orcamento - custo;
    };

    const getDifferenceClass = (pedido) => {
      const diff = getDifference(pedido);
      if (diff > 0) return 'positive';
      if (diff < 0) return 'negative';
      return 'neutral';
    };

    return {
      orcamentoTotal,
      custoRealTotal,
      saldoFinanceiro,
      formatCurrency,
      getDifference,
      getDifferenceClass
    };
  }
};
</script>

<style scoped>
.financial-summary {
  background: #1a1a1a;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.summary-header {
  margin-bottom: var(--spacing-lg);
}

.summary-header h3 {
  margin: 0;
  color: #f5f5f5;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-lg);
}

.summary-header h3 i {
  color: #ff6f61;
  font-size: var(--font-size-xl);
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid #333;
  transition: all 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.card-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4DB6AC, #66BB6A);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon.spent {
  background: linear-gradient(135deg, #FF6F61, #FF8A80);
}

.card-icon.savings {
  background: linear-gradient(135deg, #66BB6A, #81C784);
}

.card-icon.deficit {
  background: linear-gradient(135deg, #EF5350, #E57373);
}

.card-icon i {
  color: white;
  font-size: var(--font-size-lg);
}

.card-content h4 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: #aaa;
  font-weight: 500;
}

.card-value {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: #f5f5f5;
}

.summary-details h4 {
  margin: 0 0 var(--spacing-md) 0;
  color: #f5f5f5;
  font-size: var(--font-size-md);
}

.details-table {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-sm);
  overflow: hidden;
}

.table-header,
.table-row {
  display: grid;
  grid-template-columns: 80px 1fr 120px 120px 120px 60px;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  align-items: center;
}

.table-header {
  background: rgba(255, 255, 255, 0.05);
  font-weight: 600;
  color: #f5f5f5;
  font-size: var(--font-size-sm);
}

.table-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: var(--font-size-sm);
  color: #ccc;
  transition: background 0.3s ease;
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.table-row:last-child {
  border-bottom: none;
}

.positive {
  color: #4caf50;
}

.negative {
  color: #f44336;
}

.neutral {
  color: #9e9e9e;
}

.edit-btn {
  background: rgba(255, 111, 97, 0.2);
  border: none;
  color: #ff6f61;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: rgba(255, 111, 97, 0.3);
  transform: scale(1.1);
}

.edit-btn i {
  font-size: var(--font-size-sm);
}

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
  .summary-cards {
    grid-template-columns: 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }

  .table-header span,
  .table-row span {
    padding: 0.25rem 0;
  }
}
</style> 