<template>
  <div v-if="isOpen" class="modal-financeiro">
    <div class="modal-content">
      <div class="modal-header">
        <h2 class="modal-title">
          <i class="material-icons">account_balance</i>
          Detalhes Financeiros
        </h2>
        <button class="close-btn" @click="$emit('close')">
          <i class="material-icons">close</i>
        </button>
      </div>
      
      <div class="modal-body">
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Carregando dados financeiros...</p>
        </div>
        <div v-else>
          <!-- Resumo financeiro detalhado -->
          <div class="financial-overview">
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
                <i class="material-icons kpi-icon" :class="saldoIconClass">{{ saldoIcon }}</i>
                <div class="kpi-content">
                  <h3>{{ saldoLabel }}</h3>
                  <div class="kpi-value">
                    R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}
                    <span class="trend-indicator">
                      <i class="material-icons trend-icon">{{ saldoTrendIcon }}</i>
                      {{ saldoPercentage }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Progresso do orçamento -->
            <div class="budget-progress-container">
              <h3>Consumo do Orçamento</h3>
              <div class="budget-progress">
                <div class="progress-bar" :style="{ width: progressPercentage + '%' }" :class="progressClass"></div>
              </div>
              <div class="progress-labels">
                <span>{{ progressPercentage }}% utilizado</span>
                <span>Meta: 100%</span>
              </div>
            </div>
          </div>
          
          <!-- Tabela dos últimos pedidos com informações financeiras -->
          <div class="financial-table-container">
            <h3>
              <i class="material-icons">list_alt</i>
              Pedidos com Dados Financeiros
            </h3>
            <table class="financial-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Descrição</th>
                  <th>Orçamento</th>
                  <th>Custo Real</th>
                  <th>Diferença</th>
                  <th>Status</th>
                  <th>Ação</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="pedidosComFinancas.length === 0">
                  <td colspan="7" class="empty-cell">
                    <i class="material-icons empty-icon">info</i>
                    Nenhum pedido com dados financeiros encontrado
                  </td>
                </tr>
                <tr v-for="pedido in pedidosComFinancas" :key="pedido.id" :class="{'highlight-row': isOverBudget(pedido)}">
                  <td>#{{ pedido.id }}</td>
                  <td class="description-cell">{{ truncateText(pedido.descricao, 30) }}</td>
                  <td>R$ {{ formatCurrency(pedido.orcamento_previsto) }}</td>
                  <td>R$ {{ formatCurrency(pedido.custo_real) }}</td>
                  <td :class="getDiffClass(pedido.orcamento_previsto - pedido.custo_real)">
                    <span class="diff-value">
                      <i class="material-icons diff-icon">{{ getDiffIcon(pedido.orcamento_previsto - pedido.custo_real) }}</i>
                      R$ {{ formatCurrency(Math.abs(pedido.orcamento_previsto - pedido.custo_real)) }}
                    </span>
                  </td>
                  <td>
                    <span class="status-badge" :class="getStatusClass(pedido.status)">
                      {{ pedido.status }}
                    </span>
                  </td>
                  <td>
                    <button class="edit-btn" @click="editPedido(pedido)">
                      <i class="material-icons">edit</i>
                      Editar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Dicas para melhorar a gestão financeira -->
          <div class="financial-tips" v-if="showTips">
            <h3>
              <i class="material-icons">lightbulb</i>
              Dicas para Gestão Financeira
            </h3>
            <ul class="tips-list">
              <li v-if="custoRealTotal > orcamentoTotal">
                <i class="material-icons tip-icon">warning</i>
                <span>Os custos reais estão excedendo o orçamento em {{ percentageOver }}%. Considere revisar seus gastos.</span>
              </li>
              <li v-else>
                <i class="material-icons tip-icon">thumb_up</i>
                <span>Seu projeto está dentro do orçamento. Continue monitorando os custos.</span>
              </li>
              <li v-if="pedidosComFinancas.filter(p => p.status === 'Pendente' && p.orcamento_previsto > 0).length > 0">
                <i class="material-icons tip-icon">assignment</i>
                <span>Existem {{ pedidosComFinancas.filter(p => p.status === 'Pendente' && p.orcamento_previsto > 0).length }} pedidos pendentes com orçamento alocado.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import authService from '@/api/authService';

export default {
  name: "ModalFinanceiro",
  emits: ['close'],
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      pedidos: [],
      isLoading: true,
      orcamentoTotal: 0,
      custoRealTotal: 0,
      saldoFinanceiro: 0,
      showTips: true
    };
  },
  computed: {
    pedidosComFinancas() {
      return this.pedidos
        .filter(p => parseFloat(p.orcamento_previsto || 0) > 0 || parseFloat(p.custo_real || 0) > 0)
        .sort((a, b) => parseFloat(b.orcamento_previsto || 0) - parseFloat(a.orcamento_previsto || 0));
    },
    saldoClass() {
      return this.saldoFinanceiro >= 0 ? 'positive-balance' : 'negative-balance';
    },
    saldoIcon() {
      return this.saldoFinanceiro >= 0 ? 'savings' : 'money_off';
    },
    saldoIconClass() {
      return this.saldoFinanceiro >= 0 ? 'economy-icon' : 'deficit-icon';
    },
    saldoLabel() {
      return this.saldoFinanceiro >= 0 ? 'Economia' : 'Déficit';
    },
    saldoTrendIcon() {
      return this.saldoFinanceiro >= 0 ? 'trending_up' : 'trending_down';
    },
    saldoPercentage() {
      if (this.orcamentoTotal === 0) return 0;
      return Math.abs(Math.round((this.saldoFinanceiro / this.orcamentoTotal) * 100));
    },
    progressPercentage() {
      if (this.orcamentoTotal === 0) return 0;
      const percentage = Math.round((this.custoRealTotal / this.orcamentoTotal) * 100);
      return Math.min(percentage, 100); // Limitar a 100% para visualização
    },
    progressClass() {
      if (this.progressPercentage < 70) return 'progress-good';
      if (this.progressPercentage < 90) return 'progress-warning';
      return 'progress-danger';
    },
    percentageOver() {
      if (this.orcamentoTotal === 0) return 0;
      return Math.round(((this.custoRealTotal - this.orcamentoTotal) / this.orcamentoTotal) * 100);
    }
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.fetchPedidos();
      }
    }
  },
  mounted() {
    if (this.isOpen) {
      this.fetchPedidos();
    }
  },
  methods: {
    async fetchPedidos() {
      this.isLoading = true;
      
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: authService.getAuthHeaders()
        });
        
        this.pedidos = response.data || [];
        
        // Calcular totais
        let orcamento = 0;
        let custo = 0;
        
        this.pedidos.forEach(pedido => {
          orcamento += parseFloat(pedido.orcamento_previsto || 0);
          custo += parseFloat(pedido.custo_real || 0);
        });
        
        this.orcamentoTotal = orcamento;
        this.custoRealTotal = custo;
        this.saldoFinanceiro = orcamento - custo;
      } catch (error) {
        console.error("Erro ao carregar dados financeiros:", error);
      } finally {
        this.isLoading = false;
      }
    },
    truncateText(text, maxLength) {
      if (!text) return '';
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    },
    formatCurrency(value) {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    getDiffClass(diff) {
      if (diff > 0) return 'positive-diff';
      if (diff < 0) return 'negative-diff';
      return '';
    },
    getDiffIcon(diff) {
      if (diff > 0) return 'arrow_drop_down';
      if (diff < 0) return 'arrow_drop_up';
      return 'remove';
    },
    getStatusClass(status) {
      switch (status) {
        case 'Concluído':
          return 'status-completed';
        case 'Pendente':
          return 'status-pending';
        case 'Cancelado':
          return 'status-canceled';
        default:
          return '';
      }
    },
    isOverBudget(pedido) {
      return parseFloat(pedido.custo_real || 0) > parseFloat(pedido.orcamento_previsto || 0);
    },
    editPedido(pedido) {
      this.$emit('edit-pedido', pedido.id);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

.modal-financeiro {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
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
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
  color: #f5f5f5;
  position: relative;
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

.modal-title {
  font-size: 24px;
  margin: 0;
  color: #f5f5f5;
  display: flex;
  align-items: center;
}

.modal-title i {
  margin-right: 15px;
  color: #ff6f61;
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

.modal-body {
  padding: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
  color: #ddd;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 111, 97, 0.3);
  border-radius: 50%;
  border-top-color: #ff6f61;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Resumo financeiro */
.financial-overview {
  margin-bottom: 30px;
}

.financial-kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.financial-kpi {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
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
  font-size: 36px;
  margin-right: 15px;
  color: #ff6f61;
}

.economy-icon {
  color: #2ecc71;
}

.deficit-icon {
  color: #e74c3c;
}

.kpi-content {
  flex: 1;
}

.financial-kpi h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #ddd;
}

.kpi-value {
  font-size: 24px;
  font-weight: bold;
  color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.trend-indicator {
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-left: 10px;
  padding: 3px 8px;
  border-radius: 12px;
  background-color: #333;
}

.trend-icon {
  font-size: 18px;
  margin-right: 5px;
}

.positive-balance .trend-indicator {
  background-color: rgba(46, 204, 113, 0.2);
  color: #2ecc71;
}

.positive-balance .kpi-value {
  color: #2ecc71;
}

.negative-balance .trend-indicator {
  background-color: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.negative-balance .kpi-value {
  color: #e74c3c;
}

/* Barra de progresso */
.budget-progress-container {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #333;
}

.budget-progress-container h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  color: #ff6f61;
  display: flex;
  align-items: center;
}

.budget-progress-container h3::before {
  content: 'trending_up';
  font-family: 'Material Icons';
  margin-right: 10px;
  font-size: 22px;
}

.budget-progress {
  height: 20px;
  background-color: #333;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s ease;
}

.progress-good {
  background-color: #2ecc71;
  background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent);
  background-size: 20px 20px;
  animation: progress-bar-stripes 1s linear infinite;
}

.progress-warning {
  background-color: #f39c12;
  background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent);
  background-size: 20px 20px;
  animation: progress-bar-stripes 1s linear infinite;
}

.progress-danger {
  background-color: #e74c3c;
  background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent);
  background-size: 20px 20px;
  animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
  from { background-position: 40px 0; }
  to { background-position: 0 0; }
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  color: #ddd;
  font-size: 14px;
}

/* Tabela financeira */
.financial-table-container {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #333;
}

.financial-table-container h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
  margin-top: 0;
  margin-bottom: 15px;
  color: #ff6f61;
  font-size: 18px;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.financial-table {
  width: 100%;
  border-collapse: collapse;
  color: #f5f5f5;
}

.financial-table th,
.financial-table td {
  padding: 12px 10px;
  text-align: left;
  border-bottom: 1px solid #333;
}

.financial-table th {
  background-color: #222;
  color: #ff6f61;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 1px;
}

.financial-table tr {
  transition: background-color 0.3s;
}

.financial-table tr:hover {
  background-color: #333;
}

.highlight-row {
  background-color: rgba(231, 76, 60, 0.1);
}

.highlight-row:hover {
  background-color: rgba(231, 76, 60, 0.2);
}

.description-cell {
  max-width: 250px;
}

.empty-cell {
  text-align: center;
  padding: 40px;
  color: #999;
  font-style: italic;
}

.empty-icon {
  font-size: 24px;
  margin-right: 10px;
  vertical-align: middle;
}

.diff-value {
  display: flex;
  align-items: center;
}

.diff-icon {
  margin-right: 5px;
  font-size: 20px;
}

.positive-diff {
  color: #2ecc71;
}

.negative-diff {
  color: #e74c3c;
}

.status-badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-completed {
  background-color: #2ecc71;
  color: white;
}

.status-pending {
  background-color: #f39c12;
  color: white;
}

.status-canceled {
  background-color: #e74c3c;
  color: white;
}

.edit-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #ff6f61;
  color: #1f1f1f;
  border: none;
  padding: 8px 12px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85em;
  font-weight: bold;
  transition: all 0.3s;
}

.edit-btn:hover {
  background-color: #e55b55;
  transform: translateY(-2px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.edit-btn i {
  font-size: 16px;
}

/* Dicas financeiras */
.financial-tips {
  background-color: #2a2a2a;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #333;
}

.financial-tips h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff6f61;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 18px;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.tips-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  margin-bottom: 10px;
  background-color: #333;
  border-radius: 8px;
  transition: transform 0.3s, background-color 0.3s;
  border: 1px solid #444;
}

.tips-list li:hover {
  transform: translateY(-2px);
  background-color: #3a3a3a;
  border-color: #ff6f61;
}

.tip-icon {
  font-size: 20px;
  margin-right: 10px;
  color: #ff6f61;
}

/* Responsividade */
@media (max-width: 992px) {
  .financial-kpis {
    grid-template-columns: 1fr 1fr;
  }
  
  .financial-kpi:last-child {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .financial-kpis {
    grid-template-columns: 1fr;
  }
  
  .financial-kpi:last-child {
    grid-column: auto;
  }
  
  .financial-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
  
  .financial-table th,
  .financial-table td {
    padding: 10px 8px;
    font-size: 0.9em;
  }
  
  .description-cell {
    max-width: 150px;
  }
}

@media (max-width: 480px) {
  .modal-body {
    padding: 15px;
  }
  
  .financial-kpi {
    padding: 15px;
  }
  
  .financial-table-container,
  .budget-progress-container,
  .financial-tips {
    padding: 15px;
  }
}
</style> 