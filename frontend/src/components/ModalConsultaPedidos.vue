<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeForm">
    <div class="order-form" @click.stop>
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
            <button class="open-button" @click="openOrder(order)">
              <i class="material-icons">visibility</i>
              ABRIR
            </button>
            <button class="edit-button" @click="editOrder(order)">
              <i class="material-icons">edit</i>
              EDITAR
            </button>
            <button 
              v-if="order.status.toUpperCase() === 'PENDENTE' && (isAdminOrGestor || canCompleteOrder(order))" 
              class="complete-button" 
              @click="showConfirmModal(order)"
            >
              <i class="material-icons">check_circle</i>
              CONCLUIR
            </button>
          </div>
        </div>
      </div>

      <!-- Paginação -->
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

      <!-- Botão Fechar -->
      <button class="close-btn" @click="closeForm">
        <i class="material-icons">close</i>
        FECHAR
      </button>
    </div>
  </div>
  
  <!-- Modal de Confirmação para Concluir Pedido -->
  <div v-if="showConfirmation" class="confirm-modal-overlay" @click.self="cancelConfirmation">
    <div class="confirm-modal">
      <h3>Confirmar Conclusão do Pedido</h3>
              <div class="confirm-order-details" v-if="selectedOrder">          <div class="confirm-order-header">            <span class="confirm-order-id">#{{ selectedOrder.id }}</span>          </div>          <h4 class="confirm-order-title">{{ sanitizeHtml(selectedOrder.descricao) }}</h4>          <div class="confirm-order-info">            <p>              <i class="material-icons">format_list_numbered</i>              <strong>Quantidade:</strong> {{ selectedOrder.quantidade }}            </p>            <p>              <i class="material-icons">category</i>              <strong>Categoria:</strong> {{ sanitizeHtml(selectedOrder.categoria) }}            </p>            <p>              <i class="material-icons">priority_high</i>              <strong>Urgência:</strong> {{ sanitizeHtml(selectedOrder.urgencia) }}            </p>            <p>              <i class="material-icons">event</i>              <strong>Data do Pedido:</strong> {{ formatDate(selectedOrder.deliveryDate) }}            </p>            <p>              <i class="material-icons">person</i>              <strong>Usuário Solicitante:</strong> {{ sanitizeHtml(selectedOrder.usuario_nome) }}            </p>          </div>        </div>
      
      <!-- Campo de data de conclusão -->
      <div class="completion-date-container">
        <label for="completionDate">
          <i class="material-icons">event_available</i>
          Data de Conclusão:
        </label>
        <input 
          id="completionDate" 
          type="date" 
          v-model="completionDate" 
          :min="minDate"
          required 
          class="date-picker"
        />
        <p class="date-helper-text">
          <i class="material-icons info-icon">info</i>
          Selecione a data em que o pedido foi realmente concluído. Não é possível selecionar datas anteriores à data do pedido.
        </p>
      </div>
      
      <p class="confirm-message">Tem certeza que deseja concluir este pedido?</p>
      <div class="confirm-buttons">
        <button class="confirm-yes" @click="confirmComplete">
          <i class="material-icons">check</i>
          CONFIRMAR
        </button>
        <button class="confirm-no" @click="cancelConfirmation">
          <i class="material-icons">cancel</i>
          CANCELAR
        </button>
      </div>
    </div>
  </div>
</template>

<script>import axios from "axios";import { useToast } from "vue-toastification";

export default {
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
      showConfirmation: false,
      selectedOrder: null,
      completionDate: null,
      minDate: null,
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
    // Exibe o modal de confirmação com os detalhes do pedido
    showConfirmModal(order) {
      this.selectedOrder = order;
      
      // Log para diagnóstico dos campos disponíveis no pedido
      console.log("Dados do pedido selecionado:", {
        id: order.id,
        deliveryDate: order.deliveryDate,
        todos_campos: Object.keys(order)
      });
      
      // Usar a data do pedido como data mínima para conclusão
      if (order.deliveryDate) {
        const dataPedido = new Date(order.deliveryDate);
        if (!isNaN(dataPedido.getTime())) {
          this.minDate = dataPedido.toISOString().split('T')[0];
          console.log(`Usando data do pedido como data mínima: ${this.minDate}`);
        } else {
          // Se a data do pedido for inválida, usa a data atual
          console.warn(`Data do pedido inválida (${order.deliveryDate}), usando data atual`);
          this.minDate = new Date().toISOString().split('T')[0];
        }
      } else {
        // Se não houver data do pedido, usa a data atual
        console.warn(`Pedido ${order.id} não tem data definida, usando data atual`);
        this.minDate = new Date().toISOString().split('T')[0];
      }
      
      // Inicializar a data de conclusão com a data atual
      this.completionDate = new Date().toISOString().split('T')[0];
      this.showConfirmation = true;
      
      console.log(`Modal de conclusão aberto para o pedido #${order.id}. Data mínima: ${this.minDate}`);
    },
    
    // Cancela a confirmação e fecha o modal
    cancelConfirmation() {
      this.showConfirmation = false;
      this.selectedOrder = null;
      this.completionDate = null;
    },
    
    // Confirma a conclusão do pedido após confirmação no modal
    confirmComplete() {
      if (!this.selectedOrder) return;
      
      // Obter dados do usuário atual
      const userStr = localStorage.getItem("user");
      let userId = null;
      let userName = this.userName;
      let userType = this.userType;
      
      if (userStr) {
        try {
          const userObj = JSON.parse(userStr);
          userId = userObj.id;
          userName = userObj.nome || userObj.username;
          userType = userObj.tipo_usuario;
          
          console.log("Dados do usuário:", {
            id: userId,
            nome: userName,
            tipo: userType
          });
        } catch (e) {
          console.error("Erro ao obter dados do usuário para registro:", e);
        }
      }
      
      // Verificar se o usuário pode concluir o pedido
      // Admin ou gestor podem concluir qualquer pedido
      // Usuário comum só pode concluir seus próprios pedidos
      const isAdminOrGestor = userType === "admin" || userType === "gestor";
      const isCreator = this.selectedOrder.usuario_id === userId || 
                        this.selectedOrder.usuario_nome === userName;
      
      console.log("Verificação de permissão:", {
        isAdminOrGestor,
        isCreator,
        "pedido.usuario_id": this.selectedOrder.usuario_id,
        "pedido.usuario_nome": this.selectedOrder.usuario_nome,
        "usuario.id": userId,
        "usuario.nome": userName
      });
      
      if (!isAdminOrGestor && !isCreator) {
        this.toast.error(
          "Você não tem permissão para concluir este pedido. Apenas o criador do pedido, administradores ou gestores podem concluí-lo.", 
          {
            toastClassName: "custom-toast-error",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close",
            timeout: 5000 // Mensagem mais longa, mais tempo para ler
          }
        );
        return;
      }
      
      // Criar informações de histórico detalhadas
      const historicoItem = {
        campo_alterado: "status",
        valor_anterior: this.selectedOrder.status || "Pendente",
        valor_novo: "Concluído",
        data_edicao: new Date().toISOString(),
        usuario_nome: userName,
        pedido_id: this.selectedOrder.id
      };
      
      // Preparar os dados para atualização
      // Criamos uma cópia limpa dos dados do pedido para evitar problemas com campos extras
      const updateData = {
        id: this.selectedOrder.id,
        descricao: this.selectedOrder.descricao,
        quantidade: this.selectedOrder.quantidade,
        categoria: this.selectedOrder.categoria,
        urgencia: this.selectedOrder.urgencia, 
        deliveryDate: this.selectedOrder.deliveryDate,
        setor: this.selectedOrder.setor,
        status: "Concluído",
        sender: this.selectedOrder.sender || this.selectedOrder.usuario_nome,
        observacao: this.selectedOrder.observacao || "",
        completionDate: this.completionDate,
        usuario_nome: userName,
        usuario_id: userId,
        historico: [historicoItem]
      };
      
      console.log("Dados enviados para atualização:", updateData);
      
      // Enviar requisição para atualizar o status do pedido usando o endpoint com-historico
      axios
        .put(`${process.env.VUE_APP_API_URL}/pedidos/${this.selectedOrder.id}/com-historico`, updateData, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        })
        .then((response) => {
          console.log("Resposta do servidor:", response.data);
          // Atualizar a lista de pedidos após concluir
          this.fetchOrders();
          // Fechar o modal de confirmação
          this.showConfirmation = false;
          this.selectedOrder = null;
          this.completionDate = null;
          // Notificação estilizada com as cores do sistema
          this.toast.success("Pedido concluído com sucesso!", {
            toastClassName: "custom-toast-success",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close"
          });
        })
        .catch(error => {
          console.error("Erro ao concluir pedido:", error);
          
          // Determinar a mensagem de erro adequada
          let errorMessage = "Erro ao concluir pedido. Por favor, tente novamente.";
          
          if (error.response) {
            if (error.response.status === 422) {
              errorMessage = "Não foi possível concluir este pedido. Verifique se você tem permissão para esta ação ou se o pedido já foi concluído por outro usuário.";
            } else if (error.response.data && error.response.data.detail) {
              errorMessage = error.response.data.detail;
            } else if (error.response.status === 401) {
              errorMessage = "Sua sessão expirou. Por favor, faça login novamente.";
            } else if (error.response.status === 403) {
              errorMessage = "Você não tem permissão para concluir este pedido.";
            }
          }
            
          // Notificação de erro estilizada com mensagem melhorada
          this.toast.error(errorMessage, {
            toastClassName: "custom-toast-error",
            bodyClassName: "custom-toast-body",
            closeButtonClassName: "custom-toast-close",
            timeout: 5000 // Mais tempo para ler mensagens de erro detalhadas
          });
        });
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
  padding: 30px; 
  border-radius: 10px;
  width: 100%;
  max-width: 900px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  font-size: 1.1rem;
  overflow-y: auto;
  max-height: 90vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
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
.complete-button {
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
.complete-button i {
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

.open-button:hover {
  background-color: #2980b9;
}

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
  margin-top: 25px;
}

.pagination button {
  background-color: #444;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
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
}

.pagination span {
  color: #ddd;
  font-size: 0.9rem;
}

/* Botão de fechar */
.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 25px auto 0; 
  background: transparent;
  border: 2px solid #ff6f61;
  color: #ff6f61;
  font-size: 1rem;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.close-btn i {
  margin-right: 8px;
  font-size: 18px;
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
  padding: 15px;
  box-sizing: border-box;
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
}

.confirm-order-info p {
  margin: 8px 0;
  font-size: 0.9rem;
  color: #dfe6e9;
  display: flex;
  align-items: center;
}

.confirm-order-info p i {
  margin-right: 8px;
  color: #ff6f61;
  font-size: 16px;
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
}

.completion-date-container input:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 111, 97, 0.2);
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

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .order-form {
    max-width: 90%;
    padding: 25px;
  }
  
  .orders-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 15px;
  }
  
  .form-header h2 {
    font-size: 1.3rem;
  }
  
  .order-card {
    padding: 15px;
  }
  
  .filters-container {
    margin-top: 15px;
    width: 100%;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
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
    font-size: 0.85rem;
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
  .modal-overlay,
  .confirm-modal-overlay {
    padding: 10px;
  }
  
  .order-form {
    padding: 15px;
    max-width: 100%;
  }
  
  .orders-list {
    grid-template-columns: 1fr;
  }

  .order-card {
    padding: 15px;
  }
  
  .form-header h2 {
    font-size: 1.1rem;
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
    font-size: 0.9rem;
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
    font-size: 0.9rem;
    padding: 10px 15px;
    margin-top: 15px;
  }
}
</style>
