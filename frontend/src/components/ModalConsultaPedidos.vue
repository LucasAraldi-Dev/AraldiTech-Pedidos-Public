<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="order-form" @click.stop>
      <h2>CONSULTAR PEDIDOS</h2>

      <!-- Filtro de Status -->
      <div class="filter">
        <label for="statusFilter">Status</label>
        <select v-model="statusFilter" id="statusFilter">
          <option value="PENDENTE">PENDENTE</option>
          <option value="CONCLUIDO">CONCLUÍDO</option>
          <option value="CANCELADO">CANCELADO</option>
        </select>
      </div>

      <!-- Cards dos Pedidos -->
      <div class="orders-list">
        <div v-for="order in currentOrders" :key="order.id" class="order-card">
          <div class="order-header">
            <span class="order-id">#{{ order.id }}</span>
          </div>
          <h3 class="order-title">{{ order.descricao }}</h3>
          <div class="order-details">
            <p><strong>Quantidade:</strong> {{ order.quantidade }}</p>
            <p><strong>Categoria:</strong> {{ order.categoria }}</p>
            <p><strong>Urgência:</strong> {{ order.urgencia }}</p>
            <p><strong>Entrega:</strong> {{ formatDate(order.deliveryDate) }}</p>
            <p><strong>Observação:</strong> {{ order.observacao || "Nenhuma observação" }}</p>
            <p><strong>Usuário:</strong> {{ order.usuario_nome }}</p>
          </div>
          <div class="order-actions">
            <button class="open-button" @click="openOrder(order)">ABRIR</button>
            <button class="edit-button" @click="editOrder(order)">EDITAR</button>
            <button v-if="order.status.toUpperCase() === 'PENDENTE'" class="complete-button" @click="showConfirmModal(order)">CONCLUIR</button>
          </div>
        </div>
      </div>

      <!-- Paginação -->
      <div class="pagination">
        <button :disabled="currentPage === 1" @click="previousPage">Anterior</button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="nextPage">Próximo</button>
      </div>

      <!-- Botão Fechar -->
      <button class="close-btn" @click="closeForm">FECHAR</button>
    </div>
  </div>
  
  <!-- Modal de Confirmação para Concluir Pedido -->
  <div v-if="showConfirmation" class="confirm-modal-overlay" @click.self="cancelConfirmation">
    <div class="confirm-modal">
      <h3>Confirmar Conclusão do Pedido</h3>
      <div class="confirm-order-details" v-if="selectedOrder">
        <div class="confirm-order-header">
          <span class="confirm-order-id">#{{ selectedOrder.id }}</span>
        </div>
        <h4 class="confirm-order-title">{{ selectedOrder.descricao }}</h4>
        <div class="confirm-order-info">
          <p><strong>Quantidade:</strong> {{ selectedOrder.quantidade }}</p>
          <p><strong>Categoria:</strong> {{ selectedOrder.categoria }}</p>
          <p><strong>Urgência:</strong> {{ selectedOrder.urgencia }}</p>
          <p><strong>Entrega:</strong> {{ formatDate(selectedOrder.deliveryDate) }}</p>
          <p><strong>Usuário:</strong> {{ selectedOrder.usuario_nome }}</p>
        </div>
      </div>
      <p class="confirm-message">Tem certeza que deseja concluir este pedido?</p>
      <div class="confirm-buttons">
        <button class="confirm-yes" @click="confirmComplete">CONFIRMAR</button>
        <button class="confirm-no" @click="cancelConfirmation">CANCELAR</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  props: {
    isOpen: Boolean,
    onClose: Function,
  },
  data() {
    return {
      statusFilter: "PENDENTE",
      currentPage: 1,
      orders: [],
      toast: useToast(),
      showConfirmation: false,
      selectedOrder: null,
    };
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => order.status.toUpperCase() === this.statusFilter.toUpperCase());
    },
    totalPages() {
      const ordersPerPage = this.getOrdersPerPage();
      return Math.ceil(this.filteredOrders.length / ordersPerPage);
    },
    currentOrders() {
      const startIndex = (this.currentPage - 1) * this.getOrdersPerPage();
      return this.filteredOrders.slice(startIndex, startIndex + this.getOrdersPerPage());
    },
  },
  methods: {
    fetchOrders() {
      axios
        .get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        })
        .then(response => {
          this.orders = response.data;
        })
        .catch(error => console.error("Erro ao buscar pedidos:", error));
    },
    openOrder(order) {
      this.$emit("open-order", order);
    },
    editOrder(order) {
      this.$emit("edit-order", order);
    },
    closeForm() {
      this.$emit("close");
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    previousPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    getOrdersPerPage() {
      return window.innerWidth <= 768 ? 2 : 6;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    // Exibe o modal de confirmação com os detalhes do pedido
    showConfirmModal(order) {
      this.selectedOrder = order;
      this.showConfirmation = true;
    },
    
    // Cancela a confirmação e fecha o modal
    cancelConfirmation() {
      this.showConfirmation = false;
      this.selectedOrder = null;
    },
    
    // Confirma a conclusão do pedido após confirmação no modal
    confirmComplete() {
      if (!this.selectedOrder) return;
      
      // Preparar os dados para atualização
      const updateData = {
        ...this.selectedOrder,
        status: "CONCLUIDO"
      };
      
      // Enviar requisição para atualizar o status do pedido
      axios
        .put(`${process.env.VUE_APP_API_URL}/pedidos/${this.selectedOrder.id}`, updateData, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        })
        .then(() => {
          // Atualizar a lista de pedidos após concluir
          this.fetchOrders();
          // Fechar o modal de confirmação
          this.showConfirmation = false;
          this.selectedOrder = null;
          // Notificação estilizada com as cores do sistema
          this.toast.success("Pedido concluído com sucesso!", {
            toastClassName: "custom-toast-success",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close"
          });
        })
        .catch(error => {
          console.error("Erro ao concluir pedido:", error);
          // Notificação de erro estilizada
          this.toast.error("Erro ao concluir pedido. Por favor, tente novamente.", {
            toastClassName: "custom-toast-error",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close"
          });
        });
    },
  },
  created() {
    this.fetchOrders();
  },
};
</script>





<style scoped>
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
}

/* Estilos personalizados para os toasts */
:deep(.custom-toast-success) {
  background-color: #1f1f1f !important;
  border-left: 5px solid #ff6f61 !important;
  color: #f5f5f5 !important;
  font-size: 1.1rem !important;
}

:deep(.custom-toast-error) {
  background-color: #1f1f1f !important;
  border-left: 5px solid #e74c3c !important;
  color: #f5f5f5 !important;
  font-size: 1.1rem !important;
}

:deep(.custom-toast-body) {
  font-family: inherit !important;
  padding: 12px !important;
}

:deep(.custom-toast-close) {
  color: #ff6f61 !important;
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 25px; 
  border-radius: 10px;
  width: 100%;
  max-width: 900px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  font-size: 1.1rem;
}

/* Título do formulário */
.order-form h2 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 2.5rem;
  color: #ff6f61; 
}

/* Estilo dos campos do formulário */
.filter {
  margin-bottom: 20px;
}

.filter select {
  width: 100%;
  padding: 12px;
  border-radius: 5px;
  background-color: #333; 
  color: #f5f5f5;
}

/* Cards dos Pedidos */
.orders-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.order-card {
  background-color: #1f1f1f;
  color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  font-size: 1.1rem;
}

/* Cabeçalho do card */
.order-header {
  display: flex;
  justify-content: center;
  width: 100%;
  font-size: 1.5rem;
}

.order-id {
  font-size: 1.5em;
  color: #ff6f61; 
  font-weight: bold;
  text-align: center;
  flex: 1;
}

.order-title {
  font-size: 1.2em;
  color: #f5f5f5; 
  text-align: center;
  font-size: 1.3rem;
}

.view-attachment {
  background: transparent;
  border: none;
  color: #ff6f61;
  font-size: 1.5em;
  cursor: pointer;
}

.order-details {
  width: 100%;
}

.order-card p {
  font-size: 0.9em;
  color: #dfe6e9;
}

.order-actions {
  display: flex;
  gap: 10px; /* Espaçamento horizontal entre os botões */
  flex-wrap: wrap; /* Permite que os botões quebrem para a próxima linha em telas menores */
  width: 100%; /* Garante que ocupe toda a largura disponível */
  margin-top: 10px; /* Adiciona espaço acima dos botões */
}

.open-button,
.edit-button,
.complete-button {
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 1em;
}

.open-button,
.edit-button {
  background-color: #ff6f61;
}

.complete-button {
  background-color: #4CAF50;
}

.open-button:hover,
.edit-button:hover {
  background-color: #e55b55;
}

.complete-button:hover {
  background-color: #45a049;
}

/* Paginação */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.pagination button {
  background-color: #4f5b62;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

/* Botão de fechar pgn */
.close-btn {
  display: block;
  margin: 20px auto 0; 
  background: transparent;
  border: 2px solid #ff6f61;
  color: #ff6f61;
  font-size: 20px;
  padding: 12px 20px;
  padding-top: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #ff6f61;
  color: #1f1f1f;
}

/* Modal de Confirmação */
.confirm-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.9);
  z-index: 1100;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
}

.confirm-modal {
  background-color: #1f1f1f;
  color: #f5f5f5;
  padding: 25px;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  font-size: 1.1rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
}

.confirm-modal h3 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.8rem;
  color: #ff6f61;
}

.confirm-order-details {
  background-color: #2a2a2a;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.confirm-order-header {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 10px;
}

.confirm-order-id {
  font-size: 1.5em;
  color: #ff6f61;
  font-weight: bold;
  text-align: center;
}

.confirm-order-title {
  font-size: 1.2em;
  color: #f5f5f5;
  text-align: center;
  margin-bottom: 15px;
}

.confirm-order-info p {
  margin: 5px 0;
  font-size: 0.9em;
  color: #dfe6e9;
}

.confirm-message {
  text-align: center;
  font-size: 1.2rem;
  margin: 20px 0;
  color: #f5f5f5;
}

.confirm-buttons {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 20px;
}

.confirm-yes,
.confirm-no {
  flex: 1;
  padding: 12px 0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1rem;
  border: none;
  transition: all 0.3s ease;
}

.confirm-yes {
  background-color: #4CAF50;
  color: white;
}

.confirm-no {
  background-color: #ff6f61;
  color: white;
}

.confirm-yes:hover {
  background-color: #45a049;
}

.confirm-no:hover {
  background-color: #e55b55;
}

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .order-form {
    max-width: 90%;
    padding: 20px;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 15px;
  }
  
  .order-form h2 {
    font-size: 2rem;
  }
  
  .order-card {
    padding: 15px;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  
  .confirm-modal {
    max-width: 90%;
    padding: 20px;
  }
  
  .order-form h2 {
    font-size: 1.8rem;
  }
  
  .order-id {
    font-size: 1.3em;
  }
  
  .order-title {
    font-size: 1.1rem;
  }
  
  .order-card p {
    font-size: 0.85em;
  }
  
  .pagination {
    gap: 10px;
  }
  
  .pagination button {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .order-form {
    padding: 15px;
    max-width: 95%;
  }
  
  .orders-list {
    grid-template-columns: 1fr;
  }

  .order-card {
    padding: 10px;
  }
  
  .order-form h2 {
    font-size: 1.5rem;
    margin-bottom: 15px;
  }
  
  .order-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .open-button,
  .edit-button,
  .complete-button {
    width: 100%;
    margin-bottom: 5px;
    font-size: 0.9em;
    padding: 8px 12px;
  }
  
  .confirm-modal {
    padding: 15px;
  }
  
  .confirm-modal h3 {
    font-size: 1.4rem;
  }
  
  .confirm-buttons {
    flex-direction: column;
  }
  
  .confirm-yes,
  .confirm-no {
    width: 100%;
    margin-bottom: 8px;
  }
  
  .close-btn {
    font-size: 16px;
    padding: 10px 15px;
  }
}
</style>
