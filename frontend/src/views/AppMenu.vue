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
      <!-- Botão Gerenciar Usuários apenas para administradores -->
      <button 
        v-if="isAdmin" 
        class="menu-btn admin-btn" 
        @click="openUserManagementModal"
      >
        Gerenciar Usuários
      </button>
      <button class="menu-btn logout-btn" @click="logout">Sair</button>
    </div>

    <!-- Menu de tela cheia no mobile -->
    <div v-if="isMenuOpen && isMobile" class="fullscreen-menu">
      <button class="menu-btn" @click="openCreateOrderSection">Criar Pedido</button>
      <button class="menu-btn" @click="openConsultOrdersSection">Consultar Pedidos</button>
      <!-- Botão Gerenciar Usuários apenas para administradores -->
      <button 
        v-if="isAdmin" 
        class="menu-btn admin-btn" 
        @click="openUserManagementModal"
      >
        Gerenciar Usuários
      </button>
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
        @create-order-with-image="handleCreateOrderWithImage"
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
      v-if="isEditOrderOpen"
      :isOpen="isEditOrderOpen"
      :pedido="selectedOrder"
      @close="closeEditOrderSection"
      @update-order="handleEditOrder"
    />

    <!-- Modal de Impressão de Pedido -->
    <ModalImprimirPedido
      v-if="isPrintModalOpen"
      :isOpen="isPrintModalOpen"
      :pedido="pedidoCriado"
      @close="closePrintModal"
      @new-order="openNewOrderFromPrintModal"
    />

    <!-- Modal de Gerenciamento de Usuários -->
    <ModalGerenciarUsuarios
      v-if="isUserManagementOpen"
      :isOpen="isUserManagementOpen"
      @close="closeUserManagementModal"
      @close-menu="closeMenu"
    />
  </div>
</template>

<script>
import ModalCriarPedido from "@/components/ModalCriarPedido.vue";
import ModalConsultaPedidos from "@/components/ModalConsultaPedidos.vue";
import ModalEditarPedido from "@/components/ModalEditarPedido.vue";
import ModalImprimirPedido from "@/components/ModalImprimirPedido.vue";
import ModalGerenciarUsuarios from "@/components/ModalGerenciarUsuarios.vue";
import axios from "axios";
import html2canvas from "html2canvas";

export default {
  components: {
    ModalCriarPedido,
    ModalConsultaPedidos,
    ModalEditarPedido,
    ModalImprimirPedido,
    ModalGerenciarUsuarios,
  },
  data() {
    return {
      isCreateOrderSectionOpen: false,
      isConsultOrdersSectionOpen: false,
      isPrintModalOpen: false,
      isEditOrderOpen: false,
      isUserManagementOpen: false,
      selectedOrder: null,
      pedidoCriado: null,
      orders: [],
      isMobile: false,
      isMenuOpen: false,
      isAdmin: false,
    };
  },
  created() {
    console.log("AppMenu criado, verificando autenticação...");
    this.checkIfMobile();
    window.addEventListener("resize", this.checkIfMobile);
    
    // Verifica se o usuário está autenticado
    const token = localStorage.getItem("access_token");
    const user = JSON.parse(localStorage.getItem("user"));
    
    console.log("Token presente:", token ? "Sim" : "Não");
    console.log("Usuário presente:", user ? "Sim" : "Não");
    console.log("Tipo de usuário:", user?.tipo_usuario);
    
    if (!token || !user) {
      console.warn("Usuário não autenticado, redirecionando para login");
      this.$router.push({ name: "Login" });
    } else {
      this.isAdmin = user.tipo_usuario === "admin";
    }
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
    closeEditOrderSection() {
      // Apenas fecha o modal de edição
      this.isEditOrderOpen = false;
    },
    handleEditOrder(updatedOrder) {
      // Atualiza pedido na lista local e fecha o modal
      const index = this.orders.findIndex((o) => o.id === updatedOrder.id);
      if (index !== -1) this.orders.splice(index, 1, updatedOrder);
      
      // Atualizar a lista do modal de consulta
      if (this.$refs.consultModal) {
        this.$refs.consultModal.fetchOrders();
      }
      
      // Fechar o modal de edição
      this.isEditOrderOpen = false;
    },
    handlePrintModal(pedido) {
      this.pedidoCriado = pedido;
      this.isPrintModalOpen = true;
    },
    closePrintModal() {
      this.isPrintModalOpen = false;
    },
    openNewOrderFromPrintModal() {
      this.isPrintModalOpen = false;
      this.isCreateOrderSectionOpen = true;
    },
    logout() {
      // Remove todos os itens relacionados à autenticação
      localStorage.removeItem("user");
      localStorage.removeItem("tipo_usuario");
      localStorage.removeItem("token_type");
      localStorage.removeItem("access_token");
      
      console.log("Logout realizado, redirecionando para Login");
      this.$router.push({ name: "Login" });
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
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
    async handleCreateOrderWithImage(pedidoCriado) {
      // Guardar o pedido temporariamente
      this.pedidoCriado = pedidoCriado;
      
      // Abrir o modal de impressão brevemente para gerar a imagem
      this.isPrintModalOpen = true;
      
      // Esperar um momento para o DOM ser atualizado
      await this.$nextTick();
      
      // Acessar o modal de impressão usando ref
      setTimeout(async () => {
        try {
          // Obter o elemento do DOM depois que ele estiver renderizado
          const printModalElement = document.querySelector('.print-modal');
          
          if (printModalElement) {
            // Garantir que a largura da área de impressão seja fixa
            printModalElement.style.width = '800px'; 
            
            // Modificar a visibilidade dos botões antes de gerar a imagem
            const buttons = printModalElement.querySelectorAll('button');
            buttons.forEach(btn => btn.classList.add('hidden'));
            
            // Capturar o canvas
            const canvas = await html2canvas(printModalElement, {
              useCORS: true,
              scrollX: 0,
              scrollY: -window.scrollY,
            });
            
            // Restaurar os botões
            buttons.forEach(btn => btn.classList.remove('hidden'));
            
            // Restaurar o tamanho original
            printModalElement.style.width = '';
            
            // Gerar imagem PNG
            const imgData = canvas.toDataURL('image/png');
            
            // Criar um link para baixar a imagem
            const link = document.createElement('a');
            link.href = imgData;
            link.download = `pedido_${pedidoCriado.id}.png`; 
            link.click();
          }
        } catch (error) {
          console.error("Erro ao gerar imagem automática:", error);
        } finally {
          // Fechar o modal de impressão após gerar a imagem
          this.isPrintModalOpen = false;
        }
      }, 500); // Dar um tempo para o DOM ser renderizado completamente
    },
    openUserManagementModal() {
      this.isUserManagementOpen = true;
      this.isMenuOpen = false;
    },
    closeUserManagementModal() {
      this.isUserManagementOpen = false;
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

.admin-btn {
  background-color: #4a6da7; /* Azul escuro para indicar ações administrativas */
}

.admin-btn:hover {
  background-color: #3a5d97;
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
