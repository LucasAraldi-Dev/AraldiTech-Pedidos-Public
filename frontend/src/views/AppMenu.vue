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
      <!-- Botão Dashboard apenas para gestores -->
      <button 
        v-if="isGestor" 
        class="menu-btn gestor-btn" 
        @click="openDashboard"
      >
        Dashboard de Gestão
      </button>
      <!-- Botão Relatório Financeiro para gestores -->
      <button 
        v-if="isGestor" 
        class="menu-btn finance-btn" 
        @click="openFinancialReport"
      >
        Relatório Financeiro
      </button>
      <!-- Botão Gerenciar Usuários apenas para administradores -->
      <button 
        v-if="isAdmin" 
        class="menu-btn admin-btn" 
        @click="openUserManagementModal"
      >
        Gerenciar Usuários
      </button>
      <!-- Botão de Ajuda para todos os usuários -->
      <button class="menu-btn help-btn" @click="openHelp">
        Ajuda
      </button>
      <button class="menu-btn logout-btn" @click="logout">Sair</button>
    </div>

    <!-- Menu de tela cheia no mobile -->
    <div v-if="isMenuOpen && isMobile" class="fullscreen-menu">
      <button class="menu-btn" @click="openCreateOrderSection">Criar Pedido</button>
      <button class="menu-btn" @click="openConsultOrdersSection">Consultar Pedidos</button>
      <!-- Botão Dashboard apenas para gestores -->
      <button 
        v-if="isGestor" 
        class="menu-btn gestor-btn" 
        @click="openDashboard"
      >
        Dashboard de Gestão
      </button>
      <!-- Botão Relatório Financeiro para gestores -->
      <button 
        v-if="isGestor" 
        class="menu-btn finance-btn" 
        @click="openFinancialReport"
      >
        Relatório Financeiro
      </button>
      <!-- Botão Gerenciar Usuários apenas para administradores -->
      <button 
        v-if="isAdmin" 
        class="menu-btn admin-btn" 
        @click="openUserManagementModal"
      >
        Gerenciar Usuários
      </button>
      <!-- Botão de Ajuda para todos os usuários -->
      <button class="menu-btn help-btn" @click="openHelp">
        Ajuda
      </button>
      <button class="menu-btn close-menu-btn" @click="toggleMenu">Fechar Menu</button>
      <button class="menu-btn logout-btn" @click="logout">Sair</button>
    </div>

    <div class="main-content" :class="{'has-content': isCreateOrderSectionOpen || isConsultOrdersSectionOpen || isPrintModalOpen || isEditOrderOpen || isUserManagementOpen || isFinancialReportOpen || isDashboardOpen}">
      <!-- O Dashboard foi movido para um componente modal separado e foi removido daqui -->
    </div>

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

    <!-- Modal de Relatório Financeiro -->
    <ModalRelatorioFinanceiro
      v-if="isFinancialReportOpen"
      :isOpen="isFinancialReportOpen"
      @close="closeFinancialReport"
    />

    <!-- Modal de Dashboard de Gestão -->
    <ModalDashboard
      v-if="isDashboardOpen"
      :isOpen="isDashboardOpen"
      @close="closeDashboard"
    />

    <!-- Modal de Tutorial -->
    <TutorialModal
      v-if="isTutorialOpen"
      :isOpen="isTutorialOpen"
      @close="closeTutorial"
    />
  </div>
</template>

<script>
import ModalCriarPedido from '@/components/ModalCriarPedido.vue';
import ModalConsultaPedidos from '@/components/ModalConsultaPedidos.vue';
import ModalEditarPedido from '@/components/ModalEditarPedido.vue';
import ModalImprimirPedido from '@/components/ModalImprimirPedido.vue';
import ModalGerenciarUsuarios from '@/components/ModalGerenciarUsuarios.vue';
import ModalRelatorioFinanceiro from '@/components/ModalRelatorioFinanceiro.vue';
import ModalDashboard from '@/components/ModalDashboard.vue';
import TutorialModal from '@/components/TutorialModal.vue';
import html2canvas from "html2canvas";
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';

// Registrar todos os componentes do Chart.js
Chart.register(...registerables);

export default {
  name: 'AppMenu',
  components: {
    ModalCriarPedido,
    ModalConsultaPedidos,
    ModalEditarPedido,
    ModalImprimirPedido,
    ModalGerenciarUsuarios,
    ModalRelatorioFinanceiro,
    ModalDashboard,
    TutorialModal,
  },
  data() {
    return {
      isCreateOrderSectionOpen: false,
      isConsultOrdersSectionOpen: false,
      isPrintModalOpen: false,
      isDashboardOpen: false,
      isEditOrderOpen: false,
      isFinancialReportOpen: false,
      isUserManagementOpen: false,
      isMenuOpen: false,
      isTutorialOpen: false,
      isMobile: false,
      pedidoCriado: null,
      selectedOrder: null,
      orders: [],
      // Remover variáveis específicas do dashboard que não são mais necessárias
      userName: '',
      // Verificar permissões de usuário
      isAdmin: false,
      isGestor: false
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
    console.log("Primeiro login:", user?.primeiro_login ? "Sim" : "Não");
    
    if (!token || !user) {
      console.warn("Usuário não autenticado, redirecionando para login");
      this.$router.push({ name: "Login" });
    } else {
      this.isAdmin = user.tipo_usuario === "admin";
      this.isGestor = user.tipo_usuario === "gestor" || user.tipo_usuario === "admin";
      
      // Verificar se é o primeiro login do usuário
      const urlSearchParams = new URLSearchParams(window.location.search);
      const isFirstLogin = urlSearchParams.get('firstLogin') === 'true';
      
      console.log("Parâmetro firstLogin:", isFirstLogin ? "Sim" : "Não");
      console.log("Tipo de usuário:", user.tipo_usuario);
      
      // Verificar se o tutorial deve ser exibido
      if ((isFirstLogin || user.primeiro_login) && user.tipo_usuario === 'comum') {
        console.log("Abrindo tutorial para novo usuário...");
        // Se for o primeiro login de um usuário comum, mostrar o tutorial
        this.openTutorial();
      }
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
      // Atualizar no array orders se existir
      if (this.orders && this.orders.length > 0) {
        const index = this.orders.findIndex((o) => o.id === updatedOrder.id);
        if (index !== -1) this.orders.splice(index, 1, updatedOrder);
      }
      
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
    // Métodos do Dashboard
    openDashboard() {
      this.isDashboardOpen = true;
      if (this.isMobile) {
        this.isMenuOpen = false;
      }
    },
    closeDashboard() {
      this.isDashboardOpen = false;
    },
    openFinancialReport() {
      this.isFinancialReportOpen = true;
      this.isMenuOpen = false;
    },
    closeFinancialReport() {
      this.isFinancialReportOpen = false;
    },
    openHelp() {
      // Se for um usuário comum, abrir o tutorial
      const user = JSON.parse(localStorage.getItem("user"));
      if (user && user.tipo_usuario === 'comum') {
        this.openTutorial();
      } else {
        // Para outros tipos de usuário, redirecionar para a página de ajuda
        this.$router.push({ name: "Ajuda" });
      }
      this.isMenuOpen = false;
    },
    openTutorial() {
      this.isTutorialOpen = true;
      this.isMenuOpen = false;
    },
    async closeTutorial() {
      this.isTutorialOpen = false;
      
      try {
        // Atualizar o campo primeiro_login no backend
        const token = localStorage.getItem("access_token");
        if (token) {
          const response = await axios.put(
            `${process.env.VUE_APP_API_URL}/usuarios/primeiro-login`,
            {},
            {
              headers: { Authorization: `Bearer ${token}` }
            }
          );
          
          console.log("Primeiro login atualizado no backend:", response.data);
          
          // Atualizar também no localStorage
          const user = JSON.parse(localStorage.getItem("user"));
          if (user) {
            user.primeiro_login = false;
            localStorage.setItem("user", JSON.stringify(user));
          }
        }
      } catch (error) {
        console.error("Erro ao atualizar status de primeiro login:", error);
      }
      
      // Limpar parâmetros da URL para não reabrir o tutorial em atualizações de página
      const currentUrl = window.location.href;
      const urlWithoutParams = currentUrl.split('?')[0];
      window.history.replaceState({}, document.title, urlWithoutParams);
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

.logout-btn:hover {
  background-color: #ff3333;
}

.admin-btn {
  background-color: #FF5733;
  border-color: #FF5733;
}

.admin-btn:hover {
  background-color: #e64a2e;
  border-color: #e64a2e;
}

.gestor-btn {
  background-color: #5bc0de;
  border-color: #5bc0de;
}

.gestor-btn:hover {
  background-color: #666666;
}

.finance-btn {
  background-color: #555555; /* Cinza neutro para Relatório Financeiro */
}

.finance-btn:hover {
  background-color: #666666;
}

.main-content {
  min-height: 100vh;
  width: calc(100vw - 250px); 
  margin-left: 250px;
  padding: 40px;
  background-color: #1f1f1f;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow-y: auto;
}

/* Background com logo apenas quando não há conteúdo ativo */
.main-content:not(.has-content) {
  background-image: url('../components/favicon_logo_branco.png');
  background-size: 70%; 
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.3;
}

.main-content.has-content {
  opacity: 1;
  background-image: none;
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

/* Dashboard Styles */
.dashboard-grid {
  width: 100%;
  display: grid;
  grid-gap: 20px;
  padding: 20px 0;
}

.dashboard-title {
  grid-column: 1 / -1;
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  color: #f5f5f5;
}

.dashboard-row {
  display: grid;
  grid-gap: 20px;
  width: 100%;
}

.kpi-row {
  grid-template-columns: repeat(3, 1fr);
}

.chart-row {
  grid-template-columns: repeat(3, 1fr);
  min-height: 300px;
}

.split-row {
  grid-template-columns: 1fr 1fr;
}

.kpi-card {
  background-color: #333;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
}

.kpi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.kpi-card h3 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #aaa;
}

.kpi-value {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
}

.chart-wrapper {
  background-color: #333;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  height: 300px;
}

.chart-wrapper h3 {
  margin-bottom: 10px;
  text-align: center;
  font-size: 16px;
  color: #aaa;
}

.activities-section, .reports-section {
  background-color: #333;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  min-height: 400px;
  max-height: 500px;
  display: flex;
  flex-direction: column;
}

.activities-section h2, .reports-section h2 {
  margin-bottom: 15px;
  font-size: 20px;
  color: #f5f5f5;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}

.activity-feed {
  flex: 1;
  overflow-y: auto;
  padding-right: 10px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.activity-item {
  background-color: #444;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  gap: 15px;
  transition: background-color 0.3s;
}

.activity-item:hover {
  background-color: #555;
}

.activity-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.activity-icon-create {
  background-color: #4CAF50;
}

.activity-icon-edit {
  background-color: #2196F3;
}

.activity-icon-complete {
  background-color: #9C27B0;
}

.activity-icon-cancel {
  background-color: #FF5722;
}

.activity-icon-login {
  background-color: #607D8B;
}

.activity-icon-default {
  background-color: #9E9E9E;
}

.activity-content {
  flex: 1;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.activity-user {
  font-weight: bold;
  color: #e0e0e0;
}

.activity-date {
  color: #aaa;
  font-size: 0.85em;
}

.activity-description {
  margin-bottom: 5px;
  color: #ccc;
}

.activity-details a {
  color: #8ab4f8;
  cursor: pointer;
  text-decoration: underline;
}

.view-order-btn {
  display: inline-block;
  background-color: #4a6da7;
  color: white !important;
  padding: 5px 10px;
  border-radius: 4px;
  text-decoration: none !important;
  font-size: 0.85em;
  margin-top: 5px;
  transition: background-color 0.3s, transform 0.2s;
}

.view-order-btn:hover {
  background-color: #5e82bc;
  transform: translateY(-2px);
}

.report-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #aaa;
}

.form-group select, .form-group input {
  width: 100%;
  padding: 8px;
  background-color: #444;
  border: 1px solid #555;
  border-radius: 4px;
  color: #f5f5f5;
}

.date-range {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.btn-generate {
  width: 100%;
  padding: 12px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-generate:hover {
  background-color: #27ae60;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #aaa;
}

.empty-feed {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
  color: #aaa;
  font-style: italic;
}

.financial-summary-section {
  background-color: #2c3e50;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.financial-kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.financial-kpi {
  background-color: #34495e;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.financial-kpi h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #ccc;
}

.financial-kpi .kpi-value {
  font-size: 24px;
  font-weight: bold;
}

.positive-balance .kpi-value {
  color: #2ecc71;
}

.negative-balance .kpi-value {
  color: #e74c3c;
}

.financial-chart-wrapper {
  background-color: #34495e;
  border-radius: 8px;
  padding: 15px;
  height: 300px;
  margin-top: 20px;
}

.financial-chart-wrapper h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
  text-align: center;
  color: #f5f5f5;
}

.activity-icon-finance {
  background-color: #9b59b6;
}

.help-btn {
  background-color: #5cb85c;
  border-color: #5cb85c;
}

.help-btn:hover {
  background-color: #4cae4c;
  border-color: #4cae4c;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  .main-content {
    width: 100vw;
    margin-left: 0;
    padding: 20px;
  }
  
  .kpi-row, .chart-row, .split-row {
    grid-template-columns: 1fr;
  }
  
  .dashboard-title {
    font-size: 22px;
  }
  .financial-kpis {
    grid-template-columns: 1fr;
  }
}

/* Otimizações para tablets e telas 1024x768 */
@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar {
    width: 200px;
  }
  
  .main-content {
    width: calc(100vw - 200px);
    margin-left: 200px;
    padding: 25px;
  }
  
  .kpi-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .kpi-card:last-child {
    grid-column: span 2;
  }
  
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .financial-kpis {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .financial-kpi:last-child {
    grid-column: span 2;
  }
  
  .menu-btn {
    font-size: 14px;
    padding: 10px 15px;
  }
}

/* Otimizações para telas entre 1025px e 1200px */
@media (min-width: 1025px) and (max-width: 1200px) {
  .chart-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .chart-wrapper:last-child {
    grid-column: span 2;
  }
  
  .main-content {
    padding: 30px;
  }
}

/* Otimizações para telas Full HD (1920x1080) */
@media (min-width: 1367px) and (max-width: 1920px) {
  .main-content {
    padding: 40px 60px;
  }
  
  .sidebar {
    width: 270px;
  }
  
  .main-content {
    width: calc(100vw - 270px);
    margin-left: 270px;
  }
  
  .menu-btn {
    padding: 15px 25px;
    font-size: 18px;
  }
  
  .dashboard-title {
    font-size: 32px;
  }
  
  .kpi-card {
    padding: 25px;
  }
  
  .kpi-card h3 {
    font-size: 18px;
  }
  
  .kpi-value {
    font-size: 38px;
  }
}

/* Otimizações para telas maiores que Full HD */
@media (min-width: 1921px) {
  .sidebar {
    width: 300px;
  }
  
  .main-content {
    width: calc(100vw - 300px);
    margin-left: 300px;
    padding: 50px 80px;
  }
  
  .menu-btn {
    padding: 18px 30px;
    font-size: 20px;
    margin-bottom: 15px;
  }
  
  .dashboard-title {
    font-size: 36px;
  }
  
  .kpi-row, .chart-row {
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
  }
  
  .kpi-card {
    padding: 30px;
  }
  
  .kpi-card h3 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .kpi-value {
    font-size: 42px;
  }
}
</style>
