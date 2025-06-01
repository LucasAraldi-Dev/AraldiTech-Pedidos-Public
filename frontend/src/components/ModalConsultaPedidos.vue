<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeForm">
    <div class="order-form" @click.stop>
      <!-- Botão Fechar no canto superior direito -->
      <button class="close-btn-header" @click="closeForm">
        <i class="material-icons">close</i>
      </button>

      <div class="form-header">
        <h2>CONSULTAR PEDIDOS</h2>
        <div class="filters-container">
          <div class="filter-item">
            <label for="sectorFilter">
              <i class="material-icons">business</i>
              Setor:
            </label>
            <select v-model="sectorFilter" id="sectorFilter" :disabled="!isAdminOrGestor">
              <option value="TODOS">TODOS</option>
              <option value="Escritório">Escritório</option>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="CPO">CPO</option>
              <option value="Granjas">Granjas</option>
              <option value="Abatedouro">Abatedouro</option>
              <option value="Transporte">Transporte</option>
              <option value="Incubatório">Incubatório</option>
              <option value="Favorito">Favorito</option>
            </select>
          </div>
          <div class="filter-item">
            <label for="statusFilter">
              <i class="material-icons">filter_list</i>
              Status:
            </label>
            <select v-model="statusFilter" id="statusFilter">
              <option value="PENDENTE">PENDENTE</option>
              <option value="CONCLUÍDO">CONCLUÍDO</option>
              <option value="CANCELADO">CANCELADO</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Cards dos Pedidos -->
      <div class="orders-list">
        <div v-for="order in currentOrders" :key="order.id" class="order-card" :class="[getUrgencyClass(order.urgencia)]">
          <div class="order-header">
            <span class="order-id">#{{ order.id }}</span>
            <span class="urgency-badge" v-if="order.urgencia !== 'Padrão'">{{ order.urgencia }}</span>
          </div>
          <h3 class="order-title">{{ order.descricao }}</h3>
          <div class="order-details">
            <p>
              <i class="material-icons">format_list_numbered</i>
              <strong>Quantidade:</strong> {{ order.quantidade }}
            </p>
            <p>
              <i class="material-icons">category</i>
              <strong>Categoria:</strong> {{ order.categoria }}
            </p>
            <p>
              <i class="material-icons">priority_high</i>
              <strong>Urgência:</strong> {{ order.urgencia }}
            </p>
            <p>
              <i class="material-icons">business</i>
              <strong>Setor:</strong> {{ order.setor }}
            </p>
            <p>
              <i class="material-icons">event</i>
              <strong>Data do Pedido:</strong> {{ formatDate(order.deliveryDate) }}
            </p>
            <p v-if="order.status.toUpperCase() === 'CONCLUÍDO' && order.conclusao_data">
              <i class="material-icons">event_available</i>
              <strong>Concluído em:</strong> {{ formatDate(order.conclusao_data) }}
            </p>
            <p>
              <i class="material-icons">notes</i>
              <strong>Observação:</strong> {{ order.observacao || "Nenhuma observação" }}
            </p>
            <p>
              <i class="material-icons">person</i>
              <strong>Usuário:</strong> {{ order.usuario_nome }}
            </p>
          </div>
          <div class="order-actions">
            <!-- Botão Abrir para pedidos não concluídos -->
            <button 
              v-if="order.status.toUpperCase() !== 'CONCLUÍDO'" 
              class="open-button" 
              @click="openOrder(order)"
            >
              <i class="material-icons">visibility</i>
              ABRIR
            </button>
            
            <!-- Botão Detalhes para pedidos concluídos -->
            <button 
              v-if="order.status.toUpperCase() === 'CONCLUÍDO'" 
              class="details-button" 
              @click="openCompletedDetailsModal(order)"
            >
              <i class="material-icons">assignment_turned_in</i>
              DETALHES
            </button>
            
            <!-- Botão Editar - apenas para admin ou criador do pedido -->
            <button 
              v-if="isAdmin || canEditOrder(order)" 
              class="edit-button" 
              @click="editOrder(order)"
            >
              <i class="material-icons">edit</i>
              EDITAR
            </button>
            <button 
              v-if="order.status.toUpperCase() === 'PENDENTE' && (isAdminOrGestor || canCompleteOrder(order))" 
              class="complete-button" 
              @click="openCompletionModal(order)"
            >
              <i class="material-icons">check_circle</i>
              CONCLUIR
            </button>
          </div>
        </div>
      </div>

      <!-- Barra de paginação fixa -->
      <div class="fixed-pagination">
        <div class="pagination">
          <button :disabled="currentPage === 1" @click="previousPage">
            <i class="material-icons">navigate_before</i>
            Anterior
          </button>
          <span>Página {{ currentPage }} de {{ totalPages }}</span>
          <button :disabled="currentPage === totalPages" @click="nextPage">
            Próximo
            <i class="material-icons">navigate_next</i>
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Modal de Conclusão de Pedido -->
  <ModalConclusaoPedido
    :isOpen="showCompletionModal"
    :pedido="selectedOrder"
    @close="closeCompletionModal"
    @completed="onOrderCompleted"
  />

  <!-- Modal de Detalhes do Pedido Concluído -->
  <ModalPedidoConcluido
    :isOpen="showCompletedDetailsModal"
    :pedido="selectedOrder"
    @close="closeCompletedDetailsModal"
  />
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";
import ModalConclusaoPedido from "./ModalConclusaoPedido.vue";
import ModalPedidoConcluido from "./ModalPedidoConcluido.vue";

export default {
  components: {
    ModalConclusaoPedido,
    ModalPedidoConcluido
  },
  props: {
    isOpen: Boolean,
    onClose: Function,
  },
  data() {
    return {
      statusFilter: "PENDENTE",
      sectorFilter: "TODOS",
      currentPage: 1,
      orders: [],
      toast: useToast(),
      showCompletionModal: false,
      showCompletedDetailsModal: false,
      selectedOrder: null,
      userType: null,
      userSector: null,
      userName: null,
    };
  },
  computed: {
    isAdmin() {
      return this.userType === "admin";
    },
    isAdminOrGestor() {
      return this.userType === "admin" || this.userType === "gestor";
    },
    filteredOrders() {
      return this.orders.filter(order => {
        const statusMatch = order.status.toUpperCase() === this.statusFilter.toUpperCase();
        // Verificar correspondência de setor, incluindo possíveis variações de capitalização
        const sectorMatch = this.sectorFilter === "TODOS" || 
                            order.setor === this.sectorFilter || 
                            order.setor?.toLowerCase() === this.sectorFilter?.toLowerCase();
        
        return statusMatch && sectorMatch;
      });
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
    sanitizeHtml(text) {
      if (!text) return '';
      return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    },
    fetchOrders() {
      // Garantir que os dados do usuário foram carregados antes de buscar pedidos
      this.loadUserData();
      
      axios
        .get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        })
        .then(response => {
          this.orders = response.data;
          console.log(`Pedidos carregados: ${this.orders.length}, Filtro de setor: ${this.sectorFilter}, Tipo de usuário: ${this.userType}`);
          
          if (this.orders.length > 0) {
            // Log para depuração dos setores disponíveis
            const setores = [...new Set(this.orders.map(order => order.setor))];
            console.log(`Setores encontrados nos pedidos: ${setores.join(', ')}`);
          }
          
          // Ordenar os pedidos por prioridade (Crítico > Urgente > Padrão)
          this.orders.sort((a, b) => this.getUrgencyPriority(b.urgencia) - this.getUrgencyPriority(a.urgencia));
          
          // Validar se temos pedidos após aplicar os filtros
          setTimeout(() => {
            console.log(`Pedidos filtrados: ${this.filteredOrders.length} para o setor: ${this.sectorFilter}`);
            
            // Se não houver pedidos filtrados e o usuário não é admin/gestor, tenta ajustar o filtro
            if (this.filteredOrders.length === 0 && !this.isAdminOrGestor && this.orders.length > 0) {
              const setores = [...new Set(this.orders.map(order => order.setor))];
              
              if (setores.length === 1) {
                // Se só há um setor nos pedidos, use-o
                this.sectorFilter = setores[0];
                console.log(`Ajustando filtro para o único setor disponível: ${this.sectorFilter}`);
              } else if (this.userSector) {
                // Tenta encontrar o setor do usuário nos pedidos
                const setorProximo = setores.find(s => 
                  s.toLowerCase().includes(this.userSector.toLowerCase()) || 
                  this.userSector.toLowerCase().includes(s.toLowerCase())
                );
                
                if (setorProximo) {
                  this.sectorFilter = setorProximo;
                  console.log(`Ajustando filtro para o setor aproximado: ${this.sectorFilter}`);
                }
              }
            }
          }, 100);
        })
        .catch(error => {
          console.error("Erro ao buscar pedidos:", error);
          this.toast.error("Erro ao buscar pedidos. Verifique sua conexão.", {
            toastClassName: "custom-toast-error",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close"
          });
        });
    },
    getUrgencyPriority(urgencia) {
      switch(urgencia) {
        case 'Crítico': return 3;
        case 'Urgente': return 2;
        case 'Padrão': return 1;
        default: return 0;
      }
    },
    getUrgencyClass(urgencia) {
      switch(urgencia) {
        case 'Crítico': return 'urgency-critical';
        case 'Urgente': return 'urgency-urgent';
        default: return '';
      }
    },
    openOrder(order) {
      console.log(`ModalConsultaPedidos: Emitindo evento open-order com pedidoId: ${order.id}`);
      this.$emit("open-order", order.id);
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
      if (!date) return 'Data não informada';
      
      try {
        const d = new Date(date);
        
        // Verificar se a data é válida
        if (isNaN(d.getTime())) {
          console.warn(`Data inválida: ${date}`);
          return 'Data inválida';
        }
        
        return d.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
      } catch (error) {
        console.error(`Erro ao formatar data: ${date}`, error);
        return 'Erro de formato';
      }
    },
    // Abre o modal de conclusão de pedido
    openCompletionModal(order) {
      this.selectedOrder = order;
      this.showCompletionModal = true;
      
      console.log(`Abrindo modal de conclusão para o pedido #${order.id}`);
    },
    
    // Fecha o modal de conclusão
    closeCompletionModal() {
      this.showCompletionModal = false;
      this.selectedOrder = null;
    },
    
    // Callback quando o pedido é concluído com sucesso
    onOrderCompleted(updatedOrder) {
      console.log("Pedido concluído:", updatedOrder);
      // Atualizar a lista de pedidos
      this.fetchOrders();
      // Fechar o modal
      this.closeCompletionModal();
    },

    // Abre o modal de detalhes do pedido concluído
    openCompletedDetailsModal(order) {
      this.selectedOrder = order;
      this.showCompletedDetailsModal = true;
      
      console.log(`Abrindo modal de detalhes para o pedido concluído #${order.id}`);
    },
    
    // Fecha o modal de detalhes do pedido concluído
    closeCompletedDetailsModal() {
      this.showCompletedDetailsModal = false;
      this.selectedOrder = null;
    },

    loadUserData() {
      // Carregar dados do usuário do localStorage
      const userStr = localStorage.getItem("user");
      if (userStr) {
        try {
          const userObj = JSON.parse(userStr);
          this.userType = userObj.tipo_usuario;
          this.userSector = userObj.setor;
          this.userName = userObj.nome || userObj.username;
          
          console.log(`Dados do usuário carregados - Tipo: ${this.userType}, Setor: ${this.userSector}, Nome: ${this.userName}`);
          
          // Para usuário comum, o filtro de setor deve mostrar apenas o seu setor
          if (this.userType !== "admin" && this.userType !== "gestor") {
            if (this.userSector) {
              this.sectorFilter = this.userSector;
              console.log(`Filtro de setor definido para: ${this.sectorFilter}`);
            } else {
              console.warn("Usuário comum sem setor definido!");
            }
          }
          
        } catch (e) {
          console.error("Erro ao parsear dados do usuário:", e);
        }
      } else {
        console.warn("Nenhum dado de usuário encontrado no localStorage");
      }
    },
    canCompleteOrder(order) {
      // Verifica se o usuário atual é o criador do pedido
      // Obtém dados do usuário atual
      const userStr = localStorage.getItem("user");
      if (!userStr) return false;
      
      try {
        const userObj = JSON.parse(userStr);
        const userId = userObj.id;
        const userName = userObj.nome || userObj.username;
        
        // Caso o pedido não tenha ID de usuário, compare pelo nome
        if (!order.usuario_id) {
          console.log(`Pedido ${order.id} não tem ID de usuário, comparando pelo nome: ${userName} vs ${order.usuario_nome}`);
          return order.usuario_nome === userName;
        }
        
        console.log(`Verificando permissão - Usuário atual: ${userId}/${userName}, Criador do pedido: ${order.usuario_id}/${order.usuario_nome}`);
        
        // Compara o ID do usuário ou o nome do usuário com o do pedido
        return (
          order.usuario_id === userId || 
          order.usuario_nome === userName
        );
      } catch (e) {
        console.error("Erro ao verificar permissão para concluir pedido:", e);
        return false;
      }
    },
    canEditOrder(order) {
      // Verifica se o usuário atual é o criador do pedido
      // Obtém dados do usuário atual
      const userStr = localStorage.getItem("user");
      if (!userStr) return false;
      
      try {
        const userObj = JSON.parse(userStr);
        const userId = userObj.id;
        const userName = userObj.nome || userObj.username;
        
        // Caso o pedido não tenha ID de usuário, compare pelo nome
        if (!order.usuario_id) {
          console.log(`Pedido ${order.id} - Verificando edição sem ID de usuário: ${userName} vs ${order.usuario_nome}`);
          return order.usuario_nome === userName;
        }
        
        console.log(`Verificando permissão de edição - Usuário atual: ${userId}/${userName}, Criador do pedido: ${order.usuario_id}/${order.usuario_nome}`);
        
        // Compara o ID do usuário ou o nome do usuário com o do pedido
        return (
          order.usuario_id === userId || 
          order.usuario_nome === userName
        );
      } catch (e) {
        console.error("Erro ao verificar permissão para editar pedido:", e);
        return false;
      }
    }
  },
  watch: {
    // Observar quando o modal é aberto para recarregar os dados
    isOpen(newValue) {
      if (newValue) {
        this.loadUserData();
        this.fetchOrders();
      }
    },
    // Resetar para a primeira página quando o filtro for alterado
    statusFilter() {
      this.currentPage = 1;
    },
    // Resetar para a primeira página quando o filtro de setor for alterado
    sectorFilter() {
      this.currentPage = 1;
    }
  },
  created() {
    // Não precisa chamar loadUserData aqui, pois já estamos chamando dentro de fetchOrders
    this.fetchOrders();
  },
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
  padding-bottom: 50px; /* Espaço para a barra de paginação fixa */
  box-sizing: border-box;
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
  width: 95%;
  max-width: 1200px;
  padding-bottom: 60px; /* Espaço reduzido para a barra de paginação */
  border-radius: 10px;
  position: relative;
  text-transform: none;
  font-size: 1.1rem;
  overflow-y: auto;
  max-height: 90vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

/* Botão Fechar no Cabeçalho */
.close-btn-header {
  position: absolute;
  top: 15px;
  right: 15px;
  background: transparent;
  border: 2px solid #ff6f61;
  color: #ff6f61;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.close-btn-header:hover {
  background-color: #ff6f61;
  color: #1f1f1f;
  transform: scale(1.1);
}

.close-btn-header i {
  font-size: 20px;
}

/* Cabeçalho do formulário */
.form-header {
  margin-bottom: 25px;
  border-bottom: 1px solid #333;
  padding-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

/* Título do formulário */
.form-header h2 {
  color: #ff6f61;
  font-size: 1.4rem;
  margin: 0;
}

/* Container de filtros */
.filters-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-item {
  display: flex;
  align-items: center;
  background-color: #333;
  padding: 5px 10px;
  border-radius: 5px;
}

.filter-item label {
  display: flex;
  align-items: center;
  color: #999;
  margin-right: 10px;
}

.filter-item label i {
  margin-right: 5px;
  color: #ff6f61;
  font-size: 18px;
}

.filter-item select {
  background-color: #444;
  color: #f5f5f5;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 0.9rem;
}

.filter-item select:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Cards dos Pedidos */
.orders-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
  margin-bottom: 30px; /* Espaço suficiente para não ser coberto pela barra fixa */
}

.order-card {
  background-color: #2a2a2a;
  color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  font-size: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #333;
  position: relative;
}

.order-card:hover {
  transform: translateY(-3px);
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.4);
}

/* Classes de urgência para cards */
.urgency-critical {
  border: 2px solid #e74c3c;
  box-shadow: 0 0 10px rgba(231, 76, 60, 0.3);
}

.urgency-urgent {
  border: 2px solid #f39c12;
  box-shadow: 0 0 10px rgba(243, 156, 18, 0.3);
}

.urgency-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.urgency-critical .urgency-badge {
  background-color: #e74c3c;
}

.urgency-urgent .urgency-badge {
  background-color: #f39c12;
}

/* Cabeçalho do card */
.order-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 1.5rem;
}

.order-id {
  font-size: 1.5em;
  color: #ff6f61; 
  font-weight: bold;
  text-align: left;
}

.order-title {
  font-size: 1.3rem;
  color: #f5f5f5; 
  text-align: center;
  width: 100%;
  margin: 5px 0 10px;
  border-bottom: 1px solid #444;
  padding-bottom: 8px;
}

.order-details {
  width: 100%;
}

.order-details p {
  font-size: 0.9rem;
  color: #dfe6e9;
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.order-details p i {
  margin-right: 8px;
  color: #ff6f61;
  font-size: 16px;
}

.order-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  width: 100%;
  margin-top: 15px;
  justify-content: space-between;
}

.open-button,
.edit-button,
.complete-button,
.details-button {
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.open-button i,
.edit-button i,
.complete-button i,
.details-button i {
  margin-right: 5px;
  font-size: 16px;
}

.open-button {
  background-color: #3498db;
}

.edit-button {
  background-color: #ff6f61;
}

.complete-button {
  background-color: #4CAF50;
}

.details-button {
  background-color: #27ae60;
}

.open-button:hover {
  background-color: #2980b9;
}

.edit-button:hover {
  background-color: #e55b55;
}

.complete-button:hover {
  background-color: #45a049;
}

.details-button:hover {
  background-color: #229954;
}

/* Barra de paginação fixa */
.fixed-pagination {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #1f1f1f;
  border-top: 1px solid #333;
  z-index: 1001;
  padding: 6px 15px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Paginação */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
}

.pagination button {
  background-color: #444;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  min-height: 30px;
}

.pagination button i {
  font-size: 18px;
}

.pagination button:disabled {
  background-color: #333;
  cursor: not-allowed;
  opacity: 0.5;
}

.pagination button:not(:disabled):hover {
  background-color: #555;
  transform: translateY(-1px);
}

.pagination span {
  color: #ddd;
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0 6px;
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
  padding: 15px;
  box-sizing: border-box;
  overflow-y: auto; /* Permitir rolagem caso o conteúdo seja grande */
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
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  max-height: 90vh; /* Altura máxima para não estourar a tela */
  overflow-y: auto; /* Adicionar rolagem se necessário */
  margin: auto; /* Centralizar horizontalmente */
}

.confirm-modal h3 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.8rem;
  color: #ff6f61;
  border-bottom: 1px solid #333;
  padding-bottom: 10px;
}

.confirm-order-details {
  background-color: #2a2a2a;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #333;
  word-break: break-word;
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
  border-bottom: 1px solid #444;
  padding-bottom: 8px;
  word-wrap: break-word;
}

.confirm-order-info p {
  margin: 8px 0;
  font-size: 0.9rem;
  color: #dfe6e9;
  display: flex;
  align-items: flex-start;
  flex-wrap: wrap;
}

.confirm-order-info p i {
  margin-right: 8px;
  color: #ff6f61;
  font-size: 16px;
  min-width: 18px;
}

.completion-date-container {
  margin: 15px 0 20px;
  padding: 15px;
  background-color: #2a2a2a;
  border-radius: 8px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  border: 1px solid #333;
}

.completion-date-container label {
  display: flex;
  align-items: center;
  color: #f5f5f5;
  font-weight: bold;
  margin-right: 10px;
  min-width: 150px;
}

.completion-date-container label i {
  margin-right: 8px;
  color: #ff6f61;
  font-size: 18px;
}

.completion-date-container input {
  background-color: #333;
  color: #f5f5f5;
  border: 1px solid #444;
  padding: 8px 15px;
  border-radius: 5px;
  font-size: 1rem;
  flex: 1;
  min-width: 200px;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 100%;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
}

.completion-date-container input:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 111, 97, 0.2);
}

/* Estilização específica para calendários em dispositivos móveis */
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  opacity: 0.8;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: 10px;
  padding: 4px;
  background-color: rgba(255, 111, 97, 0.1);
  border-radius: 3px;
}

input[type="date"]::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
  background-color: rgba(255, 111, 97, 0.2);
}

@media (max-width: 480px) {
  input[type="date"]::-webkit-calendar-picker-indicator {
    width: 24px;
    height: 24px;
    padding: 5px;
  }
}

.date-helper-text {
  font-size: 0.85rem;
  color: #aaa;
  margin-top: 8px;
  width: 100%;
  padding: 5px 10px;
  background-color: #2a2a2a;
  border-radius: 5px;
  display: flex;
  align-items: flex-start;
}

.date-helper-text .info-icon {
  color: #ff6f61;
  font-size: 16px;
  margin-right: 8px;
  margin-top: 2px;
  flex-shrink: 0;
}

.confirm-message {
  text-align: center;
  font-size: 1.2rem;
  margin: 20px 0;
  color: #f5f5f5;
  background-color: #333;
  padding: 10px;
  border-radius: 5px;
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
  font-size: 1rem;
  border: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  -webkit-tap-highlight-color: transparent; /* Remover highlight em dispositivos touch */
  touch-action: manipulation; /* Melhorar resposta ao toque */
}

.confirm-yes i,
.confirm-no i {
  margin-right: 8px;
  font-size: 18px;
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

/* Adicionar estados ativos para melhor feedback em dispositivos touch */
.confirm-yes:active {
  background-color: #3d8b40;
  transform: translateY(1px);
}

.confirm-no:active {
  background-color: #cc5a4e;
  transform: translateY(1px);
}

/* Aumentar área clicável para dispositivos touch */
@media (pointer: coarse) {
  .confirm-yes,
  .confirm-no {
    padding: 14px 0;
    min-height: 50px;
  }
  
  .completion-date-container input {
    min-height: 44px; /* Altura mínima para facilitar toque */
  }
  
  /* Aumentar espaçamento vertical entre elementos para evitar toques acidentais */
  .confirm-order-info p {
    padding: 4px 0;
  }
}

/* Responsividade para diferentes dispositivos */

/* Telas de 13-14 polegadas (1366x768, 1440x900) */
@media (max-width: 1440px) and (max-height: 900px) {
  .order-form {
    width: 92%;
    max-width: 1100px;
    padding: 20px;
    max-height: 85vh;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 18px;
  }
  
  .order-card {
    padding: 18px;
  }
  
  .fixed-pagination {
    padding: 5px 15px;
  }
  
  .pagination button {
    padding: 4px 8px;
    font-size: 0.8rem;
    min-height: 28px;
  }
}

/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .order-form {
    width: 90%;
    max-width: 950px;
    padding: 18px;
    max-height: 82vh;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
  
  .form-header h2 {
    font-size: 1.3rem;
  }
  
  .order-card {
    padding: 16px;
  }
  
  .filters-container {
    margin-top: 15px;
    width: 100%;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .fixed-pagination {
    padding: 5px 15px;
  }
  
  .pagination {
    gap: 12px;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .order-form {
    width: 95%;
    max-width: 100%;
    padding: 15px;
    max-height: 85vh;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 15px;
  }
  
  .confirm-modal {
    width: 95%;
    max-width: 100%;
    padding: 18px;
  }
  
  .filter-item {
    width: 100%;
    justify-content: space-between;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
  }
  
  .order-id {
    font-size: 1.3em;
  }
  
  .order-title {
    font-size: 1.1rem;
  }
  
  .order-card p {
    font-size: 0.9rem;
  }
  
  .fixed-pagination {
    padding: 5px 15px;
  }
  
  .pagination {
    gap: 8px;
  }
  
  .pagination button {
    padding: 4px 8px;
    font-size: 0.8rem;
    min-height: 28px;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal-overlay,
  .confirm-modal-overlay {
    padding: 8px;
    align-items: flex-start;
    overflow-y: auto;
    padding-bottom: 45px; /* Espaço para a barra fixa */
  }
  
  .close-btn-header {
    top: 10px;
    right: 10px;
    width: 35px;
    height: 35px;
  }
  
  .close-btn-header i {
    font-size: 18px;
  }
  
  .order-form {
    padding: 12px;
    width: 100%;
    max-width: 100%;
    max-height: calc(100vh - 45px); /* Altura ajustada para a barra fixa */
    margin-top: 10px;
  }
  
  .orders-list {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .order-card {
    padding: 12px;
  }
  
  .form-header h2 {
    font-size: 1.05rem;
  }
  
  .order-actions {
    flex-direction: column;
    width: 100%;
    gap: 8px;
  }
  
  .open-button,
  .edit-button,
  .complete-button,
  .details-button {
    width: 100%;
    font-size: 0.85rem;
    padding: 10px 12px;
    min-height: 42px;
  }
  
  .fixed-pagination {
    padding: 4px 10px;
  }
  
  .pagination {
    gap: 6px;
    flex-wrap: wrap;
  }
  
  .pagination button {
    padding: 6px 8px;
    font-size: 0.75rem;
    min-height: 32px;
  }
  
  .pagination span {
    font-size: 0.75rem;
    order: -1;
    width: 100%;
    text-align: center;
    margin-bottom: 4px;
  }
  
  .confirm-modal {
    padding: 15px;
    margin: 10px;
    max-height: 85vh; /* Reduzir altura máxima para deixar espaço para rolagem */
    width: calc(100% - 20px); /* Garantir que o modal não ultrapasse a tela */
  }
  
  .confirm-modal h3 {
    font-size: 1.4rem;
    padding-bottom: 8px;
    margin-bottom: 15px;
  }
  
  .confirm-order-details {
    padding: 12px;
    margin-bottom: 15px;
  }
  
  .confirm-order-id {
    font-size: 1.3em;
  }
  
  .confirm-order-title {
    font-size: 1.1em;
    padding-bottom: 6px;
    margin-bottom: 10px;
  }
  
  .confirm-order-info p {
    font-size: 0.85rem;
    margin: 6px 0;
  }
  
  .completion-date-container {
    padding: 12px;
    margin: 12px 0;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .completion-date-container label {
    margin-bottom: 8px;
    width: 100%;
  }
  
  .completion-date-container input {
    width: 100%;
    min-width: 100%;
    padding: 10px;
    font-size: 16px; /* Tamanho mínimo para evitar zoom em dispositivos iOS */
  }
  
  .date-helper-text {
    font-size: 0.8rem;
    padding: 8px;
  }
  
  .confirm-message {
    font-size: 1.1rem;
    margin: 15px 0;
    padding: 8px;
  }
  
  .confirm-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .confirm-yes,
  .confirm-no {
    width: 100%;
    padding: 12px 0;
    margin: 0;
    font-size: 1rem;
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  
  .confirm-yes i,
  .confirm-no i {
    font-size: 20px; /* Ícones ligeiramente maiores em mobile */
  }
  
  .close-btn {
    font-size: 0.9rem;
    padding: 10px 15px;
    margin-top: 15px;
  }
  
  /* Ajuste para telas com teclado virtual ativo */
  @media (max-height: 450px) {
    .confirm-modal {
      max-height: 100vh;
      overflow-y: auto;
    }
    
    .confirm-modal-overlay {
      align-items: flex-start;
      padding-top: 5px;
    }
  }
  

}

/* Dispositivos móveis muito pequenos */
@media (max-width: 360px) {
  .order-form {
    padding: 10px;
    margin-top: 5px;
  }
  
  .form-header h2 {
    font-size: 1rem;
  }
  
  .order-card {
    padding: 10px;
  }
  
  .order-title {
    font-size: 1rem;
  }
  
  .order-details p {
    font-size: 0.8rem;
  }
  
  .fixed-pagination {
    padding: 4px 8px;
  }
  
  .pagination button {
    padding: 4px 6px;
    font-size: 0.7rem;
    min-height: 28px;
  }
  
  .confirm-modal {
    padding: 12px;
    margin: 8px;
  }
  
  .confirm-modal h3 {
    font-size: 1.3rem;
  }
  
  .confirm-order-details {
    padding: 10px;
  }
  
  .confirm-order-info p {
    font-size: 0.8rem;
  }
  
  .completion-date-container {
    padding: 10px;
  }
  
  .date-helper-text {
    font-size: 0.75rem;
  }
  
  .confirm-message {
    font-size: 1rem;
  }
}

/* Ajustes específicos para notebooks de 13 polegadas (1280x800) */
@media screen and (max-width: 1280px) and (max-height: 800px) {
  .order-form {
    width: 90%;
    max-width: 1000px;
    padding: 16px;
    max-height: 80vh;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
  }
  
  .order-card {
    padding: 14px;
  }
  
  .fixed-pagination {
    padding: 5px 15px;
  }
}

/* Ajustes para notebooks de 14 polegadas (1366x768) */
@media screen and (max-width: 1366px) and (max-height: 768px) {
  .order-form {
    width: 88%;
    max-width: 1050px;
    padding: 18px;
    max-height: 78vh;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
  
  .order-card {
    padding: 16px;
  }
  
  .fixed-pagination {
    padding: 5px 15px;
  }
}

/* Ajustes para telas 720p */
@media (min-height: 720px) and (max-height: 768px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: 2vh;
  }
  
  .order-form {
    max-height: 82vh;
  }
}

/* Ajustes específicos para notebooks com zoom */
@media screen and (min-resolution: 1.25dppx) {
  .order-form {
    max-height: 85vh;
  }
  
  .orders-list {
    gap: 16px;
  }
  
  .fixed-navigation {
    padding: 10px 16px;
  }
}

/* Ajuste para telas muito pequenas onde a rolagem pode ser necessária */
@media (max-height: 640px) {
  .confirm-modal-overlay {
    align-items: flex-start; /* Alinhar ao topo para permitir rolagem */
    padding-top: 10px;
    padding-bottom: 10px;
  }
  
  .confirm-modal {
    margin-top: 10px;
    margin-bottom: 10px;
  }
}
</style>
