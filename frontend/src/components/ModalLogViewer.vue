<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="log-viewer-modal" @click.stop>
      <div class="modal-header">
        <h2>
          <i class="material-icons">history</i>
          LOGS DO SISTEMA
        </h2>
        <div class="filters-container">
          <div class="filter-item">
            <label for="logTypeFilter">
              <i class="material-icons">filter_list</i>
              Tipo:
            </label>
            <select v-model="filters.type" id="logTypeFilter">
              <option value="TODOS">TODOS</option>
              <option value="login">AUTENTICAÇÃO</option>
              <option value="criacao">CRIAÇÃO</option>
              <option value="edicao">EDIÇÃO</option>
              <option value="conclusao">CONCLUSÃO</option>
              <option value="orcamento">ORÇAMENTO</option>
              <option value="erro">ERRO</option>
              <option value="seguranca">SEGURANÇA</option>
            </select>
          </div>
          <div class="filter-item">
            <label for="dateRangeFilter">
              <i class="material-icons">date_range</i>
              Período:
            </label>
            <select v-model="filters.period" id="dateRangeFilter">
              <option value="hoje">HOJE</option>
              <option value="7dias">ÚLTIMOS 7 DIAS</option>
              <option value="30dias">ÚLTIMOS 30 DIAS</option>
              <option value="personalizado">PERSONALIZADO</option>
            </select>
          </div>
          <div class="filter-item" v-if="filters.period === 'personalizado'">
            <div class="date-range-container">
              <div class="date-input">
                <label for="startDate">De:</label>
                <input type="date" id="startDate" v-model="filters.startDate" />
              </div>
              <div class="date-input">
                <label for="endDate">Até:</label>
                <input type="date" id="endDate" v-model="filters.endDate" />
              </div>
            </div>
          </div>
          <div class="filter-item search-filter">
            <input 
              type="text" 
              v-model="filters.search" 
              placeholder="Pesquisar logs..." 
              class="search-input"
            />
            <i class="material-icons search-icon">search</i>
          </div>
        </div>
      </div>

      <!-- Conteúdo dos Logs -->
      <div class="logs-container">
        <!-- Indicador de carregamento -->
        <div v-if="loading" class="loading-container">
          <LoadingIndicator message="Carregando logs..." />
        </div>
        
        <!-- Mensagem se não houver logs -->
        <div v-else-if="filteredLogs.length === 0" class="no-logs-message">
          <i class="material-icons">info</i>
          <p>Nenhum log encontrado para os filtros selecionados</p>
        </div>
        
        <!-- Lista de logs -->
        <div v-else class="logs-list">
          <div 
            v-for="(log, index) in paginatedLogs" 
            :key="index" 
            class="log-item"
            :class="getLogTypeClass(log.tipo)"
          >
            <div class="log-header">
              <div class="log-icon">
                <i class="material-icons">{{ getLogTypeIcon(log.tipo) }}</i>
              </div>
              <div class="log-type">{{ formatLogType(log.tipo) }}</div>
              <div class="log-date">{{ formatDateTime(log.data) }}</div>
            </div>
            <div class="log-content">
              <p class="log-description">{{ log.descricao }}</p>
              <div class="log-details">
                <span class="log-user">
                  <i class="material-icons">person</i>
                  {{ log.usuario_nome || 'Sistema' }}
                </span>
                <span v-if="log.pedido_id" class="log-order-id">
                  <i class="material-icons">receipt</i>
                  Pedido #{{ log.pedido_id }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Paginação -->
      <div class="pagination">
        <button 
          :disabled="currentPage === 1" 
          @click="prevPage" 
          class="pagination-button"
        >
          <i class="material-icons">navigate_before</i>
          Anterior
        </button>
        <span class="page-info">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button 
          :disabled="currentPage === totalPages" 
          @click="nextPage" 
          class="pagination-button"
        >
          Próximo
          <i class="material-icons">navigate_next</i>
        </button>
      </div>
      
      <!-- Botões -->
      <div class="modal-actions">
        <button @click="refreshLogs" class="refresh-button">
          <i class="material-icons">refresh</i>
          ATUALIZAR
        </button>
        <button @click="exportLogs" class="export-button">
          <i class="material-icons">cloud_download</i>
          EXPORTAR
        </button>
        <button @click="closeModal" class="close-button">
          <i class="material-icons">close</i>
          FECHAR
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import LoadingIndicator from "./ui/LoadingIndicator.vue";
import { cachedRequest } from "../utils/cacheService";
import axiosService from "../api/axiosService";
import { validateDate } from "../utils/validationService";

export default {
  name: "ModalLogViewer",
  components: {
    LoadingIndicator
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    onClose: {
      type: Function,
      default: () => {}
    }
  },
  data() {
    return {
      logs: [],
      loading: false,
      currentPage: 1,
      itemsPerPage: 10,
      filters: {
        type: "TODOS",
        period: "7dias",
        search: "",
        startDate: this.getDefaultStartDate(),
        endDate: this.formatDateForInput(new Date())
      },
      cacheOptions: {
        logs: {
          enabled: true,
          ttl: 2 * 60 * 1000 // 2 minutos para logs
        }
      },
      toast: useToast()
    };
  },
  computed: {
    filteredLogs() {
      return this.logs.filter(log => {
        // Filtrar por tipo
        if (this.filters.type !== "TODOS" && log.tipo !== this.filters.type) {
          return false;
        }
        
        // Filtrar por data
        const logDate = new Date(log.data);
        const startDate = this.filters.startDate 
          ? new Date(this.filters.startDate) 
          : new Date(0);
        const endDate = this.filters.endDate 
          ? new Date(this.filters.endDate) 
          : new Date();
        endDate.setHours(23, 59, 59, 999); // Fim do dia
        
        if (logDate < startDate || logDate > endDate) {
          return false;
        }
        
        // Filtrar por texto de pesquisa
        if (this.filters.search && this.filters.search.trim() !== "") {
          const searchTerm = this.filters.search.toLowerCase();
          const descricao = (log.descricao || "").toLowerCase();
          const usuario = (log.usuario_nome || "").toLowerCase();
          const tipo = (log.tipo || "").toLowerCase();
          
          return (
            descricao.includes(searchTerm) ||
            usuario.includes(searchTerm) ||
            tipo.includes(searchTerm) ||
            (log.pedido_id && log.pedido_id.toString().includes(searchTerm))
          );
        }
        
        return true;
      });
    },
    paginatedLogs() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredLogs.slice(start, end);
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredLogs.length / this.itemsPerPage));
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        // Quando o modal é aberto, buscar logs automaticamente
        this.fetchLogs();
      }
    },
    'filters.period'(newValue) {
      // Atualizar datas quando o período mudar
      if (newValue === 'hoje') {
        const today = new Date();
        this.filters.startDate = this.formatDateForInput(today);
        this.filters.endDate = this.formatDateForInput(today);
      } else if (newValue === '7dias') {
        const today = new Date();
        const sevenDaysAgo = new Date();
        sevenDaysAgo.setDate(today.getDate() - 7);
        this.filters.startDate = this.formatDateForInput(sevenDaysAgo);
        this.filters.endDate = this.formatDateForInput(today);
      } else if (newValue === '30dias') {
        const today = new Date();
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(today.getDate() - 30);
        this.filters.startDate = this.formatDateForInput(thirtyDaysAgo);
        this.filters.endDate = this.formatDateForInput(today);
      }
    },
    'filters.type'() {
      // Resetar paginação quando o filtro mudar
      this.currentPage = 1;
    },
    'filters.search'() {
      // Resetar paginação quando pesquisar
      this.currentPage = 1;
    }
  },
  mounted() {
    // Se o modal já estiver aberto ao montar o componente, buscar logs
    if (this.isOpen) {
      this.fetchLogs();
    }
  },
  methods: {
    async fetchLogs() {
      this.loading = true;
      
      try {
        // Validar datas se estiver usando período personalizado
        if (this.filters.period === 'personalizado') {
          const startDateValid = validateDate(this.filters.startDate);
          const endDateValid = validateDate(this.filters.endDate);
          
          if (!startDateValid.isValid || !endDateValid.isValid) {
            this.toast.error('Por favor, verifique o formato das datas');
            this.loading = false;
            return;
          }
          
          // Verificar se a data inicial é anterior à final
          const startDate = new Date(this.filters.startDate);
          const endDate = new Date(this.filters.endDate);
          
          if (startDate > endDate) {
            this.toast.error('A data inicial deve ser anterior à data final');
            this.loading = false;
            return;
          }
        }
        
        // Construir parâmetros para a requisição
        const params = {};
        
        if (this.filters.type !== 'TODOS') {
          params.tipo = this.filters.type;
        }
        
        if (this.filters.period === 'hoje') {
          const today = new Date();
          params.start_date = this.formatDateForAPI(today);
          params.end_date = this.formatDateForAPI(today, true);
        } else if (this.filters.period === '7dias') {
          const today = new Date();
          const sevenDaysAgo = new Date();
          sevenDaysAgo.setDate(today.getDate() - 7);
          params.start_date = this.formatDateForAPI(sevenDaysAgo);
          params.end_date = this.formatDateForAPI(today, true);
        } else if (this.filters.period === '30dias') {
          const today = new Date();
          const thirtyDaysAgo = new Date();
          thirtyDaysAgo.setDate(today.getDate() - 30);
          params.start_date = this.formatDateForAPI(thirtyDaysAgo);
          params.end_date = this.formatDateForAPI(today, true);
        } else if (this.filters.period === 'personalizado') {
          params.start_date = this.formatDateForAPI(new Date(this.filters.startDate));
          params.end_date = this.formatDateForAPI(new Date(this.filters.endDate), true);
        }
        
        // Fazer a requisição usando o cache
        const response = await cachedRequest(
          axiosService.get,
          '/logs',
          { params },
          this.cacheOptions.logs
        );
        
        this.logs = response.data || [];
        
        // Resetar para a primeira página quando novos dados são carregados
        this.currentPage = 1;
      } catch (error) {
        console.error('Erro ao carregar logs:', error);
        this.toast.error('Erro ao carregar logs. Tente novamente mais tarde.');
        this.logs = [];
      } finally {
        this.loading = false;
      }
    },
    formatDateTime(dateString) {
      if (!dateString) return 'Data desconhecida';
      
      const date = new Date(dateString);
      return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    formatLogType(type) {
      const types = {
        login: 'AUTENTICAÇÃO',
        criacao: 'CRIAÇÃO',
        edicao: 'EDIÇÃO',
        conclusao: 'CONCLUSÃO',
        orcamento: 'ORÇAMENTO',
        erro: 'ERRO',
        seguranca: 'SEGURANÇA'
      };
      
      return types[type] || type.toUpperCase();
    },
    getLogTypeIcon(type) {
      const icons = {
        login: 'login',
        criacao: 'add_circle',
        edicao: 'edit',
        conclusao: 'check_circle',
        orcamento: 'attach_money',
        erro: 'error',
        seguranca: 'security'
      };
      
      return icons[type] || 'info';
    },
    getLogTypeClass(type) {
      return `log-type-${type}`;
    },
    closeModal() {
      this.onClose();
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    refreshLogs() {
      // Invalidar o cache para obter dados frescos
      this.cacheOptions.logs.enabled = false;
      this.fetchLogs().finally(() => {
        // Reativar o cache após a atualização
        this.cacheOptions.logs.enabled = true;
      });
      this.toast.info("Atualizando logs...");
    },
    exportLogs() {
      // Criar CSV dos logs filtrados
      let csvContent = "data:text/csv;charset=utf-8,";
      
      // Cabeçalho
      csvContent += "Data,Tipo,Descrição,Usuário,Pedido ID\r\n";
      
      // Dados
      this.filteredLogs.forEach(log => {
        const row = [
          this.formatDateTime(log.data),
          this.formatLogType(log.tipo),
          log.descricao.replace(/,/g, ";"),  // Substituir vírgulas por ponto e vírgula para evitar problemas no CSV
          log.usuario_nome || "Sistema",
          log.pedido_id || ""
        ];
        
        csvContent += row.join(",") + "\r\n";
      });
      
      // Criar link para download
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `logs_sistema_${this.formatDateForFilename(new Date())}.csv`);
      document.body.appendChild(link);
      
      // Trigger download
      link.click();
      
      // Limpar
      document.body.removeChild(link);
      
      this.toast.success("Logs exportados com sucesso");
    },
    getDefaultStartDate() {
      // 7 dias atrás como padrão
      const date = new Date();
      date.setDate(date.getDate() - 7);
      return this.formatDateForInput(date);
    },
    formatDateForInput(date) {
      return date.toISOString().split('T')[0];
    },
    formatDateForFilename(date) {
      return date.toISOString().split('T')[0].replace(/-/g, "");
    },
    formatDateForAPI(date, endOfDay = false) {
      const formattedDate = date.toISOString().split('T')[0];
      if (endOfDay) {
        const endOfDayDate = new Date(formattedDate);
        endOfDayDate.setDate(date.getDate() + 1);
        endOfDayDate.setHours(0, 0, 0, 0);
        return endOfDayDate.toISOString().split('T')[0];
      }
      return formattedDate;
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

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
  overflow: auto;
  padding: 20px;
  box-sizing: border-box;
}

.log-viewer-modal {
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  background-color: #1f1f1f;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modalFadeIn 0.3s ease;
}

.modal-header {
  background-color: #ff6f61;
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
}

.modal-header h2 i {
  margin-right: 10px;
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin: 15px 0 0;
  width: 100%;
}

.filter-item {
  display: flex;
  align-items: center;
  margin-right: 15px;
}

.filter-item label {
  margin-right: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.filter-item label i {
  margin-right: 5px;
}

.filter-item select,
.filter-item input {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #444;
  background-color: #333;
  color: white;
  font-size: 0.9rem;
}

.date-range-container {
  display: flex;
  gap: 10px;
}

.date-input {
  display: flex;
  align-items: center;
}

.date-input label {
  margin-right: 5px;
  white-space: nowrap;
}

.search-filter {
  position: relative;
  flex-grow: 1;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 35px;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
}

.logs-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background-color: #272727;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.no-logs-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #aaa;
  text-align: center;
}

.no-logs-message i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #ff6f61;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.log-item {
  background-color: #333;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.log-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.log-header {
  padding: 12px 15px;
  display: flex;
  align-items: center;
  background-color: #3a3a3a;
  border-bottom: 1px solid #444;
}

.log-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #555;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.log-icon i {
  font-size: 18px;
  color: white;
}

.log-type {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 4px;
  background-color: #555;
  margin-right: auto;
}

.log-date {
  font-size: 0.8rem;
  color: #bbb;
}

.log-content {
  padding: 15px;
  color: #eee;
}

.log-description {
  margin: 0 0 15px;
  line-height: 1.5;
}

.log-details {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 0.85rem;
  color: #bbb;
}

.log-user,
.log-order-id {
  display: flex;
  align-items: center;
}

.log-user i,
.log-order-id i {
  font-size: 16px;
  margin-right: 5px;
}

/* Classes de tipo de log */
.log-type-login .log-icon {
  background-color: #4caf50;
}
.log-type-criacao .log-icon {
  background-color: #2196f3;
}
.log-type-edicao .log-icon {
  background-color: #ff9800;
}
.log-type-conclusao .log-icon {
  background-color: #9c27b0;
}
.log-type-orcamento .log-icon {
  background-color: #00bcd4;
}
.log-type-erro .log-icon {
  background-color: #f44336;
}
.log-type-seguranca .log-icon {
  background-color: #795548;
}

.log-type-login .log-type {
  background-color: #4caf50;
}
.log-type-criacao .log-type {
  background-color: #2196f3;
}
.log-type-edicao .log-type {
  background-color: #ff9800;
}
.log-type-conclusao .log-type {
  background-color: #9c27b0;
}
.log-type-orcamento .log-type {
  background-color: #00bcd4;
}
.log-type-erro .log-type {
  background-color: #f44336;
}
.log-type-seguranca .log-type {
  background-color: #795548;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
  background-color: #1f1f1f;
  border-top: 1px solid #444;
}

.pagination-button {
  background-color: #333;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #444;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button i {
  font-size: 20px;
}

.page-info {
  margin: 0 20px;
  color: #ddd;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  padding: 15px 20px;
  background-color: #1f1f1f;
  border-top: 1px solid #444;
}

.modal-actions button {
  margin-left: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
}

.modal-actions button i {
  margin-right: 8px;
}

.refresh-button {
  background-color: #555;
  color: white;
}

.refresh-button:hover {
  background-color: #666;
}

.export-button {
  background-color: #4caf50;
  color: white;
}

.export-button:hover {
  background-color: #3d8b40;
}

.close-button {
  background-color: #ff6f61;
  color: white;
}

.close-button:hover {
  background-color: #e5635a;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .modal-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filters-container {
    flex-direction: column;
    width: 100%;
  }
  
  .filter-item {
    width: 100%;
    margin-right: 0;
    margin-bottom: 10px;
  }
  
  .date-range-container {
    flex-direction: column;
    gap: 5px;
  }
  
  .modal-actions {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .modal-actions button {
    margin: 5px;
  }
  
  .log-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .log-icon {
    margin-bottom: 10px;
  }
  
  .log-type {
    margin-bottom: 10px;
  }
  
  .log-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}
</style> 