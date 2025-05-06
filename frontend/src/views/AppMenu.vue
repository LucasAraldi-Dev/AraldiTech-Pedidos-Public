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
      <!-- Botão Dashboard apenas para gestores -->
      <button 
        v-if="isGestor" 
        class="menu-btn gestor-btn" 
        @click="openDashboard"
      >
        Dashboard de Gestão
      </button>
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

    <div class="main-content" :class="{'has-content': isDashboardOpen || isCreateOrderSectionOpen || isConsultOrdersSectionOpen || isPrintModalOpen || isEditOrderOpen || isUserManagementOpen}">
      <!-- Dashboard para Gestores -->
      <div v-if="isDashboardOpen && isGestor" class="dashboard-grid">
        <h1 class="dashboard-title">Dashboard de Gestão</h1>
        
        <!-- Primeira linha: KPIs -->
        <div class="dashboard-row kpi-row">
          <div class="kpi-card">
            <h3>Total de Pedidos</h3>
            <div class="kpi-value">{{ totalPedidos }}</div>
          </div>
          <div class="kpi-card">
            <h3>Tempo Médio de Conclusão</h3>
            <div class="kpi-value">{{ tempoMedioConclusao }}</div>
          </div>
          <div class="kpi-card">
            <h3>Pedidos Pendentes</h3>
            <div class="kpi-value">{{ pedidosPendentes }}</div>
          </div>
        </div>
        
        <!-- Segunda linha: Gráficos -->
        <div class="dashboard-row chart-row">
          <div class="chart-wrapper">
            <h3>Pedidos por Status</h3>
            <canvas ref="statusChart"></canvas>
          </div>
          <div class="chart-wrapper">
            <h3>Pedidos por Categoria</h3>
            <canvas ref="categoryChart"></canvas>
          </div>
          <div class="chart-wrapper">
            <h3>Pedidos por Urgência</h3>
            <canvas ref="urgencyChart"></canvas>
          </div>
        </div>
        
        <!-- Terceira linha: Atividades e Relatórios -->
        <div class="dashboard-row split-row">
          <!-- Feed de atividades -->
          <div class="activities-section">
            <h2>Atividades Recentes</h2>
            <div class="activity-feed">
              <div v-if="isLoading" class="loading">Carregando atividades...</div>
              <div v-else-if="activities.length === 0" class="empty-feed">
                Nenhuma atividade recente encontrada.
              </div>
              <div v-else class="activity-list">
                <div v-for="activity in activities" :key="activity.id" class="activity-item">
                  <div class="activity-icon" :class="getActivityIcon(activity.tipo)">
                    <i :class="getActivityIconClass(activity.tipo)"></i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-header">
                      <span class="activity-user">{{ activity.usuario_nome }}</span>
                      <span class="activity-date">{{ formatDate(activity.data) }}</span>
                    </div>
                    <div class="activity-description">{{ activity.descricao }}</div>
                    <div v-if="activity.pedido_id" class="activity-details">
                      <a @click="openOrderDetailsFromActivity(activity.pedido_id)" class="view-order-btn">Ver pedido #{{ activity.pedido_id }}</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Geração de Relatórios -->
          <div class="reports-section">
            <h2>Relatórios</h2>
            <div class="report-options">
              <div class="form-group">
                <label for="reportType">Tipo:</label>
                <select id="reportType" v-model="reportOptions.tipo">
                  <option value="pedidos">Pedidos</option>
                  <option value="atividades">Atividades</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="reportPeriod">Período:</label>
                <select id="reportPeriod" v-model="reportOptions.periodo">
                  <option value="diario">Diário</option>
                  <option value="semanal">Semanal</option>
                  <option value="mensal">Mensal</option>
                  <option value="personalizado">Personalizado</option>
                </select>
              </div>
              
              <div class="date-range" v-if="reportOptions.periodo === 'personalizado'">
                <div class="form-group">
                  <label for="startDate">Data Inicial:</label>
                  <input type="date" id="startDate" v-model="reportOptions.dataInicial">
                </div>
                <div class="form-group">
                  <label for="endDate">Data Final:</label>
                  <input type="date" id="endDate" v-model="reportOptions.dataFinal">
                </div>
              </div>
              
              <div class="form-group">
                <label for="reportFormat">Formato:</label>
                <select id="reportFormat" v-model="reportOptions.formato">
                  <option value="pdf">PDF</option>
                  <option value="excel">Excel</option>
                </select>
              </div>
              
              <button class="btn-generate" @click="generateReport">Gerar Relatório</button>
            </div>
          </div>
        </div>
      </div>
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
  </div>
</template>

<script>
import ModalCriarPedido from "@/components/ModalCriarPedido.vue";
import ModalConsultaPedidos from "@/components/ModalConsultaPedidos.vue";
import ModalEditarPedido from "@/components/ModalEditarPedido.vue";
import ModalImprimirPedido from "@/components/ModalImprimirPedido.vue";
import ModalGerenciarUsuarios from "@/components/ModalGerenciarUsuarios.vue";
import html2canvas from "html2canvas";
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import { Chart, registerables } from 'chart.js';

// Registrar todos os componentes do Chart.js
Chart.register(...registerables);

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
      isGestor: false,
      isDashboardOpen: false,
      // Dashboard data
      totalPedidos: 0,
      tempoMedioConclusao: '0 dias',
      pedidosPendentes: 0,
      isLoading: true,
      activities: [],
      charts: {
        status: null,
        category: null,
        urgency: null
      },
      reportOptions: {
        tipo: 'pedidos',
        periodo: 'diario',
        dataInicial: this.getDefaultStartDate(),
        dataFinal: this.formatDateForInput(new Date()),
        formato: 'pdf',
      },
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
    // Limpar os gráficos do Chart.js para evitar vazamento de memória
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
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
    // Métodos do Dashboard
    openDashboard() {
      this.isDashboardOpen = true;
      this.isMenuOpen = false;
      this.fetchDashboardData();
    },
    async fetchDashboardData() {
      this.isLoading = true;
      try {
        // Carrega pedidos
        await this.fetchPedidosForDashboard();
        
        // Carrega atividades recentes
        await this.fetchActivities();
        
        // Inicializa gráficos após carregar os dados
        this.$nextTick(() => {
          this.initCharts();
        });
      } catch (error) {
        console.error("Erro ao carregar dados do dashboard:", error);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchPedidosForDashboard() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        });
        this.orders = response.data;
        this.totalPedidos = this.orders.length;
        this.pedidosPendentes = this.orders.filter(p => p.status === 'Pendente').length;
        
        // Calcula tempo médio de conclusão
        const pedidosConcluidos = this.orders.filter(p => p.status === 'Concluído');
        if (pedidosConcluidos.length > 0) {
          let totalDias = 0;
          pedidosConcluidos.forEach(pedido => {
            const dataCriacao = new Date(pedido.criacao_data || pedido.deliveryDate);
            const dataConclusao = new Date(pedido.conclusao_data || new Date());
            const diffTime = Math.abs(dataConclusao - dataCriacao);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            totalDias += diffDays;
          });
          const mediaDias = totalDias / pedidosConcluidos.length;
          this.tempoMedioConclusao = `${mediaDias.toFixed(1)} dias`;
        }
      } catch (error) {
        console.error("Erro ao carregar pedidos:", error);
      }
    },
    async fetchActivities() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/atividades`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` },
        });
        this.activities = response.data;
      } catch (error) {
        console.error("Erro ao carregar atividades:", error);
      }
    },
    initCharts() {
      // Destruir gráficos existentes antes de criar novos
      Object.entries(this.charts).forEach(([key, chart]) => {
        if (chart) {
          chart.destroy();
          this.charts[key] = null;
        }
      });
      
      // Inicializar os novos gráficos
      this.initStatusChart();
      this.initCategoryChart();
      this.initUrgencyChart();
    },
    initStatusChart() {
      const ctx = this.$refs.statusChart?.getContext('2d');
      if (!ctx) return;
      
      // Contagem de pedidos por status
      const statusCounts = {};
      this.orders.forEach(pedido => {
        const status = pedido.status || 'Não definido';
        statusCounts[status] = (statusCounts[status] || 0) + 1;
      });
      
      // Cores para cada status
      const statusColors = {
        'Pendente': '#FFD700',
        'Em Andamento': '#1E90FF',
        'Concluído': '#32CD32',
        'Cancelado': '#FF6347',
        'Não definido': '#A9A9A9'
      };
      
      // Prepara dados para o gráfico
      const labels = Object.keys(statusCounts);
      const data = Object.values(statusCounts);
      const colors = labels.map(label => statusColors[label] || '#A9A9A9');
      
      // Cria o gráfico
      this.charts.status = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    },
    initCategoryChart() {
      const ctx = this.$refs.categoryChart?.getContext('2d');
      if (!ctx) return;
      
      // Contagem de pedidos por categoria
      const categoryCounts = {};
      this.orders.forEach(pedido => {
        const categoria = pedido.categoria || 'Não categorizado';
        categoryCounts[categoria] = (categoryCounts[categoria] || 0) + 1;
      });
      
      // Prepara dados para o gráfico
      const labels = Object.keys(categoryCounts);
      const data = Object.values(categoryCounts);
      
      // Cria o gráfico
      this.charts.category = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Pedidos por Categoria',
            data: data,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0,
                color: '#f5f5f5'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            },
            x: {
              ticks: {
                color: '#f5f5f5'
              },
              grid: {
                color: 'rgba(255, 255, 255, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              labels: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    },
    initUrgencyChart() {
      const ctx = this.$refs.urgencyChart?.getContext('2d');
      if (!ctx) return;
      
      // Contagem de pedidos por urgência
      const urgencyCounts = {};
      this.orders.forEach(pedido => {
        const urgencia = pedido.urgencia || 'Normal';
        urgencyCounts[urgencia] = (urgencyCounts[urgencia] || 0) + 1;
      });
      
      // Cores para cada nível de urgência
      const urgencyColors = {
        'Normal': '#32CD32',
        'Urgente': '#FFD700',
        'Crítico': '#FF6347',
        'Não definido': '#A9A9A9'
      };
      
      // Prepara dados para o gráfico
      const labels = Object.keys(urgencyCounts);
      const data = Object.values(urgencyCounts);
      const colors = labels.map(label => urgencyColors[label] || '#A9A9A9');
      
      // Cria o gráfico
      this.charts.urgency = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f5f5f5'
              }
            }
          }
        }
      });
    },
    getDefaultStartDate() {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      return this.formatDateForInput(date);
    },
    formatDateForInput(date) {
      if (!date) return '';
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    async generateReport() {
      try {
        // Construir parâmetros do relatório
        const params = {
          tipo: this.reportOptions.tipo,
          periodo: this.reportOptions.periodo,
          formato: this.reportOptions.formato
        };
        
        // Adicionar datas se for personalizado
        if (this.reportOptions.periodo === 'personalizado') {
          params.dataInicial = this.reportOptions.dataInicial;
          params.dataFinal = this.reportOptions.dataFinal;
        }
        
        // Chamar API para gerar relatório
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/relatorios`, {
          params: params,
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            'Accept': this.reportOptions.formato === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          },
          responseType: 'blob'
        });
        
        // Criar link para download
        const blob = new Blob([response.data], {
          type: this.reportOptions.formato === 'pdf' ? 'application/pdf' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        // Nome do arquivo
        const dataAtual = new Date().toISOString().split('T')[0];
        const extensao = this.reportOptions.formato === 'pdf' ? 'pdf' : 'xlsx';
        a.download = `relatorio_${this.reportOptions.tipo}_${dataAtual}.${extensao}`;
        
        // Disparar download
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        alert('Erro ao gerar relatório. Por favor, tente novamente.');
      }
    },
    getActivityIcon(tipo) {
      const tipoMap = {
        'criacao': 'activity-icon-create',
        'edicao': 'activity-icon-edit',
        'conclusao': 'activity-icon-complete',
        'cancelamento': 'activity-icon-cancel',
        'login': 'activity-icon-login',
        'registro': 'activity-icon-register'
      };
      return tipoMap[tipo] || 'activity-icon-default';
    },
    getActivityIconClass(tipo) {
      const iconMap = {
        'criacao': 'fas fa-plus',
        'edicao': 'fas fa-edit',
        'conclusao': 'fas fa-check',
        'cancelamento': 'fas fa-times',
        'login': 'fas fa-sign-in-alt',
        'registro': 'fas fa-user-plus'
      };
      return iconMap[tipo] || 'fas fa-info';
    },
    formatDate(date) {
      if (!date) return '';
      const options = { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      };
      return new Date(date).toLocaleDateString('pt-BR', options);
    },
    openOrderDetailsFromActivity(pedidoId) {
      // Encontrar o pedido pelo ID
      const pedido = this.orders.find(p => p.id === pedidoId);
      if (pedido) {
        // Usar o mesmo modal de impressão/visualização que é usado na consulta
        this.pedidoCriado = pedido;
        this.isPrintModalOpen = true;
      } else {
        console.error(`Pedido #${pedidoId} não encontrado`);
      }
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

.gestor-btn {
  background-color: #2ecc71; /* Verde para indicar ações de gestão */
}

.gestor-btn:hover {
  background-color: #27ae60;
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
}

@media (max-width: 1200px) and (min-width: 769px) {
  .chart-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .chart-wrapper:last-child {
    grid-column: span 2;
  }
}
</style>
