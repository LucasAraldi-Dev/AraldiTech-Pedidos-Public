<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="log-viewer-modal" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">
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
              <option value="logout">LOGOUT</option>
              <option value="criacao">CRIAÇÃO</option>
              <option value="edicao">EDIÇÃO</option>
              <option value="consulta">CONSULTA</option>
              <option value="conclusao">CONCLUSÃO</option>
              <option value="orcamento">ORÇAMENTO</option>
              <option value="erro">ERRO</option>
              <option value="registro">CADASTRO</option>
              <option value="seguranca">SEGURANÇA</option>
              <option value="cancelamento">CANCELAMENTO</option>
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
              <button 
                @click="fetchLogs" 
                class="apply-date-btn"
                :disabled="loading"
              >
                <i class="material-icons">check</i>
                Aplicar
              </button>
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

      <!-- Dashboard de estatísticas -->
      <div class="stats-dashboard" v-show="logs.length > 0">
        <div class="stats-header">
          <div class="stats-title">
            <i class="material-icons">analytics</i>
            Visão Geral da Auditoria
          </div>
          <button class="toggle-stats-btn" @click="toggleStats">
            <i class="material-icons">{{ isStatsExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</i>
            {{ isStatsExpanded ? 'Recolher' : 'Expandir' }}
          </button>
        </div>
        <div class="stats-content" v-if="isStatsExpanded">
          <div class="stats-cards">
            <div class="stats-card">
              <div class="stats-card-title">Total de Logs</div>
              <div class="stats-card-value">{{ logs.length }}</div>
            </div>
            <div class="stats-card">
              <div class="stats-card-title">Período</div>
              <div class="stats-card-value">{{ getFilterPeriodLabel() }}</div>
            </div>
            <div class="stats-card">
              <div class="stats-card-title">Logs por Tipo</div>
              <div class="stats-card-content">
                <div v-for="(count, type) in countLogsByType" :key="type" class="log-type-chip">
                  <span 
                    class="log-type-indicator" 
                    :class="`indicator-${type}`"
                  ></span>
                  {{ formatLogType(type) }}: {{ count }}
                </div>
              </div>
            </div>
            <div class="stats-card">
              <div class="stats-card-title">Última Atualização</div>
              <div class="stats-card-value">{{ formatDateTime(new Date()) }}</div>
            </div>
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
              <div class="log-type-tag">
                {{ formatLogType(log.tipo) }}
              </div>
              <div class="log-date">
                <i class="material-icons date-icon">event</i>
                {{ formatDateTime(log.data) }}
              </div>
            </div>
            <div class="log-content">
              <p class="log-description">{{ log.descricao }}</p>
              <div class="log-details">
                <div class="log-tags">
                  <span v-if="log.usuario_nome" class="log-tag log-tag-user">
                    <i class="material-icons">person</i>
                    {{ log.usuario_nome }}
                  </span>
                  <span v-if="log.pedido_id" class="log-tag log-tag-order" @click="showOrderInfo(log.pedido_id)">
                    <i class="material-icons">receipt</i>
                    Pedido #{{ log.pedido_id }}
                  </span>
                  <span class="log-tag log-tag-time">
                    <i class="material-icons">schedule</i>
                    {{ getTimeFromNow(log.data) }}
                  </span>
                </div>
                <div class="log-actions">
                  <button class="action-button" @click="viewLogDetails(log)">
                    <i class="material-icons">info</i>
                    Detalhes
                  </button>
                  <button v-if="log.pedido_id" class="action-button" @click="showOrderInfo(log.pedido_id)">
                    <i class="material-icons">visibility</i>
                    Ver Pedido
                  </button>
                  <button class="action-button" @click="copyLogToClipboard(log)">
                    <i class="material-icons">content_copy</i>
                    Copiar
                  </button>
                </div>
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
    
    <!-- Modal de Detalhes do Log -->
    <ModalLogDetail
      :isOpen="isLogDetailOpen"
      :log="selectedLog"
      :onClose="closeLogDetail"
      @view-order="showOrderInfoFromDetail"
    />
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import LoadingIndicator from "./ui/LoadingIndicator.vue";
import axiosService from "../api/axiosService";
import { validateDate } from "../utils/validationService";
import ModalLogDetail from "./ModalLogDetail.vue";

export default {
  name: "ModalLogViewer",
  components: {
    LoadingIndicator,
    ModalLogDetail
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
      toast: useToast(),
      isAdmin: localStorage.getItem("user") ? 
        JSON.parse(localStorage.getItem("user")).tipo_usuario === "admin" : 
        false,
      isLogDetailOpen: false,
      selectedLog: null,
      isStatsExpanded: false
    };
  },
  computed: {
    filteredLogs() {
      return this.logs.filter(log => {
        // Filtrar por tipo
        if (this.filters.type !== "TODOS" && log.tipo !== this.filters.type) {
          return false;
        }
        
        // Filtro de data já é aplicado na API, não precisamos filtrar novamente
        
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
    },
    // Contagem de logs por tipo para o dashboard de estatísticas
    countLogsByType() {
      const typeCounts = {};
      
      this.logs.forEach(log => {
        const tipo = log.tipo || 'desconhecido';
        typeCounts[tipo] = (typeCounts[tipo] || 0) + 1;
      });
      
      return typeCounts;
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
      
      // Aplicar filtros imediatamente
      if (this.isOpen) {
        this.fetchLogs();
      }
    },
    'filters.type'() {
      // Resetar paginação quando o filtro mudar
      this.currentPage = 1;
      // Buscar dados filtrados imediatamente
      if (this.isOpen) {
        this.fetchLogs();
      }
    },
    'filters.search'() {
      // Resetar paginação quando pesquisar
      this.currentPage = 1;
      // Buscar dados com a pesquisa
      if (this.isOpen && this.filters.search.trim().length > 2) {
        this.fetchLogs();
      }
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
      console.log("Iniciando busca de logs...");
      
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
        
        // Preparar parâmetros para a requisição
        const params = {
          limit: 1000  // Limite alto para obter muitos logs
        };
        
        // Adicionar filtro de tipo se não for TODOS
        if (this.filters.type !== 'TODOS') {
          params.tipo = this.filters.type;
        }
        
        // Adicionar filtros de data conforme o período selecionado
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
        
        // Adicionar termo de busca se houver
        if (this.filters.search && this.filters.search.trim() !== "") {
          params.search = this.filters.search;
        }
        
        console.log("Buscando dados do endpoint /atividades com parâmetros:", params);
        
        // Fazer a requisição direta sem cache
        const response = await axiosService.get('/atividades', { params });
        
        // Atualizar os logs
        this.logs = response.data || [];
        console.log(`Recebidos ${this.logs.length} logs do endpoint /atividades`);
        
        // Ordenar por data, do mais recente para o mais antigo
        this.logs.sort((a, b) => new Date(b.data) - new Date(a.data));
        
        // Mostrar estatísticas no console
        const tiposEncontrados = [...new Set(this.logs.map(log => log.tipo))];
        console.log("Tipos de logs encontrados:", tiposEncontrados);
        console.log("Total de logs:", this.logs.length);
        
        // Resetar para a primeira página
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
        logout: 'LOGOUT',
        criacao: 'CRIAÇÃO',
        edicao: 'EDIÇÃO',
        consulta: 'CONSULTA',
        conclusao: 'CONCLUSÃO',
        orcamento: 'ORÇAMENTO',
        erro: 'ERRO',
        seguranca: 'SEGURANÇA',
        registro: 'CADASTRO',
        cancelamento: 'CANCELAMENTO'
      };
      
      return types[type] || type.toUpperCase();
    },
    getLogTypeIcon(type) {
      const icons = {
        login: 'login',
        logout: 'logout',
        criacao: 'add_circle',
        edicao: 'edit',
        consulta: 'search',
        conclusao: 'check_circle',
        orcamento: 'attach_money',
        erro: 'error',
        seguranca: 'security',
        registro: 'person_add',
        cancelamento: 'cancel'
      };
      
      return icons[type] || 'info';
    },
    getLogTypeClass(type) {
      return `log-type-${type}`;
    },
    closeModal() {
      console.log('[CRÍTICO] Método closeModal chamado - fechando ModalLogViewer');
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
      this.fetchLogs();
      this.toast.info("Atualizando logs do sistema...");
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
    },
    // Novos métodos adicionados para suportar funcionalidades
    getTimeFromNow(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      
      // Converter para segundos, minutos, horas e dias
      const seconds = Math.floor(diffMs / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      if (days > 0) {
        return days === 1 ? 'há 1 dia' : `há ${days} dias`;
      } else if (hours > 0) {
        return hours === 1 ? 'há 1 hora' : `há ${hours} horas`;
      } else if (minutes > 0) {
        return minutes === 1 ? 'há 1 minuto' : `há ${minutes} minutos`;
      } else {
        return seconds <= 10 ? 'agora mesmo' : `há ${seconds} segundos`;
      }
    },
    async showOrderInfo(pedidoId) {
      try {
        console.log(`[CRÍTICO] showOrderInfo chamado com pedidoId: ${pedidoId}`);
        
        // Adicionar um feedback visual claro para o usuário
        this.toast.info(`Buscando detalhes do pedido #${pedidoId}...`, {
          timeout: 3000,
          closeButton: false
        });
        
        // Método 1: Fazer uma busca específica pelo ID do pedido usando axios
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error('[CRÍTICO] Token de autenticação não encontrado');
          this.toast.error('Sessão expirada. Faça login novamente.');
          return;
        }
        
        // Garantir que pedidoId seja numérico
        const pedidoIdNum = typeof pedidoId === 'string' ? parseInt(pedidoId, 10) : pedidoId;
        console.log(`[CRÍTICO] ID do pedido convertido para número: ${pedidoIdNum}`);
        
        // Emitir evento para o componente pai (AppMenu) para abrir o modal de impressão
        console.log(`[CRÍTICO] Emitindo evento open-order com pedidoId: ${pedidoIdNum}`);
        this.$emit('open-order', pedidoIdNum);
        
        console.log('[CRÍTICO] Evento open-order emitido com sucesso');
              
        // Não fechamos mais o modal para que ele possa ser reaberto quando o pedido for fechado
        // console.log('[CRÍTICO] Fechando modal de logs depois de emitir o evento');
        // this.onClose();
        
        return true;
      } catch (error) {
        console.error('[CRÍTICO] Erro ao buscar detalhes do pedido:', error);
        
        let mensagemErro = 'Não foi possível carregar os detalhes do pedido.';
        
        if (error.response) {
          // O servidor respondeu com um código de erro
          console.error(`Erro de resposta: ${error.response.status}`, error.response.data);
          if (error.response.status === 403) {
            mensagemErro += ' Você não tem permissão para ver este pedido.';
          } else if (error.response.status === 404) {
            mensagemErro += ' Pedido não encontrado.';
          } else if (error.response.status >= 500) {
            mensagemErro += ' Erro no servidor. Tente novamente mais tarde.';
          }
        } else if (error.request) {
          // A requisição foi feita mas não houve resposta (problema de rede)
          console.error('Erro de rede - sem resposta do servidor:', error.request);
          mensagemErro += ' Verifique sua conexão com a internet.';
        } else {
          // Erro de configuração da requisição ou outro tipo de erro
          console.error('Outro tipo de erro:', error.message);
        }
        
        this.toast.error(mensagemErro, {
          timeout: 5000,
          closeButton: false
        });
        
        return false;
      }
    },
    copyLogToClipboard(log) {
      try {
        // Criar texto formatado para copiar
        const formattedLog = `
          Tipo: ${this.formatLogType(log.tipo)}
          Data: ${this.formatDateTime(log.data)}
          Descrição: ${log.descricao}
          Usuário: ${log.usuario_nome || 'Sistema'}
          ${log.pedido_id ? `Pedido: #${log.pedido_id}` : ''}
          ID: ${log.id}
        `.trim();
        
        // Método alternativo para copiar para o clipboard, compatível com mais navegadores
        const textArea = document.createElement('textarea');
        textArea.value = formattedLog;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        
        if (successful) {
          this.toast.success('Log copiado para a área de transferência');
        } else {
          // Tentar método moderno se o antigo falhar
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(formattedLog)
              .then(() => {
                this.toast.success('Log copiado para a área de transferência');
              })
              .catch(err => {
                throw err;
              });
          } else {
            this.toast.error('Seu navegador não suporta copiar para área de transferência');
          }
        }
        
        document.body.removeChild(textArea);
      } catch (error) {
        console.error('Erro ao copiar log:', error);
        this.toast.error('Não foi possível copiar o log');
      }
    },
    getFilterPeriodLabel() {
      switch (this.filters.period) {
        case 'hoje':
          return 'Hoje';
        case '7dias':
          return 'Últimos 7 dias';
        case '30dias':
          return 'Últimos 30 dias';
        case 'personalizado':
          return `${this.filters.startDate} a ${this.filters.endDate}`;
        default:
          return 'Personalizado';
      }
    },
    viewLogDetails(log) {
      this.selectedLog = log;
      this.isLogDetailOpen = true;
    },
    closeLogDetail() {
      this.isLogDetailOpen = false;
    },
    showOrderInfoFromDetail(pedidoId) {
      this.showOrderInfo(pedidoId);
    },
    toggleStats() {
      this.isStatsExpanded = !this.isStatsExpanded;
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
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
  padding: 15px;
  box-sizing: border-box;
}

.log-viewer-modal {
  background-color: #1f1f1f;
  border-radius: 10px;
  width: 90%;
  max-width: 1200px;
  height: 90vh; /* Definir altura fixa */
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  color: #f5f5f5;
  overflow: hidden;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #333;
  display: flex;
  flex-direction: column;
  background-color: #1f1f1f;
  z-index: 10;
  flex-shrink: 0; /* Evitar que o cabeçalho encolha */
}

.modal-title {
  font-size: 24px;
  margin: 0;
  color: #f5f5f5;
  display: flex;
  align-items: center;
}

.modal-title i {
  margin-right: 15px;
  color: #ff6f61;
}

.filters-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 15px;
  padding: 10px;
  background-color: #252525;
  border-radius: 4px;
  border: 1px solid #333;
}

.filter-item {
  display: flex;
  align-items: center;
}

.filter-item label {
  margin-right: 8px;
  display: flex;
  align-items: center;
  color: #f5f5f5;
}

.filter-item label i {
  margin-right: 5px;
  color: #ff6f61;
}

.filter-item select,
.filter-item input {
  padding: 8px 12px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #f5f5f5;
  font-size: 14px;
}

.date-range-container {
  display: flex;
  align-items: center;
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

.apply-date-btn {
  padding: 8px 12px;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}

.apply-date-btn i {
  margin-right: 5px;
}

.apply-date-btn:hover {
  background-color: #e74c3c;
}

.search-filter {
  position: relative;
  flex-grow: 1;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 35px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #f5f5f5;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.logs-container {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: #252525;
  display: flex;
  flex-direction: column;
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
  justify-content: center;
  align-items: center;
  height: 200px;
  color: #999;
  font-size: 1.2rem;
}

.no-logs-message i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #ff6f61;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
}

.log-item {
  background-color: #2a2a2a;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  border-left: 5px solid #444;
  transition: transform 0.2s;
  width: 100%;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.log-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.log-header {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  background-color: #333;
  border-bottom: 1px solid #444;
  width: 100%;
  box-sizing: border-box;
}

.log-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #444;
  margin-right: 12px;
}

.log-icon i {
  font-size: 20px;
  color: #f5f5f5;
}

.log-type-tag {
  padding: 5px 10px;
  background-color: #444;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  margin-right: auto;
  color: #f5f5f5;
  min-width: 80px;
  text-align: center;
}

.log-date {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  color: #999;
}

.date-icon {
  font-size: 16px;
  margin-right: 5px;
}

.log-content {
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
}

.log-description {
  margin: 0 0 15px 0;
  font-size: 1rem;
  line-height: 1.5;
  color: #f5f5f5;
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  white-space: pre-line; /* Preservar quebras de linha no texto */
}

.log-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
  box-sizing: border-box;
}

.log-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.log-tag {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  background-color: #333;
  border-radius: 4px;
  font-size: 0.85rem;
}

.log-tag i {
  font-size: 16px;
  margin-right: 5px;
}

.log-tag-user {
  background-color: rgba(3, 169, 244, 0.2);
  color: #03a9f4;
}

.log-tag-order {
  background-color: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  cursor: pointer;
}

.log-tag-order:hover {
  background-color: rgba(76, 175, 80, 0.3);
}

.log-tag-time {
  background-color: rgba(255, 152, 0, 0.2);
  color: #ff9800;
}

.log-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-button {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #f5f5f5;
}

.action-button i {
  font-size: 16px;
  margin-right: 5px;
  color: #ff6f61;
}

.action-button:hover {
  background-color: #444;
}

/* Estilos específicos para tipos de log */
.log-type-login {
  border-left-color: #3498db;
}

.log-type-logout {
  border-left-color: #34495e;
}

.log-type-criacao {
  border-left-color: #2ecc71;
}

.log-type-edicao {
  border-left-color: #f39c12;
}

.log-type-consulta {
  border-left-color: #1abc9c;
}

.log-type-conclusao {
  border-left-color: #27ae60;
}

.log-type-orcamento {
  border-left-color: #9b59b6;
}

.log-type-erro {
  border-left-color: #e74c3c;
}

.log-type-seguranca {
  border-left-color: #8e44ad;
}

.log-type-registro {
  border-left-color: #16a085;
}

.log-type-cancelamento {
  border-left-color: #c0392b;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 15px;
  background-color: #252525;
  border-top: 1px solid #333;
  flex-shrink: 0; /* Evitar que a paginação encolha */
}

.pagination-button {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #ff6f61;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #e74c3c;
}

.pagination-button:disabled {
  background-color: #444;
  cursor: not-allowed;
}

.pagination-button i {
  font-size: 18px;
}

.page-info {
  margin: 0 15px;
  font-size: 0.9rem;
  color: #999;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px;
  background-color: #1f1f1f;
  border-top: 1px solid #333;
  flex-shrink: 0; /* Evitar que os botões encolham */
}

.refresh-button,
.export-button,
.close-button {
  display: flex;
  align-items: center;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.refresh-button {
  background-color: #ff6f61;
  color: white;
}

.refresh-button:hover {
  background-color: #e74c3c;
}

.export-button {
  background-color: #2ecc71;
  color: white;
}

.export-button:hover {
  background-color: #27ae60;
}

.close-button {
  background-color: #333;
  color: white;
}

.close-button:hover {
  background-color: #444;
}

.modal-actions button i {
  margin-right: 5px;
}

/* Dashboard de estatísticas */
.stats-dashboard {
  padding: 10px 15px;
  background-color: #252525;
  border-bottom: 1px solid #333;
  flex-shrink: 0; /* Evitar que as estatísticas encolham */
}

.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stats-title {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: bold;
  color: #f5f5f5;
}

.stats-title i {
  margin-right: 8px;
  color: #ff6f61;
}

.toggle-stats-btn {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: #333;
  border: 1px solid #444;
  border-radius: 4px;
  color: #f5f5f5;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.toggle-stats-btn:hover {
  background-color: #444;
}

.toggle-stats-btn i {
  margin-right: 5px;
}

.stats-content {
  animation: slideDown 0.3s ease-in-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stats-card {
  background-color: #2a2a2a;
  border-radius: 6px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  border: 1px solid #333;
}

.stats-card-title {
  font-size: 0.9rem;
  color: #999;
  margin-bottom: 10px;
}

.stats-card-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #f5f5f5;
}

.stats-card-content {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.log-type-chip {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  background-color: #333;
  border-radius: 12px;
  font-size: 0.8rem;
  color: #f5f5f5;
}

.log-type-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 5px;
}

.indicator-login {
  background-color: #3498db;
}

.indicator-logout {
  background-color: #34495e;
}

.indicator-criacao {
  background-color: #2ecc71;
}

.indicator-edicao {
  background-color: #f39c12;
}

.indicator-consulta {
  background-color: #1abc9c;
}

.indicator-conclusao {
  background-color: #27ae60;
}

.indicator-orcamento {
  background-color: #9b59b6;
}

.indicator-erro {
  background-color: #e74c3c;
}

.indicator-seguranca {
  background-color: #8e44ad;
}

.indicator-registro {
  background-color: #16a085;
}

.indicator-cancelamento {
  background-color: #c0392b;
}

.indicator-desconhecido {
  background-color: #bdc3c7;
}

/* Responsividade melhorada */
@media (max-width: 768px) {
  .log-viewer-modal {
    width: 100%;
    height: 100vh;
    border-radius: 0;
    max-height: none;
    padding-bottom: 100px; /* Adicionar espaço para evitar que os botões fiquem escondidos */
  }
  
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .date-range-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .logs-container {
    padding: 10px;
    padding-bottom: 150px; /* Adicionar padding para evitar que os logs fiquem escondidos pelos botões fixos */
    max-height: calc(100vh - 200px); /* Garantir espaço adequado para rolagem, considerando cabeçalho e botões */
  }
  
  .log-item {
    margin-bottom: 15px;
  }
  
  .log-header {
    flex-wrap: wrap;
  }
  
  .log-type-tag {
    margin-right: 10px;
    margin-bottom: 5px;
  }
  
  .log-date {
    width: 100%;
    margin-top: 5px;
    justify-content: flex-end;
  }
  
  .log-details {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .log-actions {
    margin-top: 10px;
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
  
  .log-tag {
    margin-bottom: 5px;
  }
  
  .action-button {
    margin-bottom: 5px;
  }
  
  /* Estilos para garantir que a paginação e botões de ação fiquem visíveis */
  .pagination {
    position: fixed;
    bottom: 60px;
    left: 0;
    right: 0;
    background-color: #252525;
    z-index: 10;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
  }
  
  .modal-actions {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #1f1f1f;
    z-index: 10;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
    padding: 10px;
  }
}

/* Estilização personalizada dos scrollbars */
.logs-container::-webkit-scrollbar {
  width: 8px;
}

.logs-container::-webkit-scrollbar-track {
  background: #333;
  border-radius: 10px;
}

.logs-container::-webkit-scrollbar-thumb {
  background-color: #ff6f61;
  border-radius: 10px;
}

.logs-container {
  scrollbar-width: thin;
  scrollbar-color: #ff6f61 #333;
}

/* Telas muito pequenas - ajuste adicional */
@media (max-width: 480px) {
  .log-viewer-modal {
    padding-bottom: 120px; /* Mais espaço para dispositivos muito pequenos */
  }
  
  .logs-container {
    padding-bottom: 170px; /* Espaço extra para dispositivos pequenos */
    max-height: calc(100vh - 220px); /* Ajuste extra para telas muito pequenas */
  }
  
  .pagination {
    padding: 8px 5px;
    bottom: 65px;
  }
  
  .pagination-button {
    padding: 6px 10px;
    font-size: 0.8rem;
  }
  
  .page-info {
    font-size: 0.8rem;
    margin: 0 5px;
  }
  
  .modal-actions {
    padding: 8px 5px;
    gap: 5px;
  }
  
  .refresh-button,
  .export-button,
  .close-button {
    padding: 6px 10px;
    font-size: 0.8rem;
  }
}
</style>