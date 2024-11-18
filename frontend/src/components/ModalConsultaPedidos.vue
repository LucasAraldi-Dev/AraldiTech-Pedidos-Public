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
          <button class="open-button" @click="openOrder(order)">ABRIR</button>
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
</template>

<script>
import axios from "axios";

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
}

/* Título do formulário */
.order-form h2 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.4rem;
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
}

/* Cabeçalho do card */
.order-header {
  display: flex;
  justify-content: center;
  width: 100%;
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
  text-align: left;
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

.open-button {
  background-color: #ff6f61;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.edit-button:hover {
  background-color: #e05545;
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

/* Responsividade para limitar cards no mobile */
@media (max-width: 768px) {
  .orders-list {
    grid-template-columns: 1fr 1fr; 
  }
}

@media (max-width: 480px) {
  .orders-list {
    grid-template-columns: 1fr;
  }

  .order-card {
    padding: 10px;
  }
}
</style>
