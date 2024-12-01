<template>
  <div class="app-container">
    <!-- Botão para abrir o menu no mobile -->
    <button class="open-menu-btn" @click="toggleMenu" v-if="isMobile">
      Menu
    </button>

    <!-- Sidebar no desktop e menu modal no mobile -->
    <div class="sidebar" v-if="!isMobile">
      <button class="menu-btn" @click="openCreateOrderSection">Criar Pedido</button>
      <button class="menu-btn" @click="openConsultOrdersSection">Consultar Pedidos</button>
      <button class="menu-btn logout-btn" @click="logout">Sair</button>
    </div>

    <!-- Menu de tela cheia no mobile -->
    <div v-if="isMenuOpen && isMobile" class="fullscreen-menu">
      <button class="menu-btn" @click="openCreateOrderSection">Criar Pedido</button>
      <button class="menu-btn" @click="openConsultOrdersSection">Consultar Pedidos</button>
      <button class="menu-btn close-menu-btn" @click="toggleMenu">Fechar Menu</button>
      <button class="menu-btn logout-btn" @click="logout">Sair</button>
    </div>

    <div class="main-content"></div>

    <!-- Modal de Criação de Pedido -->
    <section v-if="isCreateOrderSectionOpen" class="order-section">
      <ModalCriarPedido
        :isOpen="isCreateOrderSectionOpen"
        @close="closeCreateOrderSection"
        @create-order="handleCreateOrder"
      />
    </section>

    <!-- Modal de Consulta de Pedidos -->
    <section v-if="isConsultOrdersSectionOpen" class="order-section">
      <ModalConsultaPedidos
        ref="consultModal"
        :isOpen="isConsultOrdersSectionOpen"
        @close="closeConsultOrdersSection"
        @edit-order="openEditOrderSection"
        @open-order="handlePrintModal"
      />
    </section>

    <!-- Modal de Edição de Pedido -->
    <ModalEditarPedido
  ref="editModal"
  v-if="isEditOrderOpen"
  :isOpen="isEditOrderOpen"
  :order="selectedOrder"
  @close="closeEditOrderSection"
  @order-updated="closeEditOrderSection"
/>

    <!-- Modal de Impressão de Pedido -->
    <ModalImprimirPedido
      v-if="isPrintModalOpen"
      :isOpen="isPrintModalOpen"
      :pedido="pedidoCriado"
      @close="closePrintModal"
    />
  </div>
</template>

<script>
import ModalCriarPedido from "@/components/ModalCriarPedido.vue";
import ModalConsultaPedidos from "@/components/ModalConsultaPedidos.vue";
import ModalEditarPedido from "@/components/ModalEditarPedido.vue";
import ModalImprimirPedido from "@/components/ModalImprimirPedido.vue";
import axios from "axios";

export default {
  components: {
    ModalCriarPedido,
    ModalConsultaPedidos,
    ModalEditarPedido,
    ModalImprimirPedido,
  },
  data() {
    return {
      isCreateOrderSectionOpen: false,
      isConsultOrdersSectionOpen: false,
      isPrintModalOpen: false,
      isEditOrderOpen: false,
      selectedOrder: null,
      pedidoCriado: null,
      orders: [],
      isMobile: false,
      isMenuOpen: false,
    };
  },
  created() {
    this.checkIfMobile();
    window.addEventListener("resize", this.checkIfMobile);
  },
  unmounted() {
    window.removeEventListener("resize", this.checkIfMobile);
  },
  methods: {
    openCreateOrderSection() {
      this.isCreateOrderSectionOpen = true;
      this.isMenuOpen = false;
    },
    closeCreateOrderSection() {
      this.isCreateOrderSectionOpen = false;
    },
    openConsultOrdersSection() {
      this.isConsultOrdersSectionOpen = true;
      this.isMenuOpen = false;
    },
    closeConsultOrdersSection() {
      this.isConsultOrdersSectionOpen = false;
    },
    openEditOrderSection(order) {
      this.selectedOrder = {
        ...order,
        deliveryDate: new Date(order.deliveryDate).toISOString().split("T")[0],
      };
      this.isEditOrderOpen = true;
    },
    async closeEditOrderSection(updatedOrder) {
  this.isEditOrderOpen = false;

  if (updatedOrder) {
    // Atualiza na lista local de pedidos
    const index = this.orders.findIndex((o) => o.id === updatedOrder.id);
    if (index !== -1) {
      this.orders.splice(index, 1, updatedOrder); // Atualiza pedido específico
    }

    // Sincroniza a lista de pedidos no modal de consulta
    if (this.$refs.consultModal) {
      this.$refs.consultModal.fetchOrders(); // Recarrega lista no modal
    }
  } else {
    await this.fetchOrders(); // Recarrega lista geral, se necessário
  }
},
    handleEditOrder(updatedOrder) {
      const index = this.orders.findIndex((o) => o.id === updatedOrder.id);
      if (index !== -1) this.orders.splice(index, 1, updatedOrder);
    },
    handlePrintModal(pedido) {
      this.pedidoCriado = pedido;
      this.isPrintModalOpen = true;
    },
    closePrintModal() {
      this.isPrintModalOpen = false;
    },
    logout() {
      localStorage.removeItem("user_name");
      localStorage.removeItem("user");
      localStorage.removeItem("token_type");
      localStorage.removeItem("access_token");
      this.$router.push({ name: "Login" });
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    checkIfMobile() {
      this.isMobile = window.innerWidth <= 768;
      if (!this.isMobile) {
        this.isMenuOpen = false;
      }
    },
    async fetchOrders() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        });
        this.orders = response.data;
      } catch (error) {
        console.error("Erro ao carregar pedidos:", error);
      }
    },
    handleCreateOrder(pedidoCriado) {
      this.pedidoCriado = pedidoCriado;
      this.isPrintModalOpen = true;
      this.isCreateOrderSectionOpen = false;
    },
  },
};
</script>




<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.app-container {
  display: flex;
  font-family: 'Roboto', sans-serif;
  color: #f5f5f5;
  background-color: #1a1a1a;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #2e2e2e;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  box-shadow: 2px 0 15px rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 1;
}

.menu-btn {
  background-color: #424242;
  color: #f5f5f5;
  font-weight: bold;
  font-size: 1rem;
  width: 80%;
  margin: 10px 0;
  padding: 12px 0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn {
  background-color: #ff5252;
}

.main-content {
  min-height: 100vh;
  width: calc(100vw - 250px); 
  padding: 40px;
  background-color: #1f1f1f;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.3);
  background-image: url('../components/favicon_logo_branco.png');
  background-size: 70%; 
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.3;
}

.open-menu-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  background-color: #424242;
  color: #f5f5f5;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 1rem;
  z-index: 1000;
  cursor: pointer;
}

.fullscreen-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #1a1a1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.close-menu-btn {
  margin-top: 20px;
  background-color: #424242;
  color: #f5f5f5;
  font-weight: bold;
  width: 80%;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  .main-content {
    margin-left: 0;
  }
  @media (max-width: 768px) {
  .main-content {
    width: 100vw; 
    margin-left: 0; 
    padding: 20px; 
  }
}

}
</style>
