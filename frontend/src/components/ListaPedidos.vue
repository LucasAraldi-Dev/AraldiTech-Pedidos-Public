<template>
  <div class="lista-pedidos-container">
    <div class="header">
      <h2>Lista de Pedidos</h2>
      <div class="header-actions">
        <!-- Botão de informações com tooltip -->
        <TooltipInfo 
          title="Informações da Lista" 
          position="left"
          :maxWidth="300"
        >
          <p>Esta listagem mostra os pedidos no sistema. Os dados são atualizados a cada 5 minutos 
          ou quando os filtros são modificados.</p>
          <p>Clique em um pedido para ver mais detalhes.</p>
        </TooltipInfo>
        
        <button @click="fetchPedidos" class="refresh-button">
          <i class="material-icons">refresh</i>
          Atualizar
        </button>
      </div>
    </div>
    
    <!-- Seção de filtros aqui -->
    <div class="filters-section">
      <!-- Controles de filtros aqui -->
    </div>
    
    <!-- Indicador de carregamento -->
    <div v-if="loading" class="loading-section">
      <LoadingIndicator message="Carregando pedidos..." />
    </div>
    
    <!-- Mensagem de erro -->
    <div v-else-if="error" class="error-message">
      <i class="material-icons">error</i>
      <p>{{ error }}</p>
      <button @click="fetchPedidos" class="retry-button">Tentar novamente</button>
    </div>
    
    <!-- Lista de pedidos -->
    <div v-else-if="pedidos && pedidos.length" class="pedidos-list">
      <!-- Loop através dos pedidos -->
      <div 
        v-for="pedido in pedidos" 
        :key="pedido.id" 
        class="pedido-item"
        @click="() => handlePedidoClick(pedido.id)"
      >
        <div class="pedido-header">
          <span class="pedido-id">#{{ pedido.id }}</span>
          <span class="pedido-status" :class="getStatusClass(pedido.status)">
            {{ getStatusLabel(pedido.status) }}
          </span>
        </div>
        <div class="pedido-body">
          <div class="pedido-cliente">{{ pedido.cliente }}</div>
          <div class="pedido-data">{{ formatDate(pedido.data_criacao) }}</div>
        </div>
        <div class="pedido-footer">
          <div class="pedido-valor">{{ formatCurrency(pedido.valor_total) }}</div>
          <div class="pedido-actions">
            <button class="action-button">
              <i class="material-icons">visibility</i>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Mensagem quando não há pedidos -->
    <div v-else class="no-pedidos">
      <i class="material-icons">inbox</i>
      <p>Nenhum pedido encontrado</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import axiosService from "../api/axiosService";
import { cachedRequest } from "../utils/cacheService";
import { formatDate, formatCurrency } from "../utils/validationService";
import LoadingIndicator from "./ui/LoadingIndicator.vue";
import TooltipInfo from "./ui/TooltipInfo.vue";

export default {
  name: "ListaPedidos",
  components: {
    LoadingIndicator,
    TooltipInfo
  },
  props: {
    // Props para filtro inicial se necessário
    filtroInicial: {
      type: Object,
      default: () => ({})
    }
  },
  setup() {
    const pedidos = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const filtros = ref({
      status: '',
      cliente: '',
      dataInicio: '',
      dataFim: ''
    });
    
    // Opções de cache para diferentes requisições
    const cacheOptions = {
      listaPedidos: {
        enabled: true,
        ttl: 5 * 60 * 1000 // 5 minutos para lista básica
      },
      filtrados: {
        enabled: true,
        ttl: 2 * 60 * 1000 // 2 minutos para resultados filtrados
      },
      detalhes: {
        enabled: true,
        ttl: 10 * 60 * 1000 // 10 minutos para detalhes que mudam pouco
      }
    };
    
    // Buscar pedidos usando cache
    const fetchPedidos = async () => {
      loading.value = true;
      error.value = null;
      
      try {
        // Verificar se estamos usando filtros
        const usandoFiltros = Object.values(filtros.value).some(val => 
          val !== null && val !== undefined && val !== '');
        
        // Escolher as opções de cache adequadas
        const opcoes = usandoFiltros ? cacheOptions.filtrados : cacheOptions.listaPedidos;
        
        // Realizar a requisição com cache
        const response = await cachedRequest(
          axiosService.get,
          "/pedidos",
          { params: filtros.value },
          opcoes
        );
        
        // Atualizar os dados
        pedidos.value = response.data;
        
        // Informar ao usuário se os dados vieram do cache
        if (response.cached) {
          console.log("Dados de pedidos carregados do cache");
        }
      } catch (err) {
        error.value = "Erro ao carregar pedidos. Tente novamente.";
        console.error("Erro ao buscar pedidos:", err);
      } finally {
        loading.value = false;
      }
    };
    
    // Carregar detalhes de pedido com cache
    const loadPedidoDetails = async (pedidoId) => {
      try {
        const response = await cachedRequest(
          axiosService.get,
          `/pedidos/${pedidoId}`,
          {},
          cacheOptions.detalhes
        );
        
        return response.data;
      } catch (err) {
        console.error(`Erro ao carregar detalhes do pedido ${pedidoId}:`, err);
        throw new Error("Não foi possível carregar os detalhes do pedido");
      }
    };
    
    // Manipular clique em pedido
    const handlePedidoClick = async (pedidoId) => {
      try {
        const detalhes = await loadPedidoDetails(pedidoId);
        // Aqui você pode abrir um modal, navegar para a página de detalhes, etc.
        console.log("Detalhes do pedido:", detalhes);
      } catch (err) {
        console.error("Erro ao obter detalhes:", err);
      }
    };
    
    // Obter classe CSS para status
    const getStatusClass = (status) => {
      const statusMap = {
        'pendente': 'status-pendente',
        'em_andamento': 'status-em-andamento',
        'concluido': 'status-concluido',
        'cancelado': 'status-cancelado'
      };
      
      return statusMap[status] || 'status-pendente';
    };
    
    // Obter label amigável para status
    const getStatusLabel = (status) => {
      const labelMap = {
        'pendente': 'Pendente',
        'em_andamento': 'Em Andamento',
        'concluido': 'Concluído',
        'cancelado': 'Cancelado'
      };
      
      return labelMap[status] || status;
    };
    
    // Observar mudanças nos filtros para atualizar dados
    watch(filtros, () => {
      fetchPedidos();
    }, { deep: true });
    
    // Inicialização
    onMounted(() => {
      fetchPedidos();
    });
    
    return {
      pedidos,
      loading,
      error,
      filtros,
      fetchPedidos,
      loadPedidoDetails,
      handlePedidoClick,
      getStatusClass,
      getStatusLabel,
      formatDate,
      formatCurrency
    };
  }
};
</script>

<style scoped>
.lista-pedidos-container {
  width: 100%;
  background-color: #292929;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #3e3e3e;
}

.header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #444;
  border: none;
  color: #fff;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-button:hover {
  background-color: #555;
}

.refresh-button i {
  font-size: 18px;
}

.loading-section {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #ff6b6b;
  text-align: center;
}

.error-message i {
  font-size: 48px;
  margin-bottom: 15px;
}

.retry-button {
  margin-top: 15px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.retry-button:hover {
  background-color: #ff5252;
}

.pedidos-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.pedido-item {
  background-color: #363636;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.pedido-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.pedido-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #444;
  color: white;
}

.pedido-id {
  font-weight: 600;
  font-size: 1.1rem;
}

.pedido-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pendente {
  background-color: #ffc107;
  color: #333;
}

.status-em-andamento {
  background-color: #3498db;
  color: white;
}

.status-concluido {
  background-color: #2ecc71;
  color: white;
}

.status-cancelado {
  background-color: #e74c3c;
  color: white;
}

.pedido-body {
  padding: 15px;
  border-bottom: 1px solid #484848;
}

.pedido-cliente {
  font-size: 1rem;
  margin-bottom: 8px;
  color: #fff;
}

.pedido-data {
  font-size: 0.85rem;
  color: #bbb;
}

.pedido-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
}

.pedido-valor {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2ecc71;
}

.pedido-actions {
  display: flex;
  gap: 5px;
}

.action-button {
  background-color: transparent;
  border: none;
  color: #bbb;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: #555;
  color: white;
}

.action-button i {
  font-size: 20px;
}

.no-pedidos {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #777;
  text-align: center;
}

.no-pedidos i {
  font-size: 48px;
  margin-bottom: 15px;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .pedidos-list {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style> 