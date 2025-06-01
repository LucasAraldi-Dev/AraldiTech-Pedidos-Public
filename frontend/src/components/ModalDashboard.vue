<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" @click.stop>
      <!-- Header do Modal -->
      <div class="modal-header">
        <div class="header-content">
          <div class="header-title">
            <i class="material-icons">dashboard</i>
            <h2>Dashboard de Gestão</h2>
          </div>
          <div class="header-actions">
            <button class="refresh-btn" @click="refreshAllData" :disabled="isRefreshing">
              <i class="material-icons" :class="{ 'spinning': isRefreshing }">refresh</i>
              <span>{{ isRefreshing ? 'Atualizando...' : 'Atualizar' }}</span>
            </button>
            <button class="close-btn" @click="$emit('close')">
              <i class="material-icons">close</i>
            </button>
          </div>
        </div>
        

      </div>
        
      <!-- Navegação por Abas -->
      <div class="tabs-navigation">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          class="tab-button"
          :class="{ 'active': activeTab === tab.id }"
          @click="setActiveTab(tab.id)"
        >
          <i class="material-icons">{{ tab.icon }}</i>
          <span>{{ tab.label }}</span>
          <div v-if="tab.badge" class="tab-badge">{{ tab.badge }}</div>
        </button>
      </div>
            
      <!-- Conteúdo das Abas -->
      <div class="dashboard-content">
        <!-- Loading Global -->
        <div v-if="isLoading" class="dashboard-loading">
          <LoadingIndicator message="Carregando dados do dashboard..." size="large" />
        </div>
              
        <!-- Todas as abas ficam montadas, apenas alternamos visibilidade -->
        <div v-else class="tabs-container">
          <!-- Aba: Visão Geral -->
          <div 
            class="tab-content overview-tab" 
            :class="{ 'tab-active': activeTab === 'overview', 'tab-hidden': activeTab !== 'overview' }"
          >
            <DashboardOverview 
              :pedidos="pedidos"
              :activities="activities"
              :is-loading="false"
              @refresh="refreshOverview"
            />
          </div>
                
          <!-- Aba: Análise -->
          <div 
            class="tab-content analytics-tab" 
            :class="{ 'tab-active': activeTab === 'analytics', 'tab-hidden': activeTab !== 'analytics' }"
          >
            <DashboardAnalytics 
              :pedidos="pedidos"
              :is-loading="false"
              @refresh="refreshAnalytics"
            />
          </div>
                
          <!-- Aba: Financeiro -->
          <div 
            class="tab-content financial-tab" 
            :class="{ 'tab-active': activeTab === 'financial', 'tab-hidden': activeTab !== 'financial' }"
          >
            <DashboardFinancial 
              :pedidos="pedidos"
              :is-loading="false"
              @refresh="refreshFinancial"
              @view-details="openFinancialDetails"
            />
          </div>
            
          <!-- Aba: Relatórios -->
          <div 
            class="tab-content reports-tab" 
            :class="{ 'tab-active': activeTab === 'reports', 'tab-hidden': activeTab !== 'reports' }"
          >
            <!-- Aviso de Fase de Testes -->
            <div class="test-warning-banner">
              <div class="warning-content">
                <i class="material-icons warning-icon">science</i>
                <div class="warning-text">
                  <h4>🧪 Funcionalidade em Fase de Testes</h4>
                  <p>
                    O sistema de relatórios está em desenvolvimento e pode apresentar instabilidades. 
                    Estamos trabalhando para melhorar a experiência. Agradecemos sua compreensão!
                  </p>
                </div>
              </div>
            </div>
            
            <DashboardReports 
              :is-loading="false"
              @generate-report="handleGenerateReport"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
              
  <!-- Modal de Detalhes Financeiros -->
  <ModalFinanceiro
    v-if="showFinancialDetails"
    :isOpen="showFinancialDetails"
    @close="closeFinancialDetails"
  />
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useToast } from 'vue-toastification';
import authService from '@/api/authService';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';
import ModalFinanceiro from '@/components/ModalFinanceiro.vue';
import DashboardOverview from '@/components/dashboard/DashboardOverview.vue';
import DashboardAnalytics from '@/components/dashboard/DashboardAnalytics.vue';
import DashboardFinancial from '@/components/dashboard/DashboardFinancial.vue';
import DashboardReports from '@/components/dashboard/DashboardReports.vue';

export default {
  name: 'ModalDashboard',
  components: {
    LoadingIndicator,
    ModalFinanceiro,
    DashboardOverview,
    DashboardAnalytics,
    DashboardFinancial,
    DashboardReports
  },
  emits: ['close'],
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const toast = useToast();
    
    // Estado reativo
    const activeTab = ref('overview');
    const isLoading = ref(false);
    const isRefreshing = ref(false);
    const dataFromCache = ref(false);
    const showFinancialDetails = ref(false);
    
    // Estados de loading por aba
    const isLoadingOverview = ref(false);
    const isLoadingAnalytics = ref(false);
    const isLoadingFinancial = ref(false);
    const isLoadingReports = ref(false);
    
    // Dados
    const pedidos = ref([]);
    const activities = ref([]);
    
    // Configuração das abas
    const tabs = computed(() => [
      {
        id: 'overview',
        label: 'Visão Geral',
        icon: 'dashboard',
        badge: pedidos.value.length || null
      },
      {
        id: 'analytics',
        label: 'Análise',
        icon: 'analytics'
      },
      {
        id: 'financial',
        label: 'Financeiro',
        icon: 'account_balance'
      },
      {
        id: 'reports',
        label: 'Relatórios',
        icon: 'description'
      }
    ]);

    // Cache options (configuração para futuras implementações)
    // const cacheOptions = {
    //   dashboard: {
    //     enabled: true,
    //     ttl: 5 * 60 * 1000 // 5 minutos
    //   },
    //   activities: {
    //     enabled: true,
    //     ttl: 2 * 60 * 1000 // 2 minutos
    //   }
    // };

    // Métodos
    const setActiveTab = (tabId) => {
      // Simplesmente mudar a aba ativa - sem destruir componentes
      activeTab.value = tabId;
      
      // Carregar dados apenas se necessário
      if (pedidos.value.length === 0) {
        switch (tabId) {
          case 'overview':
            if (!isLoadingOverview.value) {
              refreshOverview();
            }
            break;
          case 'analytics':
            if (!isLoadingAnalytics.value) {
              refreshAnalytics();
            }
            break;
          case 'financial':
            if (!isLoadingFinancial.value) {
              refreshFinancial();
            }
            break;
        }
      }
    };



    const fetchPedidos = async () => {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: {
            ...authService.getAuthHeaders(),
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
          }
        });
        
        if (!response.ok) throw new Error('Erro ao buscar pedidos');
        
        const data = await response.json();
        pedidos.value = data || [];
        dataFromCache.value = false;
      } catch (error) {
        console.error('Erro ao buscar pedidos:', error);
        throw error;
      }
    };

    const fetchActivities = async () => {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/atividades`, {
          headers: {
            ...authService.getAuthHeaders(),
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
          }
        });
        
        if (!response.ok) throw new Error('Erro ao buscar atividades');
        
        const data = await response.json();
        activities.value = data || [];
        dataFromCache.value = false;
      } catch (error) {
        console.error('Erro ao buscar atividades:', error);
        // Não mostrar erro para atividades, pois não é crítico
        activities.value = [];
      }
    };

    const loadInitialData = async () => {
      isLoading.value = true;
      try {
        await Promise.all([
          fetchPedidos(),
          fetchActivities()
        ]);
      } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
        toast.error('Erro ao carregar dados do dashboard');
      } finally {
        isLoading.value = false;
      }
    };

    const refreshAllData = async () => {
      isRefreshing.value = true;
      try {
        await Promise.all([
          fetchPedidos(),
          fetchActivities()
        ]);
        toast.success('Dados atualizados com sucesso!');
      } catch (error) {
        console.error('Erro ao atualizar dados:', error);
        toast.error('Erro ao atualizar dados');
      } finally {
        isRefreshing.value = false;
      }
    };

    const refreshOverview = async () => {
      isLoadingOverview.value = true;
      try {
        await Promise.all([
          fetchPedidos(),
          fetchActivities()
        ]);
      } catch (error) {
        console.error('Erro ao atualizar visão geral:', error);
      } finally {
        isLoadingOverview.value = false;
      }
    };

    const refreshAnalytics = async () => {
      isLoadingAnalytics.value = true;
      try {
        await fetchPedidos();
      } catch (error) {
        console.error('Erro ao atualizar análises:', error);
      } finally {
        isLoadingAnalytics.value = false;
      }
    };

    const refreshFinancial = async () => {
      isLoadingFinancial.value = true;
      try {
        await fetchPedidos();
      } catch (error) {
        console.error('Erro ao atualizar dados financeiros:', error);
      } finally {
        isLoadingFinancial.value = false;
      }
    };

    const refreshReports = async () => {
      isLoadingReports.value = true;
      try {
        // Simular carregamento de relatórios
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error('Erro ao atualizar relatórios:', error);
      } finally {
        isLoadingReports.value = false;
      }
    };

    const openFinancialDetails = () => {
      showFinancialDetails.value = true;
    };

    const closeFinancialDetails = () => {
      showFinancialDetails.value = false;
    };

    const handleGenerateReport = async (reportData) => {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/relatorios`, {
          method: 'POST',
          headers: {
            ...authService.getAuthHeaders(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(reportData)
        });

        if (!response.ok) throw new Error('Erro ao gerar relatório');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `relatorio_${Date.now()}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        toast.success('Relatório gerado com sucesso!');
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        toast.error('Erro ao gerar relatório');
      }
    };

    // Watchers
    watch(() => props.isOpen, (newValue) => {
      if (newValue) {
        activeTab.value = 'overview';
        loadInitialData();
      }
    });

    // Lifecycle
    onMounted(() => {
      if (props.isOpen) {
        loadInitialData();
      }
    });

    onUnmounted(() => {
      // Cleanup se necessário
    });

    return {
      // Estado
      activeTab,
      isLoading,
      isRefreshing,
      dataFromCache,
      showFinancialDetails,
      isLoadingOverview,
      isLoadingAnalytics,
      isLoadingFinancial,
      isLoadingReports,
      
      // Dados
      pedidos,
      activities,
      tabs,
      
      // Métodos
      setActiveTab,
      refreshAllData,
      refreshOverview,
      refreshAnalytics,
      refreshFinancial,
      refreshReports,
      openFinancialDetails,
      closeFinancialDetails,
      handleGenerateReport
    };
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  z-index: var(--z-index-modal);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: var(--spacing-md);
  box-sizing: border-box;
}

.modal-content {
  background-color: #1f1f1f;
  color: #f5f5f5;
  border-radius: var(--border-radius-lg);
  width: 100%;
  max-width: 1400px;
  height: 90vh;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  border: 1px solid #333;
  overflow: hidden;
}

/* Header */
.modal-header {
  background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
  border-bottom: 1px solid #333;
  padding: var(--spacing-lg);
  flex-shrink: 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-sm);
}

.header-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.header-title i {
  color: #ff6f61;
  font-size: var(--font-size-xl);
}

.header-title h2 {
  margin: 0;
  color: #f5f5f5;
  font-size: var(--font-size-lg);
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.refresh-btn, .close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: var(--font-size-sm);
}

.refresh-btn:hover:not(:disabled), .close-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.close-btn {
  padding: var(--spacing-xs);
}

.close-btn:hover {
  background: rgba(255, 111, 97, 0.2);
  border-color: #ff6f61;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}



/* Tabs Navigation */
.tabs-navigation {
  display: flex;
  background: #2a2a2a;
  border-bottom: 1px solid #333;
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
  justify-content: center;
  flex-shrink: 0;
  height: 60px;
  align-items: center;
}

.tabs-navigation::-webkit-scrollbar {
  height: 4px;
}

.tabs-navigation::-webkit-scrollbar-track {
  background: #333;
}

.tabs-navigation::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 2px;
}

.tab-button {
  background: none;
  border: none;
  color: #ccc;
  padding: var(--spacing-md) var(--spacing-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  position: relative;
  font-size: var(--font-size-sm);
  font-weight: 500;
  width: 180px;
  justify-content: center;
  flex-shrink: 0;
}



.tab-button:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f5f5f5;
}

.tab-button.active {
  color: #fff;
  border-bottom-color: #ff6f61;
  background: linear-gradient(135deg, rgba(255, 111, 97, 0.15), rgba(255, 111, 97, 0.05));
  box-shadow: 0 2px 8px rgba(255, 111, 97, 0.3);
}

.tab-button i {
  font-size: var(--font-size-md);
  flex-shrink: 0;
}

.tab-badge {
  background: #ff6f61;
  color: white;
  font-size: var(--font-size-xs);
  padding: 0.125rem 0.375rem;
  border-radius: 0.75rem;
  min-width: 1.25rem;
  text-align: center;
  font-weight: 600;
  flex-shrink: 0;
}

/* Dashboard Content */
.dashboard-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.dashboard-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  flex: 1;
}

.tabs-container {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.tab-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  padding: var(--spacing-lg);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.tab-content.tab-active {
  opacity: 1;
  visibility: visible;
  z-index: 1;
}

.tab-content.tab-hidden {
  opacity: 0;
  visibility: hidden;
  z-index: 0;
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-overlay {
    padding: var(--spacing-sm);
  }

  .modal-content {
    max-width: 100%;
    height: 95vh;
    max-height: 95vh;
  }

  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .header-actions {
    justify-content: space-between;
  }

  .tabs-navigation {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    height: 55px;
  }

  .tab-button {
    padding: var(--spacing-sm) var(--spacing-md);
    width: 140px;
  }

  .tab-content {
    padding: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: var(--spacing-xs);
  }

  .modal-content {
    height: 98vh;
    max-height: 98vh;
  }

  .header-title h2 {
    font-size: var(--font-size-md);
  }

  .tabs-navigation {
    height: 50px;
  }

  .tab-button {
    padding: var(--spacing-sm);
    width: 120px;
    font-size: var(--font-size-xs);
  }

  .tab-button span {
    display: block;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .tab-content {
    padding: var(--spacing-sm);
  }
}

/* Ajustes específicos para telas muito pequenas */
@media (max-width: 360px) {
  .tab-button {
    width: 100px;
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .tab-button span {
    font-size: 0.7rem;
  }
}

/* Banner de Aviso de Testes */
.test-warning-banner {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border: 1px solid #ffc107;
  border-radius: 8px;
  margin-bottom: var(--spacing-lg);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
  animation: slideInDown 0.5s ease-out;
}

.warning-content {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
}

.warning-icon {
  color: #856404;
  font-size: 24px;
  flex-shrink: 0;
  margin-top: 2px;
}

.warning-text {
  flex: 1;
}

.warning-text h4 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #856404;
  font-size: var(--font-size-md);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.warning-text p {
  margin: 0;
  color: #6c5700;
  font-size: var(--font-size-sm);
  line-height: 1.5;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsividade para o banner */
@media (max-width: 768px) {
  .warning-content {
    padding: var(--spacing-sm) var(--spacing-md);
    gap: var(--spacing-sm);
  }
  
  .warning-icon {
    font-size: 20px;
  }
  
  .warning-text h4 {
    font-size: var(--font-size-sm);
  }
  
  .warning-text p {
    font-size: var(--font-size-xs);
  }
}

@media (max-width: 480px) {
  .warning-content {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-xs);
  }
  
  .warning-icon {
    align-self: center;
  }
}
</style> 