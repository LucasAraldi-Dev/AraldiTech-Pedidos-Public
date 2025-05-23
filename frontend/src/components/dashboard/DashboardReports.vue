<template>
  <div class="reports-container">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <LoadingIndicator message="Carregando relatórios..." size="large" />
    </div>

    <div v-else class="reports-content">
      <!-- Quick Reports Section -->
      <div class="quick-reports-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">flash_on</i>
            Relatórios Rápidos
          </h3>
          <button class="refresh-btn" @click="refreshData" :disabled="isRefreshing">
            <i class="material-icons" :class="{ 'spinning': isRefreshing }">refresh</i>
            <span>Atualizar</span>
          </button>
        </div>

        <div class="quick-reports-grid">
          <div 
            v-for="template in quickTemplates" 
            :key="template.id"
            class="report-card"
            @click="generateQuickReport(template)"
            :class="{ 'generating': generatingTemplate === template.id }"
          >
            <div class="card-icon" :class="template.color">
              <i class="material-icons">{{ template.icon }}</i>
            </div>
            <div class="card-content">
              <h4>{{ template.name }}</h4>
              <p>{{ template.description }}</p>
              <div class="card-meta">
                <span class="meta-item">
                  <i class="material-icons">schedule</i>
                  {{ template.estimatedTime }}
                </span>
                <span class="meta-item">
                  <i class="material-icons">description</i>
                  {{ template.format }}
                </span>
              </div>
            </div>
            <div class="card-action">
              <i class="material-icons" v-if="generatingTemplate !== template.id">play_arrow</i>
              <i class="material-icons spinning" v-else>hourglass_empty</i>
            </div>
          </div>
        </div>
      </div>

      <!-- Custom Report Builder -->
      <div class="custom-reports-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">build</i>
            Construtor de Relatórios Personalizados
          </h3>
        </div>

        <div class="report-builder">
          <div class="builder-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="reportName">
                  <i class="material-icons">title</i>
                  Nome do Relatório
                </label>
                <input 
                  id="reportName"
                  v-model="customReport.name" 
                  type="text" 
                  placeholder="Ex: Relatório Mensal de Vendas"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label for="reportType">
                  <i class="material-icons">category</i>
                  Tipo de Relatório
                </label>
                <select id="reportType" v-model="customReport.type" class="form-select">
                  <option value="">Selecione o tipo</option>
                  <option value="pedidos">Relatório de Pedidos</option>
                  <option value="atividades">Relatório de Atividades</option>
                </select>
              </div>

              <div class="form-group">
                <label for="reportPeriod">
                  <i class="material-icons">date_range</i>
                  Período
                </label>
                <select id="reportPeriod" v-model="customReport.period" class="form-select" @change="updateDateRange">
                  <option value="diario">Hoje</option>
                  <option value="semanal">Esta Semana</option>
                  <option value="mensal">Este Mês</option>
                  <option value="personalizado">Período Personalizado</option>
                </select>
              </div>

              <div class="form-group">
                <label for="reportFormat">
                  <i class="material-icons">file_present</i>
                  Formato
                </label>
                <select id="reportFormat" v-model="customReport.format" class="form-select">
                  <option value="pdf">PDF</option>
                  <option value="excel">Excel (XLSX)</option>
                  <option value="csv">CSV</option>
                </select>
              </div>
            </div>

            <!-- Custom Date Range -->
            <div v-if="customReport.period === 'personalizado'" class="date-range-group">
              <div class="form-group">
                <label for="dateFrom">
                  <i class="material-icons">event</i>
                  Data Inicial
                </label>
                <input 
                  id="dateFrom"
                  v-model="customReport.dateFrom" 
                  type="date" 
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="dateTo">
                  <i class="material-icons">event</i>
                  Data Final
                </label>
                <input 
                  id="dateTo"
                  v-model="customReport.dateTo" 
                  type="date" 
                  class="form-input"
                />
              </div>
            </div>

            <!-- Filters Section -->
            <div class="filters-section">
              <h4>
                <i class="material-icons">filter_list</i>
                Filtros Avançados
              </h4>
              <div class="filters-grid">
                <div class="filter-group">
                  <label class="filter-label">
                    <input 
                      type="checkbox" 
                      v-model="customReport.filters.includeStatus"
                      class="filter-checkbox"
                    />
                    <span class="checkbox-custom"></span>
                    Filtrar por Status
                  </label>
                  <select 
                    v-if="customReport.filters.includeStatus" 
                    v-model="customReport.statusFilter"
                    class="filter-select"
                  >
                    <option value="">Todos os Status</option>
                    <option value="Pendente">Pendente</option>
                    <option value="Concluído">Concluído</option>
                    <option value="Cancelado">Cancelado</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label class="filter-label">
                    <input 
                      type="checkbox" 
                      v-model="customReport.filters.includeCategory"
                      class="filter-checkbox"
                    />
                    <span class="checkbox-custom"></span>
                    Filtrar por Categoria
                  </label>
                  <select 
                    v-if="customReport.filters.includeCategory" 
                    v-model="customReport.categoryFilter"
                    class="filter-select"
                  >
                    <option value="">Todas as Categorias</option>
                    <option value="Matérias-primas">Matérias-primas</option>
                    <option value="Equipamentos e Máquinas">Equipamentos e Máquinas</option>
                    <option value="Peças de Reposição">Peças de Reposição</option>
                    <option value="Serviços">Serviços</option>
                    <option value="Mercadorias diversas">Mercadorias diversas</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label class="filter-label">
                    <input 
                      type="checkbox" 
                      v-model="customReport.filters.includeUrgency"
                      class="filter-checkbox"
                    />
                    <span class="checkbox-custom"></span>
                    Filtrar por Urgência
                  </label>
                  <select 
                    v-if="customReport.filters.includeUrgency" 
                    v-model="customReport.urgencyFilter"
                    class="filter-select"
                  >
                    <option value="">Todas as Urgências</option>
                    <option value="Padrão">Padrão</option>
                    <option value="Urgente">Urgente</option>
                    <option value="Crítico">Crítico</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label class="filter-label">
                    <input 
                      type="checkbox" 
                      v-model="customReport.filters.includeSector"
                      class="filter-checkbox"
                    />
                    <span class="checkbox-custom"></span>
                    Filtrar por Setor
                  </label>
                  <select 
                    v-if="customReport.filters.includeSector" 
                    v-model="customReport.sectorFilter"
                    class="filter-select"
                  >
                    <option value="">Todos os Setores</option>
                    <option value="Escritório">Escritório</option>
                    <option value="Fábrica de Ração">Fábrica de Ração</option>
                    <option value="CPO">CPO</option>
                    <option value="Granjas">Granjas</option>
                    <option value="Abatedouro">Abatedouro</option>
                    <option value="Transporte">Transporte</option>
                    <option value="Incubatório">Incubatório</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="form-actions">
              <button 
                class="btn-secondary" 
                @click="resetForm"
              >
                <i class="material-icons">refresh</i>
                Limpar Formulário
              </button>
              <button 
                class="btn-primary" 
                @click="generateCustomReport"
                :disabled="!canGenerateCustom || isGeneratingCustom"
              >
                <i class="material-icons" :class="{ 'spinning': isGeneratingCustom }">
                  {{ isGeneratingCustom ? 'hourglass_empty' : 'file_download' }}
                </i>
                {{ isGeneratingCustom ? 'Gerando...' : 'Gerar Relatório' }}
              </button>
            </div>
          </div>

          <!-- Report Preview -->
          <div class="report-preview">
            <div class="preview-header">
              <h4>
                <i class="material-icons">visibility</i>
                Pré-visualização
              </h4>
            </div>
            <div class="preview-content">
              <div v-if="!customReport.name && !customReport.type" class="preview-empty">
                <i class="material-icons">description</i>
                <p>Configure o relatório para ver a pré-visualização</p>
              </div>
              <div v-else class="preview-details">
                <div class="preview-item">
                  <span class="preview-label">Nome:</span>
                  <span class="preview-value">{{ customReport.name || 'Não definido' }}</span>
                </div>
                <div class="preview-item">
                  <span class="preview-label">Tipo:</span>
                  <span class="preview-value">{{ getTypeLabel(customReport.type) }}</span>
                </div>
                <div class="preview-item">
                  <span class="preview-label">Período:</span>
                  <span class="preview-value">{{ getPeriodLabel(customReport.period) }}</span>
                </div>
                <div class="preview-item">
                  <span class="preview-label">Formato:</span>
                  <span class="preview-value">{{ customReport.format.toUpperCase() }}</span>
                </div>
                <div v-if="hasActiveFilters" class="preview-filters">
                  <span class="preview-label">Filtros ativos:</span>
                  <div class="active-filters">
                    <span v-if="customReport.filters.includeStatus" class="filter-tag">
                      Status: {{ customReport.statusFilter || 'Todos' }}
                    </span>
                    <span v-if="customReport.filters.includeCategory" class="filter-tag">
                      Categoria: {{ customReport.categoryFilter || 'Todas' }}
                    </span>
                    <span v-if="customReport.filters.includeUrgency" class="filter-tag">
                      Urgência: {{ customReport.urgencyFilter || 'Todas' }}
                    </span>
                    <span v-if="customReport.filters.includeSector" class="filter-tag">
                      Setor: {{ customReport.sectorFilter || 'Todos' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Reports -->
      <div class="recent-reports-section">
        <div class="section-header">
          <h3>
            <i class="material-icons">history</i>
            Relatórios Recentes
          </h3>
          <button class="btn-secondary small" @click="clearRecentReports" v-if="recentReports.length > 0">
            <i class="material-icons">delete_sweep</i>
            Limpar Histórico
          </button>
        </div>

        <div v-if="recentReports.length === 0" class="empty-state">
          <i class="material-icons">folder_open</i>
          <p>Nenhum relatório gerado ainda</p>
          <span>Os relatórios gerados aparecerão aqui para download</span>
        </div>

        <div v-else class="reports-list">
          <div 
            v-for="report in recentReports" 
            :key="report.id"
            class="report-item"
          >
            <div class="report-icon">
              <i class="material-icons">{{ getReportIcon(report.type) }}</i>
            </div>
            <div class="report-info">
              <h5>{{ report.name }}</h5>
              <div class="report-meta">
                <span class="meta-item">
                  <i class="material-icons">schedule</i>
                  {{ formatDateTime(report.createdAt) }}
                </span>
                <span class="meta-item">
                  <i class="material-icons">file_present</i>
                  {{ report.format.toUpperCase() }}
                </span>
                <span class="meta-item" v-if="report.size">
                  <i class="material-icons">storage</i>
                  {{ report.size }}
                </span>
              </div>
            </div>
            <div class="report-actions">
              <button 
                class="action-btn download"
                @click="downloadReport(report)"
                title="Download"
              >
                <i class="material-icons">file_download</i>
              </button>
              <button 
                class="action-btn delete"
                @click="removeReport(report)"
                title="Remover do histórico"
              >
                <i class="material-icons">delete</i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'vue-toastification';
import authService from '@/api/authService';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

export default {
  name: 'DashboardReports',
  components: {
    LoadingIndicator
  },
  props: {
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const toast = useToast();
    
    // Estado reativo
    const isRefreshing = ref(false);
    const isGeneratingCustom = ref(false);
    const generatingTemplate = ref(null);
    
    // Templates de relatórios rápidos
    const quickTemplates = ref([
      {
        id: 'daily-summary',
        name: 'Resumo Diário',
        description: 'Relatório com as atividades e métricas do dia atual',
        icon: 'today',
        color: 'blue',
        estimatedTime: '< 1 min',
        format: 'PDF',
        type: 'pedidos',
        period: 'diario'
      },
      {
        id: 'weekly-performance',
        name: 'Performance Semanal',
        description: 'Análise de performance e produtividade dos últimos 7 dias',
        icon: 'trending_up',
        color: 'green',
        estimatedTime: '2-3 min',
        format: 'PDF',
        type: 'pedidos',
        period: 'semanal'
      },
      {
        id: 'monthly-financial',
        name: 'Financeiro Mensal',
        description: 'Relatório financeiro completo com orçamentos e custos',
        icon: 'account_balance',
        color: 'orange',
        estimatedTime: '3-5 min',
        format: 'Excel',
        type: 'pedidos',
        period: 'mensal'
      },
      {
        id: 'status-overview',
        name: 'Visão Geral de Status',
        description: 'Distribuição atual de todos os pedidos por status',
        icon: 'pie_chart',
        color: 'purple',
        estimatedTime: '< 1 min',
        format: 'PDF',
        type: 'atividades',
        period: 'mensal'
      }
    ]);

    // Formulário de relatório personalizado
    const customReport = ref({
      name: '',
      type: '',
      period: 'mensal',
      format: 'pdf',
      dateFrom: '',
      dateTo: '',
      filters: {
        includeStatus: false,
        includeCategory: false,
        includeUrgency: false,
        includeSector: false
      },
      statusFilter: '',
      categoryFilter: '',
      urgencyFilter: '',
      sectorFilter: ''
    });

    // Relatórios recentes
    const recentReports = ref([]);

    // Computed properties
    const canGenerateCustom = computed(() => {
      return customReport.value.name.trim() !== '' && 
             customReport.value.type !== '';
    });

    const hasActiveFilters = computed(() => {
      return Object.values(customReport.value.filters).some(filter => filter);
    });

    // Métodos
    const refreshData = async () => {
      isRefreshing.value = true;
      try {
        // Simular refresh
        await new Promise(resolve => setTimeout(resolve, 1000));
        toast.success('Dados atualizados com sucesso!');
      } catch (error) {
        toast.error('Erro ao atualizar dados');
      } finally {
        isRefreshing.value = false;
      }
    };

    const updateDateRange = () => {
      const period = customReport.value.period;
      
      if (period === 'personalizado') {
        return;
      }
      
      // Resetar datas personalizadas quando não for período personalizado
      customReport.value.dateFrom = '';
      customReport.value.dateTo = '';
    };

    const generateQuickReport = async (template) => {
      generatingTemplate.value = template.id;
      
      try {
        // Construir URL com query parameters
        const params = new URLSearchParams({
          tipo: template.type,
          periodo: template.period,
          formato: template.format.toLowerCase() === 'excel' ? 'excel' : 'pdf'
        });

        const response = await fetch(`${process.env.VUE_APP_API_URL}/relatorios/?${params.toString()}`, {
          method: 'GET',
          headers: {
            ...authService.getAuthHeaders(),
            'Cache-Control': 'no-cache'
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Erro da API:', errorText);
          throw new Error('Erro ao gerar relatório');
        }

        // Criar blob para download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${template.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.${template.format.toLowerCase() === 'excel' ? 'xlsx' : 'pdf'}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        // Adicionar ao histórico
        const newReport = {
          id: Date.now(),
          name: `${template.name} - ${new Date().toLocaleDateString('pt-BR')}`,
          type: template.type,
          format: template.format.toLowerCase(),
          createdAt: new Date(),
          size: formatFileSize(blob.size)
        };
        recentReports.value.unshift(newReport);

        toast.success('Relatório gerado com sucesso!');
        
      } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        toast.error('Erro ao gerar relatório');
      } finally {
        generatingTemplate.value = null;
      }
    };

    const generateCustomReport = async () => {
      if (!canGenerateCustom.value) return;
      
      isGeneratingCustom.value = true;
      
      try {
        // Construir URL com query parameters
        const params = new URLSearchParams({
          tipo: customReport.value.type,
          periodo: customReport.value.period,
          formato: customReport.value.format
        });

        // Adicionar datas se for período personalizado
        if (customReport.value.period === 'personalizado') {
          if (customReport.value.dateFrom) {
            params.append('dataInicial', customReport.value.dateFrom);
          }
          if (customReport.value.dateTo) {
            params.append('dataFinal', customReport.value.dateTo);
          }
        }

        // Adicionar filtros personalizados se estiverem ativos
        if (customReport.value.filters.includeStatus && customReport.value.statusFilter) {
          params.append('status', customReport.value.statusFilter);
        }
        
        if (customReport.value.filters.includeCategory && customReport.value.categoryFilter) {
          params.append('categoria', customReport.value.categoryFilter);
        }
        
        if (customReport.value.filters.includeUrgency && customReport.value.urgencyFilter) {
          params.append('urgencia', customReport.value.urgencyFilter);
        }
        
        if (customReport.value.filters.includeSector && customReport.value.sectorFilter) {
          params.append('setor', customReport.value.sectorFilter);
        }

        console.log('Parâmetros enviados:', params.toString());

        const response = await fetch(`${process.env.VUE_APP_API_URL}/relatorios/?${params.toString()}`, {
          method: 'GET',
          headers: {
            ...authService.getAuthHeaders(),
            'Cache-Control': 'no-cache'
          }
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Erro da API:', errorText);
          throw new Error('Erro ao gerar relatório personalizado');
        }

        // Criar blob para download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        
        // Determinar extensão do arquivo baseado no formato
        let fileExtension = 'pdf';
        if (customReport.value.format === 'excel') {
          fileExtension = 'xlsx';
        } else if (customReport.value.format === 'csv') {
          fileExtension = 'csv';
        }
        
        link.download = `${customReport.value.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.${fileExtension}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

        // Adicionar ao histórico
        const newReport = {
          id: Date.now(),
          name: customReport.value.name,
          type: customReport.value.type,
          format: customReport.value.format,
          createdAt: new Date(),
          size: formatFileSize(blob.size),
          filters: getActiveFiltersText()
        };
        recentReports.value.unshift(newReport);

        toast.success('Relatório personalizado gerado com sucesso!');
        
      } catch (error) {
        console.error('Erro ao gerar relatório personalizado:', error);
        toast.error('Erro ao gerar relatório personalizado');
      } finally {
        isGeneratingCustom.value = false;
      }
    };

    const resetForm = () => {
      customReport.value = {
        name: '',
        type: '',
        period: 'mensal',
        format: 'pdf',
        dateFrom: '',
        dateTo: '',
        filters: {
          includeStatus: false,
          includeCategory: false,
          includeUrgency: false,
          includeSector: false
        },
        statusFilter: '',
        categoryFilter: '',
        urgencyFilter: '',
        sectorFilter: ''
      };
    };

    const downloadReport = (report) => {
      // Simular download (na implementação real, seria um link para o arquivo)
      toast.info(`Download do relatório "${report.name}" iniciado`);
    };

    const removeReport = (report) => {
      const index = recentReports.value.findIndex(r => r.id === report.id);
      if (index > -1) {
        recentReports.value.splice(index, 1);
        toast.success('Relatório removido do histórico');
      }
    };

    const clearRecentReports = () => {
      recentReports.value = [];
      toast.success('Histórico de relatórios limpo');
    };

    // Funções auxiliares
    const getTypeLabel = (type) => {
      const labels = {
        'pedidos': 'Relatório de Pedidos',
        'atividades': 'Relatório de Atividades'
      };
      return labels[type] || 'Não definido';
    };

    const getPeriodLabel = (period) => {
      const labels = {
        'diario': 'Hoje',
        'semanal': 'Esta Semana',
        'mensal': 'Este Mês',
        'personalizado': 'Período Personalizado'
      };
      return labels[period] || 'Não definido';
    };

    const getReportIcon = (type) => {
      const icons = {
        'pedidos': 'description',
        'atividades': 'analytics'
      };
      return icons[type] || 'description';
    };

    const formatDateTime = (date) => {
      return new Date(date).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const getActiveFiltersText = () => {
      const filters = [];
      if (customReport.value.filters.includeStatus && customReport.value.statusFilter) {
        filters.push(`Status: ${customReport.value.statusFilter}`);
      }
      if (customReport.value.filters.includeCategory && customReport.value.categoryFilter) {
        filters.push(`Categoria: ${customReport.value.categoryFilter}`);
      }
      if (customReport.value.filters.includeUrgency && customReport.value.urgencyFilter) {
        filters.push(`Urgência: ${customReport.value.urgencyFilter}`);
      }
      if (customReport.value.filters.includeSector && customReport.value.sectorFilter) {
        filters.push(`Setor: ${customReport.value.sectorFilter}`);
      }
      return filters.join(', ');
    };

    // Lifecycle
    onMounted(() => {
      // Inicializar datas padrão
      const currentDate = new Date();
      const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
      customReport.value.dateFrom = firstDayOfMonth.toISOString().split('T')[0];
      customReport.value.dateTo = currentDate.toISOString().split('T')[0];
    });

    return {
      // Estado
      isRefreshing,
      isGeneratingCustom,
      generatingTemplate,
      
      // Dados
      quickTemplates,
      customReport,
      recentReports,
      
      // Computed
      canGenerateCustom,
      hasActiveFilters,
      
      // Métodos
      refreshData,
      updateDateRange,
      generateQuickReport,
      generateCustomReport,
      resetForm,
      downloadReport,
      removeReport,
      clearRecentReports,
      getTypeLabel,
      getPeriodLabel,
      getReportIcon,
      formatDateTime,
      getActiveFiltersText
    };
  }
};
</script>

<style scoped>
.reports-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.reports-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Section Headers */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid #333;
}

.section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: #f5f5f5;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.section-header h3 i {
  color: #ff6f61;
  font-size: var(--font-size-xl);
}

/* Buttons */
.refresh-btn, .btn-primary, .btn-secondary {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: var(--font-size-sm);
  font-weight: 500;
  border: none;
}

.refresh-btn, .btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #f5f5f5;
}

.refresh-btn:hover:not(:disabled), .btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-primary {
  background: linear-gradient(135deg, #ff6f61, #ff8a80);
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #e74c3c, #ff6f61);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 111, 97, 0.3);
}

.btn-primary:disabled, .btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary.small {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Quick Reports Grid */
.quick-reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.report-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid #333;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.report-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff6f61, #ff8a80);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.report-card:hover::before {
  opacity: 1;
}

.report-card.generating {
  opacity: 0.7;
  cursor: not-allowed;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon.blue {
  background: linear-gradient(135deg, #42a5f5, #64b5f6);
}

.card-icon.green {
  background: linear-gradient(135deg, #66bb6a, #81c784);
}

.card-icon.orange {
  background: linear-gradient(135deg, #ffa726, #ffcc02);
}

.card-icon.purple {
  background: linear-gradient(135deg, #ab47bc, #ba68c8);
}

.card-icon i {
  color: white;
  font-size: var(--font-size-xl);
}

.card-content {
  flex: 1;
}

.card-content h4 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #f5f5f5;
  font-size: var(--font-size-md);
  font-weight: 600;
}

.card-content p {
  margin: 0 0 var(--spacing-sm) 0;
  color: #aaa;
  font-size: var(--font-size-sm);
  line-height: 1.4;
}

.card-meta {
  display: flex;
  gap: var(--spacing-md);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: var(--font-size-xs);
  color: #888;
}

.meta-item i {
  font-size: var(--font-size-sm);
}

.card-action {
  flex-shrink: 0;
}

.card-action i {
  color: #ff6f61;
  font-size: var(--font-size-lg);
}

/* Report Builder */
.report-builder {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

.builder-form {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-sm);
  color: #f5f5f5;
  font-weight: 500;
}

.form-group label i {
  color: #ff6f61;
  font-size: var(--font-size-md);
}

.form-input, .form-select {
  padding: var(--spacing-sm);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-sm);
  background: rgba(255, 255, 255, 0.05);
  color: #f5f5f5;
  font-size: var(--font-size-sm);
  transition: all 0.3s ease;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #ff6f61;
  background: rgba(255, 255, 255, 0.08);
}

.date-range-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

/* Filters Section */
.filters-section {
  margin-bottom: var(--spacing-lg);
}

.filters-section h4 {
  margin: 0 0 var(--spacing-md) 0;
  color: #f5f5f5;
  font-size: var(--font-size-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.filters-section h4 i {
  color: #ff6f61;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.filter-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: #f5f5f5;
}

.filter-checkbox {
  display: none;
}

.checkbox-custom {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  position: relative;
  transition: all 0.3s ease;
}

.filter-checkbox:checked + .checkbox-custom {
  background: #ff6f61;
  border-color: #ff6f61;
}

.filter-checkbox:checked + .checkbox-custom::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.filter-select {
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius-sm);
  background: rgba(255, 255, 255, 0.05);
  color: #f5f5f5;
  font-size: var(--font-size-xs);
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
}

/* Report Preview */
.report-preview {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: fit-content;
  position: sticky;
  top: var(--spacing-md);
}

.preview-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-header h4 {
  margin: 0;
  color: #f5f5f5;
  font-size: var(--font-size-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.preview-header h4 i {
  color: #ff6f61;
}

.preview-content {
  padding: var(--spacing-md);
}

.preview-empty {
  text-align: center;
  color: #888;
  padding: var(--spacing-xl);
}

.preview-empty i {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-sm);
  color: #555;
}

.preview-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.preview-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.preview-label {
  font-size: var(--font-size-xs);
  color: #888;
  font-weight: 500;
}

.preview-value {
  font-size: var(--font-size-sm);
  color: #f5f5f5;
}

.preview-filters {
  margin-top: var(--spacing-sm);
  padding-top: var(--spacing-sm);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-xs);
}

.filter-tag {
  background: rgba(255, 111, 97, 0.2);
  color: #ff6f61;
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  border: 1px solid rgba(255, 111, 97, 0.3);
}

/* Reports List */
.reports-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.report-item {
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.report-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.report-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 111, 97, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.report-icon i {
  color: #ff6f61;
  font-size: var(--font-size-md);
}

.report-info {
  flex: 1;
}

.report-info h5 {
  margin: 0 0 var(--spacing-xs) 0;
  color: #f5f5f5;
  font-size: var(--font-size-sm);
  font-weight: 600;
}

.report-meta {
  display: flex;
  gap: var(--spacing-md);
}

.report-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.download {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.action-btn.download:hover {
  background: rgba(76, 175, 80, 0.3);
  transform: scale(1.1);
}

.action-btn.delete {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
}

.action-btn.delete:hover {
  background: rgba(244, 67, 54, 0.3);
  transform: scale(1.1);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: #777;
  text-align: center;
}

.empty-state i {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-sm);
  color: #555;
}

.empty-state p {
  font-size: var(--font-size-md);
  margin: 0 0 var(--spacing-xs) 0;
  color: #aaa;
}

.empty-state span {
  font-size: var(--font-size-sm);
  color: #777;
}

/* Responsividade */
@media (max-width: 1024px) {
  .report-builder {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .quick-reports-grid {
    grid-template-columns: 1fr;
  }
  
  .report-card {
    flex-direction: column;
    text-align: center;
  }
  
  .date-range-group {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .report-item {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
  
  .report-meta {
    justify-content: center;
  }
  
  .report-actions {
    justify-content: center;
  }
}
</style> 