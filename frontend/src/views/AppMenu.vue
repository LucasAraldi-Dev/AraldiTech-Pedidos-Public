<template>
  <div class="app-container">
    <!-- Fundo com logo -->
    <div class="background-logo"></div>
    
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
      <!-- Botão Visualizador de Logs para administradores -->
      <button 
        v-if="isAdmin" 
        class="menu-btn log-btn" 
        @click="openLogViewer"
      >
        Visualizar Logs
      </button>
      <div class="logout-spacer"></div>
      <button class="menu-btn logout-btn" @click="confirmLogout">Sair</button>
    </div>

    <!-- Menu de tela cheia no mobile -->
    <div v-if="isMenuOpen && isMobile" class="fullscreen-menu">
      <div class="menu-header">
        <button class="close-menu-btn" @click="toggleMenu">X</button>
      </div>
      <div class="menu-content">
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
        <!-- Botão Visualizador de Logs para administradores -->
        <button 
          v-if="isAdmin" 
          class="menu-btn log-btn" 
          @click="openLogViewer"
        >
          Visualizar Logs
        </button>
      </div>
      
      <!-- Botão Sair flutuante para mobile -->
      <button class="floating-logout-btn" @click="confirmLogout">Sair</button>
    </div>

    <div class="main-content" :class="{'has-content': isCreateOrderSectionOpen || isConsultOrdersSectionOpen || isEditOrderOpen || isUserManagementOpen || isFinancialReportOpen || isDashboardOpen}">
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
      @open-order="handlePrintModal"
    />

    <!-- Modal de Visualização de Logs -->
    <ModalLogViewer
      v-if="isLogViewerOpen"
      :isOpen="isLogViewerOpen"
      @close="closeLogViewer"
      @open-order="handlePrintModal"
    />
    
    <!-- Modal de Impressão de Pedido - deve ter a maior prioridade de renderização -->
    <div class="high-priority-modal-container" v-if="isPrintModalOpen && pedidoCriado">
      <ModalImprimirPedido
        :isOpen="isPrintModalOpen"
        :pedido="pedidoCriado"
        :origin="previousOpenModal ? 'consultation' : 'creation'"
        @close="closePrintModal"
        @new-order="handleNewOrderFromPrintModal"
      />
    </div>
            <!-- Modal de Confirmação de Logout Moderno -->    <div v-if="showLogoutConfirmation" class="logout-modal-overlay" @click="cancelLogout">      <div class="logout-modal-content" @click.stop>        <div class="logout-modal-header">          <div class="logout-icon">            <i class="material-icons">logout</i>          </div>          <h3>Confirmar Saída</h3>          <button class="close-modal-btn" @click="cancelLogout">            <i class="material-icons">close</i>          </button>        </div>                <div class="logout-modal-body">          <p>Tem certeza de que deseja sair do sistema?</p>          <div class="logout-warning">            <i class="material-icons">info</i>            <span>Você precisará fazer login novamente para acessar o sistema.</span>          </div>        </div>                <div class="logout-modal-footer">          <button class="logout-cancel-btn" @click="cancelLogout">            <i class="material-icons">close</i>            Cancelar          </button>          <button class="logout-confirm-btn" @click="proceedWithLogout">            <i class="material-icons">logout</i>            Sair do Sistema          </button>        </div>      </div>    </div>
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
import ModalLogViewer from '@/components/ModalLogViewer.vue';
import html2canvas from "html2canvas";
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';
import authService from '@/api/authService';

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
    ModalLogViewer,
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
      isMobile: false,
      pedidoCriado: null,
      selectedOrder: null,
      orders: [],
      // Remover variáveis específicas do dashboard que não são mais necessárias
      userName: '',
      // Verificar permissões de usuário
      isAdmin: false,
      isGestor: false,
      isLogViewerOpen: false,
      // Adicionar variável para debug
      debugInterval: null,
      // Adicionar variável para rastrear modal aberto anteriormente
      previousOpenModal: null,
      // Modal de confirmação de logout
      showLogoutConfirmation: false
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
      this.isGestor = user.tipo_usuario === "gestor" || user.tipo_usuario === "admin";
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
      console.log('[CRÍTICO] handlePrintModal chamado com pedido:', pedido);
      
      try {
        // Limpar qualquer intervalo de debug anterior
        if (this.debugInterval) {
          clearInterval(this.debugInterval);
          this.debugInterval = null;
        }
        
        // Se recebermos apenas o ID do pedido em vez do objeto completo
        if (typeof pedido === 'number' || (typeof pedido === 'string' && !isNaN(parseInt(pedido, 10)))) {
          const pedidoId = typeof pedido === 'number' ? pedido : parseInt(pedido, 10);
          console.log(`[CRÍTICO] Recebido apenas o ID do pedido (${pedidoId}). Buscando detalhes completos...`);
          
          // Buscar os detalhes do pedido a partir do ID
          this.fetchPedidoById(pedidoId);
          return;
        }
        
        // Verificar se o pedido tem as propriedades esperadas
        if (!pedido || !pedido.id) {
          console.error('[CRÍTICO] Pedido inválido recebido em handlePrintModal:', pedido);
          alert('Pedido inválido ou sem ID.');
          return;
        }
        
        console.log('[CRÍTICO] Pedido válido encontrado, ID:', pedido.id);
        
        // Salvar qual modal está aberto antes de abrir o modal de impressão
        this.savePreviousOpenModal();
        
        // Não fechamos mais os modais, para que o modal anterior possa ser reaberto
        // Apenas removemos o código que fecha todos os modais
        
        // Garantir que todos os campos necessários existam
        console.log('[DEBUG] Pedido original:', pedido);
        console.log('[DEBUG] Valor de sender no pedido:', pedido.sender);
        
        // Obter informações do usuário do localStorage
        let userInfo = null;
        try {
          if (localStorage.getItem('user')) {
            userInfo = JSON.parse(localStorage.getItem('user'));
            console.log('[DEBUG] Informações do usuário:', userInfo);
          }
        } catch (e) {
          console.error('[DEBUG] Erro ao obter informações do usuário:', e);
        }
        
        this.pedidoCriado = {
          ...pedido,
          // Definir valores padrão para campos que podem estar ausentes
          descricao: pedido.descricao || '',
          quantidade: pedido.quantidade || 0,
          urgencia: pedido.urgencia || 'Normal',
          categoria: pedido.categoria || 'Geral',
          deliveryDate: pedido.deliveryDate || new Date().toISOString().split('T')[0],
          observacao: pedido.observacao || '',
          sender: pedido.sender || (userInfo ? userInfo.nome : '')
        };
        
        console.log('[DEBUG] Valor final de sender para o modal:', this.pedidoCriado.sender);
        
        console.log('[CRÍTICO] Abrindo modal de impressão com pedido:', pedido.id);
        
        // Diretamente definir como aberto, sem usar nextTick
        this.isPrintModalOpen = true;
        
        // Forçar renderização direta
        this.$forceUpdate();
        
        // Para debug
        setTimeout(() => {
          const modalElement = document.querySelector('.print-modal');
          console.log('[CRÍTICO] Modal visível?', !!modalElement);
          
          if (!modalElement) {
            console.log('[CRÍTICO] Modal não encontrado! Tentando novamente...');
            this.isPrintModalOpen = false;
            this.$forceUpdate();
            
            setTimeout(() => {
              this.isPrintModalOpen = true;
              this.$forceUpdate();
              
              // Verificar novamente
              setTimeout(() => {
                const modalElementRetry = document.querySelector('.print-modal');
                console.log('[CRÍTICO] Modal visível após retry?', !!modalElementRetry);
              }, 100);
            }, 100);
          }
        }, 100);
      } catch (err) {
        console.error('[CRÍTICO] Erro ao abrir modal de impressão:', err);
        alert(`Erro ao abrir modal: ${err.message}`);
      }
    },
    
    // Método auxiliar para fechar todos os modais
    closeAllModals() {
      this.isCreateOrderSectionOpen = false;
      this.isConsultOrdersSectionOpen = false;
      this.isEditOrderOpen = false;
      this.isFinancialReportOpen = false;
      this.isDashboardOpen = false;
      this.isUserManagementOpen = false;
      this.isLogViewerOpen = false;
      this.isMenuOpen = false;
      this.isPrintModalOpen = false; // Fechar este também para garantir uma nova montagem
    },
    closePrintModal() {
      console.log('[CRÍTICO] Fechando modal de impressão');
      this.isPrintModalOpen = false;
      
      // Limpar qualquer intervalo de debug
      if (this.debugInterval) {
        clearInterval(this.debugInterval);
        this.debugInterval = null;
      }
      
      // Reabrir o modal anterior se houver algum
      if (this.previousOpenModal) {
        console.log(`[CRÍTICO] Reabrindo modal anterior: ${this.previousOpenModal}`);
        
        // Usar setTimeout para garantir que o modal de impressão seja fechado primeiro
        setTimeout(() => {
          switch (this.previousOpenModal) {
            case 'consulta':
              this.isConsultOrdersSectionOpen = true;
              break;
            case 'dashboard':
              this.isDashboardOpen = true;
              break;
            case 'logViewer':
              this.isLogViewerOpen = true;
              break;
            case 'createOrder':
              this.isCreateOrderSectionOpen = true;
              break;
            case 'editOrder':
              this.isEditOrderOpen = true;
              break;
            case 'financialReport':
              this.isFinancialReportOpen = true;
              break;
            case 'userManagement':
              this.isUserManagementOpen = true;
              break;
          }
        }, 100);
      }
    },
    handleNewOrderFromPrintModal() {
      // Fechar o modal de impressão
      this.isPrintModalOpen = false;
      
      // Limpar qualquer modal anterior salvo pois estamos indo para outra tela
      this.previousOpenModal = null;
      
      // Abrir a tela de criação de novo pedido
      this.isCreateOrderSectionOpen = true;
    },
    async logout() {
      try {
        // Usa o serviço de autenticação para fazer logout
        await authService.logout();
        console.log("Logout realizado, redirecionando para Login");
      } catch (error) {
        console.error("Erro durante logout:", error);
      } finally {
        // Redireciona para a página de login independentemente do resultado
        this.$router.push({ name: "Login" });
      }
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
      // Salvar qual modal está aberto antes de abrir o modal de impressão
      this.savePreviousOpenModal();
      
      this.pedidoCriado = pedidoCriado;
      this.isPrintModalOpen = true;
      this.isCreateOrderSectionOpen = false;
    },
    async handleCreateOrderWithImage(pedidoCriado) {
      // Salvar qual modal está aberto antes de abrir o modal de impressão
      this.savePreviousOpenModal();
      
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
          // Não fechar o modal de impressão automaticamente
          // O usuário deve fechá-lo manualmente para voltar ao modal anterior
          // this.isPrintModalOpen = false;
          
          // Mostrar mensagem para o usuário
          alert("Imagem do pedido gerada com sucesso!");
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
    openLogViewer() {
      this.isLogViewerOpen = true;
    },
    closeLogViewer() {
      this.isLogViewerOpen = false;
    },
    // Novo método para buscar um pedido pelo ID
    async fetchPedidoById(pedidoId) {
      console.log(`Buscando detalhes completos do pedido #${pedidoId}...`);
      
      // Limpar qualquer intervalo de debug anterior
      if (this.debugInterval) {
        clearInterval(this.debugInterval);
        this.debugInterval = null;
      }
      
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          console.error("Token de autenticação não encontrado");
          alert("Sessão expirada. Faça login novamente.");
          return;
        }
        
        // Buscar todos os pedidos para encontrar este específico
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        if (response && response.data && Array.isArray(response.data)) {
          console.log(`Resposta recebida com ${response.data.length} pedidos, procurando ID #${pedidoId}`);
          
          // Encontrar o pedido pelo ID
          const pedido = response.data.find(p => p.id == pedidoId);
          
          if (pedido) {
            console.log(`Pedido #${pedidoId} encontrado:`, pedido);
            
            // Salvar qual modal está aberto antes de abrir o modal de impressão
            this.savePreviousOpenModal();
            
            // Garantir que todos os campos necessários existam
            this.pedidoCriado = {
              ...pedido,
              // Garantir que todos os campos necessários existam
              descricao: pedido.descricao || '',
              quantidade: pedido.quantidade || 0,
              urgencia: pedido.urgencia || 'Normal',
              categoria: pedido.categoria || 'Geral',
              deliveryDate: pedido.deliveryDate || new Date().toISOString().split('T')[0],
              observacao: pedido.observacao || '',
              sender: pedido.sender || (localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')).nome : '')
            };
            
            // Abrir o modal
            this.$nextTick(() => {
              this.isPrintModalOpen = true;
              console.log(`Modal de impressão aberto para o pedido #${pedidoId}`);
            });
            
            return true;
          } else {
            console.error(`Pedido #${pedidoId} não encontrado na lista`);
            // Notificar o usuário
            alert(`Pedido #${pedidoId} não encontrado. Verifique se o pedido existe.`);
            return false;
          }
        } else {
          console.error("Formato de resposta inválido:", response);
          alert("Formato de resposta inválido ao buscar pedidos.");
          return false;
        }
      } catch (error) {
        console.error("Erro ao buscar pedido:", error);
        alert("Não foi possível carregar os detalhes do pedido. Tente novamente mais tarde.");
        return false;
      }
    },
    savePreviousOpenModal() {
      // Armazenar qual modal estava aberto anteriormente
      if (this.isConsultOrdersSectionOpen) {
        this.previousOpenModal = 'consulta';
      } else if (this.isDashboardOpen) {
        this.previousOpenModal = 'dashboard';
      } else if (this.isLogViewerOpen) {
        this.previousOpenModal = 'logViewer';
      } else if (this.isCreateOrderSectionOpen) {
        this.previousOpenModal = 'createOrder';
      } else if (this.isEditOrderOpen) {
        this.previousOpenModal = 'editOrder';
      } else if (this.isFinancialReportOpen) {
        this.previousOpenModal = 'financialReport';
      } else if (this.isUserManagementOpen) {
        this.previousOpenModal = 'userManagement';
      } else {
        this.previousOpenModal = null;
      }
      console.log(`[CRÍTICO] Modal anterior salvo: ${this.previousOpenModal}`);
    },
    confirmLogout() {
      // Exibir o modal de confirmação
      this.showLogoutConfirmation = true;
    },
    proceedWithLogout() {
      // Fechar o modal de confirmação
      this.showLogoutConfirmation = false;
      // Executar o logout
      this.logout();
    },
    cancelLogout() {
      // Apenas fecha o modal de confirmação
      this.showLogoutConfirmation = false;
    },
  },
};
</script>

<style scoped>
.app-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  background-color: #2c2c2c;
}

/* Background com a logo */
.background-logo {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url('@/assets/logo.png');
  background-repeat: no-repeat;
  background-position: center center;
  background-size: 40%; /* Ajuste o tamanho conforme necessário */
  opacity: 0.1; /* Transparência da logo */
  z-index: 1;
  pointer-events: none; /* Permite clicar através da imagem */
}

/* Sidebar */
.sidebar {
  width: 16rem; /* Convertido de fixo para rem */
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #262626;
  padding: var(--spacing-lg) 0;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  overflow-y: auto;
  z-index: var(--z-index-sidebar, 100);
  box-shadow: 0.25rem 0 1.25rem rgba(0, 0, 0, 0.2);
}

/* Conteúdo principal */
.main-content {
  flex: 1;
  margin-left: 16rem; /* Alinhado com a largura da sidebar */
  width: calc(100% - 16rem); /* Largura - sidebar */
  min-height: 100vh;
  padding: var(--spacing-lg);
  background-color: transparent; /* Alterado de #2c2c2c para transparente para mostrar o background */
  overflow-y: auto;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2; /* Colocado acima do background-logo */
}

.main-content.has-content {
  padding: 0;
}

/* Botões do menu */
.menu-btn {
  display: block;
  width: 90%;
  margin: 0 auto var(--spacing-sm);
  padding: 0.875rem 1.25rem; /* Convertido de 14px 20px para rem */
  text-align: center;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: var(--font-size-md);
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.3);
}

.menu-btn:hover {
  transform: translateY(-0.1875rem); /* Convertido de -3px para rem */
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.4);
  background: linear-gradient(145deg, #444, #333);
}

.menu-btn:active {
  transform: translateY(-0.0625rem); /* Convertido de -1px para rem */
}

/* Botão para administrador */
.admin-btn {
  background: linear-gradient(145deg, #b73c3c, #9a3232);
  color: white;
}

.admin-btn:hover {
  background: linear-gradient(145deg, #c54040, #aa3636);
}

.gestor-btn {
  background: linear-gradient(145deg, #3c7bb7, #32689a);
  color: white;
}

.gestor-btn:hover {
  background: linear-gradient(145deg, #4086c5, #3673aa);
}

.finance-btn {
  background: linear-gradient(145deg, #5c3cb7, #4d329a);
  color: white;
}

.finance-btn:hover {
  background: linear-gradient(145deg, #6a44d0, #573aaa);
}

.logout-btn {
  margin-top: auto;
  background-color: #444;
  border: 0.0625rem solid #555; /* Convertido de 1px para rem */
}

.logout-btn:hover {
  background-color: #555;
}

/* Botão do menu mobile */
.open-menu-btn {
  display: none;
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 90;
  background-color: #333;
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  padding: 0.625rem 1.25rem; /* Convertido de 10px 20px para rem */
  cursor: pointer;
  box-shadow: 0 0.25rem 0.625rem rgba(0, 0, 0, 0.3);
}

/* Menu de tela cheia no mobile */
.fullscreen-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.95);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0;
  overflow-y: auto;
}

/* Novos estilos para a estrutura do menu */
.menu-header {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  position: sticky;
  top: 0;
  z-index: 1002;
  background-color: rgba(0, 0, 0, 0.8);
}

.menu-content {  
  width: 100%;  
  display: flex;  
  flex-direction: column;  
  align-items: center;  
  flex: 1;  
  overflow-y: auto;  
  padding: 1rem 0 2rem 0;  
  /* Ajustando a altura para evitar scrolling desnecessário */  
  height: auto;  
  max-height: calc(100vh - 10rem); /* Altura máxima considerando o header e o botão flutuante */
}

.menu-footer {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 1rem 0;
  position: sticky;
  bottom: 0;
  z-index: 1002;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.menu-footer .logout-btn {
  background: linear-gradient(145deg, #b73c3c, #9a3232);
  width: 80%;
  max-width: 25rem;
  margin-bottom: 0;
}

.menu-footer .logout-btn:hover {
  background: linear-gradient(145deg, #c54040, #aa3636);
}

.fullscreen-menu .menu-btn {
  margin-bottom: var(--spacing-md);
  width: 80%;
  max-width: 25rem;
}

/* Estilo para o botão fechar */
.menu-header .close-menu-btn {
  background-color: #333;
  color: white;
  border: none;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
}

/* Responsividade */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  
  .main-content {
    width: 100%;
    margin-left: 0;
    padding: var(--spacing-md);
  }
  
  .open-menu-btn {
    display: block;
  }
  
  /* Ajustes específicos para mobile */
  .fullscreen-menu {
    max-height: 100vh;
    overflow-y: auto;
    justify-content: flex-start;
    padding: 0;
    padding-bottom: 6rem; /* Espaço adicional para garantir que conteúdo não fique sob o botão flutuante */
  }
  
  .menu-header {
    padding: 1rem;
    background-color: rgba(0, 0, 0, 0.8);
  }
  
  .menu-content {
    padding: 0.5rem 0 5rem 0; /* Padding inferior maior para evitar que o conteúdo fique sob o botão flutuante */
    flex: 1;
    max-height: none; /* Deixar o conteúdo fluir normalmente */
  }
  
  /* Garantir espaçamento adequado entre botões no mobile */
  .menu-content .menu-btn {
    margin-bottom: 0.8rem;
  }
  
  /* Ajustar botão flutuante em diferentes orientações de tela */
  @media (orientation: landscape) {
    .floating-logout-btn {
      bottom: 3rem;
      padding: 0.8rem;
      font-size: 1.1rem;
    }
  }
}

/* Otimizações para tablets e telas 1024x768 */
@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar {
    width: 12.5rem; /* Convertido de 200px para rem */
  }
  
  .main-content {
    width: calc(100% - 12.5rem);
    margin-left: 12.5rem;
    padding: var(--spacing-lg);
  }
  
  .menu-btn {
    font-size: 0.875rem; /* Convertido de 14px para rem */
    padding: 0.625rem 0.9375rem; /* Convertido de 10px 15px para rem */
  }
}

/* Otimizações para telas entre 1025px e 1200px */
@media (min-width: 1025px) and (max-width: 1200px) {
  .main-content {
    padding: var(--spacing-lg);
  }
}

/* Otimizações para telas Full HD (1920x1080) */
@media (min-width: 1367px) and (max-width: 1920px) {
  .main-content {
    padding: 2.5rem 3.75rem; /* Convertido de 40px 60px para rem */
  }
  
  .sidebar {
    width: 16.875rem; /* Convertido de 270px para rem */
  }
  
  .main-content {
    width: calc(100% - 16.875rem);
    margin-left: 16.875rem;
  }
  
  .menu-btn {
    padding: 0.9375rem 1.5625rem; /* Convertido de 15px 25px para rem */
    font-size: 1.125rem; /* Convertido de 18px para rem */
  }
}

/* Otimizações para telas maiores que Full HD */
@media (min-width: 1921px) {
  .sidebar {
    width: 18.75rem; /* Convertido de 300px para rem */
  }
  
  .main-content {
    width: calc(100% - 18.75rem);
    margin-left: 18.75rem;
    padding: 3.125rem 5rem; /* Convertido de 50px 80px para rem */
  }
  
  .menu-btn {
    padding: 1.125rem 1.875rem; /* Convertido de 18px 30px para rem */
    font-size: 1.25rem; /* Convertido de 20px para rem */
    margin-bottom: 0.9375rem; /* Convertido de 15px para rem */
  }
}

/* Estilos para seções específicas */
.order-section {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 0;
  background-color: transparent;
}

/* Container de alta prioridade para modais */
.high-priority-modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 99999;
}

.high-priority-modal-container > * {
  pointer-events: auto;
}

/* Espaçador antes do botão Sair */
.logout-spacer {
  flex-grow: 1;
  min-height: 2rem;
  margin-top: 1rem;
}

/* Estilo para o botão Sair */
.logout-btn {
  background: linear-gradient(145deg, #b73c3c, #9a3232);
  color: white;
  font-weight: bold;
}

.logout-btn:hover {
  background: linear-gradient(145deg, #c54040, #aa3636);
}

/* Modal de Confirmação de Logout Moderno */.logout-modal-overlay {  position: fixed;  top: 0;  left: 0;  width: 100%;  height: 100%;  display: flex;  align-items: center;  justify-content: center;  background-color: rgba(0, 0, 0, 0.85);  z-index: 10000;  backdrop-filter: blur(5px);  animation: fadeIn 0.3s ease-out;  padding: var(--spacing-md);  box-sizing: border-box;}.logout-modal-content {  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);  border-radius: var(--border-radius-lg);  max-width: 90%;  width: 28rem;  box-shadow: 0 1rem 2rem rgba(0, 0, 0, 0.6);  animation: slideUp 0.3s ease-out;  overflow: hidden;  border: 1px solid #444;}.logout-modal-header {  padding: var(--spacing-lg);  border-bottom: 1px solid #444;  display: flex;  align-items: center;  justify-content: space-between;  background-color: rgba(255, 111, 97, 0.1);  position: relative;}.logout-icon {  display: flex;  align-items: center;  justify-content: center;  width: 3rem;  height: 3rem;  background: linear-gradient(145deg, #ff6f61, #e74c3c);  border-radius: 50%;  margin-right: var(--spacing-md);  box-shadow: 0 0.25rem 0.5rem rgba(255, 111, 97, 0.3);}.logout-icon i {  color: white;  font-size: 1.5rem;}.logout-modal-header h3 {  margin: 0;  font-size: var(--font-size-xl);  color: #f5f5f5;  font-weight: 600;  flex: 1;}.close-modal-btn {  background: none;  border: none;  color: #999;  font-size: var(--font-size-lg);  cursor: pointer;  display: flex;  align-items: center;  justify-content: center;  width: 2.5rem;  height: 2.5rem;  border-radius: 50%;  transition: all 0.3s ease;}.close-modal-btn:hover {  background-color: rgba(255, 255, 255, 0.1);  color: #ff6f61;  transform: rotate(90deg);}.logout-modal-body {  padding: var(--spacing-lg);  text-align: center;}.logout-modal-body p {  margin: 0 0 var(--spacing-md) 0;  color: #f5f5f5;  font-size: var(--font-size-lg);  font-weight: 500;}.logout-warning {  display: flex;  align-items: center;  justify-content: center;  background-color: rgba(255, 193, 7, 0.1);  border: 1px solid rgba(255, 193, 7, 0.3);  border-radius: var(--border-radius-md);  padding: var(--spacing-sm) var(--spacing-md);  margin-top: var(--spacing-md);}.logout-warning i {  color: #ffc107;  margin-right: var(--spacing-sm);  font-size: var(--font-size-lg);}.logout-warning span {  color: #ddd;  font-size: var(--font-size-sm);}.logout-modal-footer {  padding: var(--spacing-lg);  border-top: 1px solid #444;  display: flex;  justify-content: flex-end;  gap: var(--spacing-md);  background-color: rgba(0, 0, 0, 0.2);}.logout-cancel-btn, .logout-confirm-btn {  display: flex;  align-items: center;  padding: var(--spacing-sm) var(--spacing-lg);  border: none;  border-radius: var(--border-radius-md);  font-size: var(--font-size-md);  font-weight: 600;  cursor: pointer;  transition: all 0.3s ease;  gap: var(--spacing-xs);  min-width: 8rem;  justify-content: center;}.logout-cancel-btn {  background: linear-gradient(145deg, #555, #444);  color: #f5f5f5;  border: 1px solid #666;}.logout-cancel-btn:hover {  background: linear-gradient(145deg, #666, #555);  transform: translateY(-0.125rem);  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.3);}.logout-confirm-btn {  background: linear-gradient(145deg, #ff6f61, #e74c3c);  color: white;  border: 1px solid #ff6f61;  position: relative;  overflow: hidden;}.logout-confirm-btn::before {  content: '';  position: absolute;  top: 0;  left: -100%;  width: 100%;  height: 100%;  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);  transition: left 0.5s;}.logout-confirm-btn:hover::before {  left: 100%;}.logout-confirm-btn:hover {  background: linear-gradient(145deg, #e74c3c, #c0392b);  transform: translateY(-0.125rem);  box-shadow: 0 0.25rem 0.5rem rgba(231, 76, 60, 0.4);}.logout-confirm-btn:active {  transform: translateY(0);}/* Animações */@keyframes fadeIn {  from {    opacity: 0;  }  to {    opacity: 1;  }}@keyframes slideUp {  from {    opacity: 0;    transform: translateY(2rem) scale(0.9);  }  to {    opacity: 1;    transform: translateY(0) scale(1);  }}

/* Ajustes específicos para botão Sair no sidebar */
.sidebar .logout-btn {
  width: 90%;
  margin: 0 auto;
}

/* Responsividade para o Modal de Logout */@media (max-width: 768px) {  .logout-modal-content {    width: 95%;    max-width: 95%;  }    .logout-modal-header {    padding: var(--spacing-md);  }    .logout-modal-header h3 {    font-size: var(--font-size-lg);  }    .logout-icon {    width: 2.5rem;    height: 2.5rem;    margin-right: var(--spacing-sm);  }    .logout-icon i {    font-size: 1.25rem;  }    .logout-modal-body {    padding: var(--spacing-md);  }    .logout-modal-body p {    font-size: var(--font-size-md);  }    .logout-warning {    flex-direction: column;    text-align: center;    gap: var(--spacing-xs);  }    .logout-warning i {    margin-right: 0;    margin-bottom: var(--spacing-xs);  }    .logout-modal-footer {    padding: var(--spacing-md);    flex-direction: column;    gap: var(--spacing-sm);  }    .logout-cancel-btn, .logout-confirm-btn {    width: 100%;    padding: var(--spacing-md);    font-size: var(--font-size-md);  }}@media (max-width: 480px) {  .logout-modal-overlay {    padding: var(--spacing-sm);  }    .logout-modal-content {    width: 98%;  }    .logout-modal-header {    padding: var(--spacing-sm);  }    .logout-modal-header h3 {    font-size: var(--font-size-md);  }    .logout-icon {    width: 2rem;    height: 2rem;  }    .logout-icon i {    font-size: 1rem;  }    .logout-modal-body {    padding: var(--spacing-sm);  }    .logout-modal-body p {    font-size: var(--font-size-sm);  }    .logout-warning span {    font-size: var(--font-size-xs);  }    .logout-modal-footer {    padding: var(--spacing-sm);  }    .logout-cancel-btn, .logout-confirm-btn {    padding: var(--spacing-sm);    font-size: var(--font-size-sm);    min-width: auto;  }}

/* Botão sair flutuante para mobile */
.floating-logout-btn {
  position: fixed;
  bottom: 4.5rem; /* Posicionado mais alto para evitar a barra do navegador */
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  max-width: 20rem;
  padding: 1.25rem;
  background: linear-gradient(145deg, #b73c3c, #9a3232);
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
  border: none;
  border-radius: 0.5rem;
  box-shadow: 0 0.25rem 1rem rgba(0, 0, 0, 0.4);
  z-index: 1010; /* Garantir que esteja acima de tudo */
  cursor: pointer;
  animation: pulse 2s infinite; /* Adicionar animação para chamar atenção */
}

.floating-logout-btn:active {
  background: linear-gradient(145deg, #c54040, #aa3636);
  transform: translateX(-50%) scale(0.98);
  animation: none; /* Parar animação ao clicar */
}

/* Animação de pulse para chamar atenção */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(183, 60, 60, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(183, 60, 60, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(183, 60, 60, 0);
  }
}

@media (max-height: 600px) {
  /* Para telas muito pequenas em altura */
  .floating-logout-btn {
    bottom: 3.5rem;
    padding: 0.75rem;
  }
}
</style>
