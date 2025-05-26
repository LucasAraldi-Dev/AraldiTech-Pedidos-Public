<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" @click.stop>
      <!-- Header do Modal -->
      <div class="modal-header">
        <div class="header-content">
          <div class="header-title">
            <i class="material-icons">account_balance_wallet</i>
            <h2>Gestão Financeira</h2>
          </div>
          <div class="header-actions">
            <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
              <i class="material-icons" :class="{ 'spinning': isLoading }">refresh</i>
              <span>{{ isLoading ? 'Atualizando...' : 'Atualizar' }}</span>
            </button>
        <button class="close-btn" @click="$emit('close')">
          <i class="material-icons">close</i>
        </button>
          </div>
        </div>
      </div>
      
      <!-- Aviso de Desenvolvimento -->
      <div class="development-warning-banner">
        <div class="warning-content">
          <i class="material-icons warning-icon">construction</i>
          <div class="warning-text">
            <h4>🚧 EM DESENVOLVIMENTO</h4>
            <p>
              O sistema de gestão financeira está em desenvolvimento ativo. 
              Algumas funcionalidades podem estar incompletas ou apresentar instabilidades.
            </p>
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
          <div class="loading-spinner"></div>
          <p class="loading-text">Carregando dados financeiros...</p>
        </div>
              
        <!-- Todas as abas ficam montadas, apenas alternamos visibilidade -->
        <div v-else class="tabs-container">
          <!-- Aba: Visão Geral -->
          <div 
            class="tab-content overview-tab financial-overview" 
            :class="{ 'tab-active': activeTab === 'overview', 'tab-hidden': activeTab !== 'overview' }"
          >
            <!-- Header da Visão Geral -->
            <div class="overview-header">
              <div class="overview-title">
                <h2>
                  <i class="material-icons">dashboard</i>
                  Visão Geral Financeira
                </h2>
                <p class="overview-subtitle">
                  Acompanhe o desempenho financeiro em tempo real
                  <span class="last-update">• Última atualização: {{ lastUpdate }}</span>
                </p>
              </div>
                            <div class="overview-actions">
                <button class="action-btn primary" @click="refreshData" :disabled="isLoading">
                  <i class="material-icons" :class="{ 'spinning': isLoading }">refresh</i>
                  <span class="btn-text">{{ isLoading ? 'Atualizando...' : 'Atualizar Dados' }}</span>
                </button>
                <button class="action-btn secondary" @click="setActiveTab('reports')">
                  <i class="material-icons">description</i>
                  <span class="btn-text">Ver Relatórios</span>
                </button>
                </div>
              </div>
              
            <!-- Cards de Métricas Principais -->
            <div class="main-metrics-container">
              <div class="metrics-grid">
                <!-- Card Orçamento Total -->
                <div class="metric-card primary-card">
                  <div class="card-header">
                    <div class="card-icon primary">
                      <i class="material-icons">account_balance_wallet</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="setActiveTab('budget-config')" title="Configurar Orçamentos">
                        <i class="material-icons">settings</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">Orçamento Total</h3>
                    <div class="card-value primary">R$ {{ formatCurrency(orcamentoTotal) }}</div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">business</i>
                        <span class="detail-text">{{ setores.length }} setores</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">trending_up</i>
                        <span class="detail-text">{{ orcamentoTrend >= 0 ? '+' : '' }}{{ orcamentoTrend }}% período</span>
                      </div>
                    </div>
                </div>
              </div>
              
                <!-- Card Custo Realizado -->
                <div class="metric-card warning-card">
                  <div class="card-header">
                    <div class="card-icon warning">
                      <i class="material-icons">shopping_cart</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="filterByStatus('Concluído')" title="Ver Pedidos Concluídos">
                        <i class="material-icons">filter_list</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">Custo Realizado</h3>
                    <div class="card-value warning">R$ {{ formatCurrency(custoRealTotal) }}</div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">receipt</i>
                        <span class="detail-text">{{ pedidosComCusto }} executados</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">trending_up</i>
                        <span class="detail-text">{{ custoTrend >= 0 ? '+' : '' }}{{ custoTrend }}% período</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Card Saldo/Economia -->
                <div class="metric-card" :class="saldoFinanceiro >= 0 ? 'success-card' : 'danger-card'">
                  <div class="card-header">
                    <div class="card-icon" :class="saldoFinanceiro >= 0 ? 'success' : 'danger'">
                      <i class="material-icons">{{ saldoIcon }}</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="showBudgetAnalysis" title="Análise Detalhada">
                        <i class="material-icons">analytics</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">{{ saldoLabel }}</h3>
                    <div class="card-value" :class="saldoFinanceiro >= 0 ? 'success' : 'danger'">
                    R$ {{ formatCurrency(Math.abs(saldoFinanceiro)) }}
                  </div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">{{ saldoFinanceiro >= 0 ? 'check_circle' : 'error' }}</i>
                        <span class="detail-text">{{ saldoFinanceiro >= 0 ? 'Dentro do orçamento' : 'Acima do orçamento' }}</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">percent</i>
                        <span class="detail-text">{{ saldoPercentage }}% do total</span>
                      </div>
                </div>
              </div>
            </div>
            
                <!-- Card Eficiência -->
                <div class="metric-card info-card">
                  <div class="card-header">
                    <div class="card-icon info">
                      <i class="material-icons">speed</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="showEfficiencyDetails" title="Detalhes da Eficiência">
                        <i class="material-icons">info</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">Eficiência</h3>
                    <div class="card-value info">{{ eficienciaFinanceira }}%</div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">{{ getEfficiencyIcon() }}</i>
                        <span class="detail-text">{{ eficienciaDescription }}</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">assessment</i>
                        <span class="detail-text">{{ getEfficiencyLevel() }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Card Pedidos Pendentes -->
                <div class="metric-card neutral-card">
                  <div class="card-header">
                    <div class="card-icon neutral">
                      <i class="material-icons">pending_actions</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="filterByStatus('Pendente')" title="Ver Pedidos Pendentes">
                        <i class="material-icons">list</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">Pendentes</h3>
                    <div class="card-value neutral">{{ pedidosPendentes }}</div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">schedule</i>
                        <span class="detail-text">Aguardando execução</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">attach_money</i>
                        <span class="detail-text">R$ {{ formatCurrency(valorPendente) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Card Média por Pedido -->
                <div class="metric-card secondary-card">
                  <div class="card-header">
                    <div class="card-icon secondary">
                      <i class="material-icons">calculate</i>
                    </div>
                    <div class="card-actions">
                      <button class="mini-btn" @click="showMonthlyTrend" title="Ver Tendência">
                        <i class="material-icons">trending_up</i>
                      </button>
                    </div>
                  </div>
                  <div class="card-content">
                    <h3 class="card-title">Média/Pedido</h3>
                    <div class="card-value secondary">R$ {{ formatCurrency(mediaPorPedido) }}</div>
                    <div class="card-details">
                      <div class="detail-item">
                        <i class="material-icons">receipt_long</i>
                        <span class="detail-text">{{ pedidosComFinancas.length }} pedidos</span>
                      </div>
                      <div class="detail-item">
                        <i class="material-icons">calendar_month</i>
                        <span class="detail-text">Últimos 30 dias</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cards de Resumo Adicional -->
            <div class="summary-cards-container">
              <div class="section-header">
                <h3>
                  <i class="material-icons">insights</i>
                  Resumo Executivo
                </h3>
              </div>
              
              <div class="summary-grid">
                <!-- Card Tempo Médio -->
                <div class="summary-card time-card">
                  <div class="summary-icon">
                    <i class="material-icons">schedule</i>
                  </div>
                  <div class="summary-content">
                    <h4>Tempo Médio</h4>
                    <div class="summary-value">{{ tempoMedioExecucao }} dias</div>
                    <p>Para conclusão</p>
                  </div>
                </div>

                <!-- Card Maior Pedido -->
                <div class="summary-card value-card">
                  <div class="summary-icon">
                    <i class="material-icons">trending_up</i>
                  </div>
                  <div class="summary-content">
                    <h4>Maior Pedido</h4>
                    <div class="summary-value">R$ {{ formatCurrency(maiorPedidoValor) }}</div>
                    <p>{{ maiorPedidoCategoria }}</p>
                  </div>
                </div>

                <!-- Card Taxa de Conclusão -->
                <div class="summary-card completion-card">
                  <div class="summary-icon">
                    <i class="material-icons">check_circle</i>
                  </div>
                  <div class="summary-content">
                    <h4>Taxa Conclusão</h4>
                    <div class="summary-value">{{ taxaConclusao }}%</div>
                    <p>Pedidos finalizados</p>
                  </div>
                </div>

                <!-- Card Economia Mensal -->
                <div class="summary-card savings-card">
                  <div class="summary-icon">
                    <i class="material-icons">savings</i>
                  </div>
                  <div class="summary-content">
                    <h4>Economia Mensal</h4>
                    <div class="summary-value">R$ {{ formatCurrency(economiaMensal) }}</div>
                    <p>Vs orçamento previsto</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Cards de Ações Rápidas -->
            <div class="quick-actions-container">
              <div class="section-header">
                <h3>
                  <i class="material-icons">flash_on</i>
                  Ações Rápidas
                </h3>
              </div>
              
              <div class="quick-actions-grid">
                <!-- Busca Rápida -->
                <div class="action-card search-card">
                  <div class="action-header">
                    <i class="material-icons">search</i>
                    <h4>Busca Rápida</h4>
                  </div>
                  <div class="action-content">
                    <div class="search-container">
                      <input 
                        type="text" 
                        placeholder="Buscar pedidos, categorias..." 
                        v-model="quickSearchTerm"
                        @keyup.enter="performQuickSearch"
                        class="quick-search-input"
                      />
                      <button class="search-btn" @click="performQuickSearch">
                        <i class="material-icons">search</i>
                      </button>
                    </div>
                    <div class="search-suggestions" v-if="searchSuggestions.length > 0">
                      <div 
                        v-for="suggestion in searchSuggestions.slice(0, 3)" 
                        :key="suggestion.id"
                        class="suggestion-item"
                        @click="selectSuggestion(suggestion)"
                      >
                        <i class="material-icons">{{ suggestion.icon }}</i>
                        <span>{{ suggestion.text }}</span>
                        <small>{{ suggestion.type }}</small>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Filtros Rápidos -->
                <div class="action-card filters-card">
                  <div class="action-header">
                    <i class="material-icons">filter_list</i>
                    <h4>Filtros Rápidos</h4>
                  </div>
                  <div class="action-content">
                    <div class="filter-buttons">
                      <button 
                        class="filter-btn" 
                        :class="{ active: quickFilter === 'over-budget' }"
                        @click="applyQuickFilter('over-budget')"
                      >
                        <i class="material-icons">trending_up</i>
                        <span>Acima do Orçamento</span>
                        <div class="filter-count">{{ pedidosAcimaOrcamento }}</div>
                      </button>
                      <button 
                        class="filter-btn" 
                        :class="{ active: quickFilter === 'high-value' }"
                        @click="applyQuickFilter('high-value')"
                      >
                        <i class="material-icons">attach_money</i>
                        <span>Alto Valor</span>
                        <div class="filter-count">{{ pedidosAltoValor }}</div>
                      </button>
                      <button 
                        class="filter-btn" 
                        :class="{ active: quickFilter === 'recent' }"
                        @click="applyQuickFilter('recent')"
                      >
                        <i class="material-icons">schedule</i>
                        <span>Recentes</span>
                        <div class="filter-count">{{ pedidosRecentes }}</div>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Estatísticas Rápidas -->
                <div class="action-card stats-card">
                  <div class="action-header">
                    <i class="material-icons">bar_chart</i>
                    <h4>Estatísticas</h4>
                  </div>
                  <div class="action-content">
                    <div class="stats-list">
                      <div class="stat-item" @click="showCategoryDetails('maior-gasto')">
                        <div class="stat-icon">
                          <i class="material-icons">trending_up</i>
                        </div>
                        <div class="stat-info">
                          <span class="stat-label">Maior Gasto</span>
                          <span class="stat-value">{{ maiorGastoCategoria.nome }}</span>
                          <small>R$ {{ formatCurrency(maiorGastoCategoria.valor) }}</small>
                        </div>
                      </div>
                      <div class="stat-item" @click="showCategoryDetails('mais-pedidos')">
                        <div class="stat-icon">
                          <i class="material-icons">receipt_long</i>
                        </div>
                        <div class="stat-info">
                          <span class="stat-label">Mais Pedidos</span>
                          <span class="stat-value">{{ categoriaMaisPedidos.nome }}</span>
                          <small>{{ categoriaMaisPedidos.count }} pedidos</small>
                        </div>
                      </div>
                      <div class="stat-item" @click="showMonthlyTrend">
                        <div class="stat-icon">
                          <i class="material-icons">calendar_month</i>
                        </div>
                        <div class="stat-info">
                          <span class="stat-label">Média Mensal</span>
                          <span class="stat-value">R$ {{ formatCurrency(mediaMensal) }}</span>
                          <small>Últimos 3 meses</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Progresso do Orçamento Melhorado -->
            <div class="budget-progress-container">
              <div class="section-header">
                <h3>
                  <i class="material-icons">timeline</i>
                  Utilização do Orçamento por Setor
                </h3>
                <button class="action-btn secondary" @click="setActiveTab('budget-config')">
                  <i class="material-icons">tune</i>
                  <span>Configurar</span>
                </button>
              </div>

              <div class="budget-sectors-grid">
                <div 
                  v-for="setor in setores" 
                  :key="setor.id" 
                  class="sector-card"
                  @click="showSectorDetails(setor)"
                >
                  <div class="sector-header">
                    <div class="sector-icon">
                      <i class="material-icons">{{ setor.icon }}</i>
                    </div>
                    <div class="sector-info">
                      <h4>{{ setor.nome }}</h4>
                      <p>{{ setor.descricao }}</p>
                    </div>
                    <div class="sector-percentage">
                      {{ getSectorPercentage(setor) }}%
                    </div>
                  </div>
                  
                  <div class="sector-progress">
                    <div class="progress-bar">
                      <div 
                        class="progress-fill" 
                        :class="getSectorProgressClass(setor)"
                        :style="{ width: Math.min(getSectorPercentage(setor), 100) + '%' }"
                      ></div>
              </div>
              <div class="progress-labels">
                      <span class="used">Usado: R$ {{ formatCurrency(setor.gasto_atual || 0) }}</span>
                      <span class="available">Disponível: R$ {{ formatCurrency((setor.orcamento_mensal || 0) - (setor.gasto_atual || 0)) }}</span>
                    </div>
                  </div>
              </div>
            </div>
          </div>
          
            <!-- Top Categorias -->
            <div class="categories-section">
              <div class="section-header">
                <h3>
                  <i class="material-icons">category</i>
                  Top Categorias por Custo
                </h3>
                <button class="action-btn secondary" @click="showAllCategories">
                  <i class="material-icons">list</i>
                  <span>Ver Todas</span>
                </button>
              </div>
              
              <div class="categories-card">
                <div v-if="topCategorias.length === 0" class="empty-state">
                  <i class="material-icons">info</i>
                  <p>Nenhuma categoria com custos encontrada</p>
                </div>

                <div v-else class="categories-list">
                  <div 
                    v-for="(categoria, index) in topCategorias" 
                    :key="categoria.name" 
                    class="category-item"
                    @click="filterByCategory(categoria.name)"
                  >
                    <div class="category-rank">{{ index + 1 }}</div>
                    <div class="category-content">
                      <div class="category-header">
                        <span class="category-name">{{ categoria.name }}</span>
                        <span class="category-value">R$ {{ formatCurrency(categoria.value) }}</span>
                      </div>
                      <div class="category-bar">
                        <div 
                          class="category-fill" 
                          :style="{ width: categoria.percentage + '%' }"
                        ></div>
                      </div>
                      <div class="category-details">
                        <span class="category-percentage">{{ categoria.percentage }}% do total</span>
                        <span class="category-count">{{ getCategoryCount(categoria.name) }} pedidos</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Alertas Melhorados -->
            <div v-if="financialAlerts.length > 0" class="alerts-container">
              <div class="section-header">
                <h3>
                  <i class="material-icons">warning</i>
                  Alertas e Notificações
                </h3>
                <button class="action-btn secondary" @click="dismissAllAlerts">
                  <i class="material-icons">clear_all</i>
                  <span>Limpar Todos</span>
                </button>
              </div>

              <div class="alerts-grid">
                <div 
                  v-for="alert in financialAlerts" 
                  :key="alert.id" 
                  class="alert-card"
                  :class="alert.type"
                >
                  <div class="alert-header">
                    <div class="alert-icon">
                      <i class="material-icons">{{ alert.icon }}</i>
                    </div>
                    <div class="alert-actions">
                      <button class="mini-btn" @click="dismissAlert(alert.id)" title="Dispensar">
                        <i class="material-icons">close</i>
                      </button>
                    </div>
                  </div>
                  <div class="alert-content">
                    <h5 class="alert-title">{{ alert.title }}</h5>
                    <p class="alert-message">{{ alert.message }}</p>
                    <div class="alert-footer" v-if="alert.action">
                      <button class="alert-action-btn" @click="executeAlertAction(alert)">
                        <i class="material-icons">{{ alert.actionIcon }}</i>
                        <span>{{ alert.actionText }}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
                
          <!-- Aba: Relatórios -->
          <div 
            class="tab-content reports-tab" 
            :class="{ 'tab-active': activeTab === 'reports', 'tab-hidden': activeTab !== 'reports' }"
          >
            <!-- Tabela de Pedidos Financeiros -->
            <div class="financial-table-section">
              <div class="section-header">
            <h3>
              <i class="material-icons">list_alt</i>
                  Detalhes por Pedido
            </h3>
                <div class="table-controls">
                  <div class="search-box">
                    <i class="material-icons">search</i>
                    <input 
                      type="text" 
                      placeholder="Buscar pedidos..." 
                      v-model="searchTerm"
                      class="search-input"
                    />
                  </div>
                  <select v-model="filterStatus" class="filter-select">
                    <option value="">Todos os status</option>
                    <option value="Pendente">Pendente</option>
                    <option value="Concluído">Concluído</option>
                    <option value="Cancelado">Cancelado</option>
                  </select>
                </div>
              </div>
              
              <div class="table-container">
            <table class="financial-table">
              <thead>
                <tr>
                      <th @click="sortBy('id')" class="sortable">
                        ID
                        <i class="material-icons sort-icon">{{ getSortIcon('id') }}</i>
                      </th>
                      <th @click="sortBy('descricao')" class="sortable">
                        Descrição
                        <i class="material-icons sort-icon">{{ getSortIcon('descricao') }}</i>
                      </th>
                      <th @click="sortBy('categoria')" class="sortable">
                        Categoria
                        <i class="material-icons sort-icon">{{ getSortIcon('categoria') }}</i>
                      </th>
                      <th @click="sortBy('orcamento_previsto')" class="sortable">
                        Orçamento
                        <i class="material-icons sort-icon">{{ getSortIcon('orcamento_previsto') }}</i>
                      </th>
                      <th @click="sortBy('custo_real')" class="sortable">
                        Custo Real
                        <i class="material-icons sort-icon">{{ getSortIcon('custo_real') }}</i>
                      </th>
                  <th>Diferença</th>
                  <th>Status</th>
                      <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                    <tr v-if="pedidosFiltrados.length === 0" class="empty-row">
                      <td colspan="8" class="empty-cell">
                        <div class="empty-state">
                          <i class="material-icons">info</i>
                          <p>{{ searchTerm ? 'Nenhum pedido encontrado com os filtros aplicados' : 'Nenhum pedido com dados financeiros encontrado' }}</p>
                        </div>
                  </td>
                </tr>
                    <tr v-for="pedido in pedidosPaginados" 
                        :key="pedido.id" 
                        class="table-row"
                        :class="{ 'over-budget': isOverBudget(pedido) }">
                      <td class="id-cell">
                        <span class="pedido-id">#{{ pedido.id }}</span>
                      </td>
                      <td class="description-cell">
                        <div class="description-content">
                          <span class="description-text" :title="pedido.descricao">
                            {{ truncateText(pedido.descricao, 40) }}
                    </span>
                          <div class="description-meta" v-if="pedido.conclusao_dados">
                            <span class="meta-tag" v-if="pedido.conclusao_dados.tem_mao_de_obra">
                              <i class="material-icons">build</i>
                              Mão de Obra
                            </span>
                            <span class="meta-tag" v-if="pedido.conclusao_dados.tem_material">
                              <i class="material-icons">inventory</i>
                              Material
                            </span>
                          </div>
                        </div>
                  </td>
                      <td class="category-cell">
                        <span class="category-badge">{{ pedido.categoria || 'N/A' }}</span>
                      </td>
                      <td class="currency-cell">
                        <span class="currency-value">R$ {{ formatCurrency(pedido.orcamento_previsto || 0) }}</span>
                      </td>
                      <td class="currency-cell">
                        <span class="currency-value">
                          R$ {{ formatCurrency(getCustoTotal(pedido)) }}
                        </span>
                        <div class="cost-breakdown" v-if="pedido.conclusao_dados && (pedido.conclusao_dados.valor_mao_de_obra > 0)">
                          <small>
                            Itens: R$ {{ formatCurrency(pedido.conclusao_dados.valor_total || 0) }}
                            <br>
                            M.O.: R$ {{ formatCurrency(pedido.conclusao_dados.valor_mao_de_obra || 0) }}
                          </small>
                        </div>
                      </td>
                      <td class="difference-cell">
                        <div class="difference-value" :class="getDiffClass(getDifference(pedido))">
                          <i class="material-icons diff-icon">{{ getDiffIcon(getDifference(pedido)) }}</i>
                          <span>R$ {{ formatCurrency(Math.abs(getDifference(pedido))) }}</span>
                        </div>
                      </td>
                      <td class="status-cell">
                    <span class="status-badge" :class="getStatusClass(pedido.status)">
                      {{ pedido.status }}
                    </span>
                  </td>
                      <td class="actions-cell">
                        <div class="action-buttons">
                          <button class="action-btn view" @click="viewPedido(pedido)" title="Ver detalhes">
                            <i class="material-icons">visibility</i>
                          </button>
                          <button class="action-btn edit" @click="editPedido(pedido)" title="Editar">
                      <i class="material-icons">edit</i>
                    </button>
                        </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
              <!-- Paginação -->
              <div class="pagination" v-if="totalPages > 1">
                <button 
                  class="pagination-btn" 
                  :disabled="currentPage === 1"
                  @click="currentPage = 1">
                  <i class="material-icons">first_page</i>
                </button>
                <button 
                  class="pagination-btn" 
                  :disabled="currentPage === 1"
                  @click="currentPage--">
                  <i class="material-icons">chevron_left</i>
                </button>
                
                <div class="pagination-info">
                  <span>{{ currentPage }} de {{ totalPages }}</span>
                  <span class="pagination-total">({{ pedidosFiltrados.length }} pedidos)</span>
                </div>
                
                <button 
                  class="pagination-btn" 
                  :disabled="currentPage === totalPages"
                  @click="currentPage++">
                  <i class="material-icons">chevron_right</i>
                </button>
                <button 
                  class="pagination-btn" 
                  :disabled="currentPage === totalPages"
                  @click="currentPage = totalPages">
                  <i class="material-icons">last_page</i>
                </button>
              </div>
            </div>
          </div>
            
          <!-- Aba: Configurações de Orçamento -->
          <div 
            class="tab-content budget-config-tab" 
            :class="{ 'tab-active': activeTab === 'budget-config', 'tab-hidden': activeTab !== 'budget-config' }"
          >
            <div class="budget-config-section">
              <div class="section-header">
                <h3>
                  <i class="material-icons">settings</i>
                  Configuração de Orçamentos por Setor
            </h3>
                <button class="btn-save-config" @click="saveBudgetConfig" :disabled="isSavingConfig">
                  <i class="material-icons">save</i>
                  {{ isSavingConfig ? 'Salvando...' : 'Salvar Configurações' }}
                </button>
          </div>

              <div class="budget-config-grid">
                <div v-for="setor in setores" :key="setor.id" class="budget-config-card">
                  <div class="config-card-header">
                    <div class="setor-icon">
                      <i class="material-icons">{{ setor.icon }}</i>
        </div>
                    <div class="setor-info">
                      <h4>{{ setor.nome }}</h4>
                      <p>{{ setor.descricao }}</p>
                    </div>
                  </div>
                  
                  <div class="config-card-body">
                    <div class="input-group">
                      <label>Orçamento Mensal (R$)</label>
                      <input 
                        type="number" 
                        v-model="setor.orcamento_mensal"
                        placeholder="0,00"
                        step="0.01"
                        min="0"
                        class="budget-input"
                      />
                    </div>
                    
                    <div class="input-group">
                      <label>Limite de Alerta (%)</label>
                      <input 
                        type="number" 
                        v-model="setor.limite_alerta"
                        placeholder="80"
                        min="0"
                        max="100"
                        class="budget-input"
                      />
                    </div>
                    
                    <div class="config-stats">
                      <div class="stat-item">
                        <span class="stat-label">Gasto Atual:</span>
                        <span class="stat-value">R$ {{ formatCurrency(setor.gasto_atual || 0) }}</span>
                      </div>
                      <div class="stat-item">
                        <span class="stat-label">Disponível:</span>
                        <span class="stat-value" :class="getDisponibilidadeClass(setor)">
                          R$ {{ formatCurrency((setor.orcamento_mensal || 0) - (setor.gasto_atual || 0)) }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;
import authService from '@/api/authService';

export default {
  name: "ModalFinanceiro",
  emits: ['close', 'edit-pedido', 'view-pedido'],
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      activeTab: 'overview',
      pedidos: [],
      isLoading: true,
      isSavingConfig: false,
      searchTerm: '',
      filterStatus: '',
      sortField: 'id',
      sortDirection: 'desc',
      currentPage: 1,
      itemsPerPage: 10,
      lastUpdate: new Date().toLocaleTimeString('pt-BR'),
      
      // Novos campos para ações rápidas
      quickSearchTerm: '',
      quickFilter: '',
      searchSuggestions: [],
      
      // Configuração de setores
      setores: [
        {
          id: 1,
          nome: 'Produção',
          descricao: 'Matérias-primas e insumos de produção',
          icon: 'precision_manufacturing',
          orcamento_mensal: 50000,
          limite_alerta: 80,
          gasto_atual: 0
        },
        {
          id: 2,
          nome: 'Manutenção',
          descricao: 'Peças de reposição e serviços de manutenção',
          icon: 'build',
          orcamento_mensal: 25000,
          limite_alerta: 75,
          gasto_atual: 0
        },
        {
          id: 3,
          nome: 'Equipamentos',
          descricao: 'Máquinas e equipamentos industriais',
          icon: 'engineering',
          orcamento_mensal: 100000,
          limite_alerta: 85,
          gasto_atual: 0
        },
        {
          id: 4,
          nome: 'Serviços',
          descricao: 'Serviços terceirizados e consultorias',
          icon: 'handyman',
          orcamento_mensal: 30000,
          limite_alerta: 70,
          gasto_atual: 0
        },
        {
          id: 5,
          nome: 'Diversos',
          descricao: 'Mercadorias e materiais diversos',
          icon: 'inventory_2',
          orcamento_mensal: 15000,
          limite_alerta: 90,
          gasto_atual: 0
        }
      ]
    };
  },
  computed: {
    tabs() {
      return [
        {
          id: 'overview',
          label: 'Visão Geral',
          icon: 'dashboard',
          badge: this.pedidosComFinancas.length || null
        },
        {
          id: 'reports',
          label: 'Relatórios',
          icon: 'description'
        },
        {
          id: 'budget-config',
          label: 'Configurações',
          icon: 'settings'
        }
      ];
    },

    // Dados financeiros principais - usando dados REAIS
    pedidosComFinancas() {
      return this.pedidos.filter(p => 
        parseFloat(p.orcamento_previsto || 0) > 0 || 
        parseFloat(this.getCustoTotal(p)) > 0
      );
    },
    
    orcamentoTotal() {
      // Usar a soma dos orçamentos configurados por setor
      return this.setores.reduce((total, setor) => {
        return total + parseFloat(setor.orcamento_mensal || 0);
      }, 0);
    },

    orcamentoPedidos() {
      // Orçamento baseado apenas nos pedidos (para comparação)
      return this.pedidosComFinancas.reduce((total, pedido) => {
        return total + parseFloat(pedido.orcamento_previsto || 0);
      }, 0);
    },
    
    custoRealTotal() {
      return this.pedidosComFinancas.reduce((total, pedido) => {
        return total + parseFloat(this.getCustoTotal(pedido));
      }, 0);
    },
    
    saldoFinanceiro() {
      return this.orcamentoTotal - this.custoRealTotal;
    },
    
    saldoRestante() {
      return Math.max(0, this.saldoFinanceiro);
    },
    
    // KPIs e métricas
    pedidosComOrcamento() {
      return this.pedidos.filter(p => parseFloat(p.orcamento_previsto || 0) > 0).length;
    },
    
    pedidosComCusto() {
      return this.pedidos.filter(p => parseFloat(this.getCustoTotal(p)) > 0).length;
    },
    
    saldoIcon() {
      return this.saldoFinanceiro >= 0 ? 'savings' : 'money_off';
    },
    
    saldoLabel() {
      return this.saldoFinanceiro >= 0 ? 'Economia' : 'Déficit';
    },
    
    saldoDescription() {
      if (this.saldoFinanceiro >= 0) {
        return 'Dentro do orçamento planejado';
      } else {
        return 'Acima do orçamento planejado';
      }
    },
    
    saldoPercentage() {
      if (this.orcamentoTotal === 0) return 0;
      return Math.abs(Math.round((this.saldoFinanceiro / this.orcamentoTotal) * 100));
    },
    
    progressPercentage() {
      if (this.orcamentoTotal === 0) return 0;
      return Math.round((this.custoRealTotal / this.orcamentoTotal) * 100);
    },
    
    progressClass() {
      if (this.progressPercentage < 70) return 'good';
      if (this.progressPercentage < 90) return 'warning';
      return 'danger';
    },
    
    eficienciaFinanceira() {
      if (this.orcamentoTotal === 0) return 100;
      if (this.custoRealTotal === 0) return 100;
      
      // Calcular eficiência baseada na proximidade do orçamento vs custo real
      const ratio = this.custoRealTotal / this.orcamentoTotal;
      if (ratio <= 1) {
        // Dentro do orçamento - eficiência alta
        return Math.round(100 - (ratio * 10)); // 90-100%
      } else {
        // Acima do orçamento - eficiência baixa
        return Math.max(0, Math.round(100 - ((ratio - 1) * 100))); // 0-90%
      }
    },
    
    eficienciaDescription() {
      if (this.eficienciaFinanceira >= 90) return 'Excelente gestão';
      if (this.eficienciaFinanceira >= 70) return 'Boa gestão';
      if (this.eficienciaFinanceira >= 50) return 'Gestão regular';
      return 'Necessita atenção';
    },
    
    // Trends baseados em dados reais dos últimos pedidos
    orcamentoTrend() {
      if (this.pedidos.length < 2) return 0;
      
      const pedidosRecentes = this.pedidos
        .filter(p => parseFloat(p.orcamento_previsto || 0) > 0)
        .sort((a, b) => new Date(b.created_at || b.data_criacao) - new Date(a.created_at || a.data_criacao))
        .slice(0, 10);
      
      if (pedidosRecentes.length < 2) return 0;
      
      const metadeRecente = pedidosRecentes.slice(0, Math.floor(pedidosRecentes.length / 2));
      const metadeAntiga = pedidosRecentes.slice(Math.floor(pedidosRecentes.length / 2));
      
      const mediaRecente = metadeRecente.reduce((sum, p) => sum + parseFloat(p.orcamento_previsto || 0), 0) / metadeRecente.length;
      const mediaAntiga = metadeAntiga.reduce((sum, p) => sum + parseFloat(p.orcamento_previsto || 0), 0) / metadeAntiga.length;
      
      if (mediaAntiga === 0) return 0;
      return Math.round(((mediaRecente - mediaAntiga) / mediaAntiga) * 100);
    },
    
    custoTrend() {
      if (this.pedidos.length < 2) return 0;
      
      const pedidosComCusto = this.pedidos
        .filter(p => parseFloat(this.getCustoTotal(p)) > 0)
        .sort((a, b) => new Date(b.created_at || b.data_criacao) - new Date(a.created_at || a.data_criacao))
        .slice(0, 10);
      
      if (pedidosComCusto.length < 2) return 0;
      
      const metadeRecente = pedidosComCusto.slice(0, Math.floor(pedidosComCusto.length / 2));
      const metadeAntiga = pedidosComCusto.slice(Math.floor(pedidosComCusto.length / 2));
      
      const mediaRecente = metadeRecente.reduce((sum, p) => sum + this.getCustoTotal(p), 0) / metadeRecente.length;
      const mediaAntiga = metadeAntiga.reduce((sum, p) => sum + this.getCustoTotal(p), 0) / metadeAntiga.length;
      
      if (mediaAntiga === 0) return 0;
      return Math.round(((mediaRecente - mediaAntiga) / mediaAntiga) * 100);
    },
    
    // Filtros e ordenação
    pedidosFiltrados() {
      let filtered = [...this.pedidosComFinancas];
      
      // Filtro por busca
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase();
        filtered = filtered.filter(p => 
          p.descricao.toLowerCase().includes(term) ||
          p.categoria?.toLowerCase().includes(term) ||
          p.id.toString().includes(term)
        );
      }
      
      // Filtro por status
      if (this.filterStatus) {
        filtered = filtered.filter(p => p.status === this.filterStatus);
      }
      
      // Filtros rápidos
      if (this.quickFilter) {
        switch (this.quickFilter) {
          case 'over-budget':
            filtered = filtered.filter(p => this.isOverBudget(p));
            break;
          case 'high-value': {
            const valorAlto = this.custoRealTotal / this.pedidosComFinancas.length * 2;
            filtered = filtered.filter(p => this.getCustoTotal(p) > valorAlto);
            break;
          }
          case 'recent': {
            const umaSemanaAtras = new Date();
            umaSemanaAtras.setDate(umaSemanaAtras.getDate() - 7);
            filtered = filtered.filter(p => {
              const dataPedido = new Date(p.created_at || p.data_criacao);
              return dataPedido >= umaSemanaAtras;
            });
            break;
          }
        }
      }
      
      // Ordenação
      filtered.sort((a, b) => {
        let aVal = a[this.sortField];
        let bVal = b[this.sortField];
        
        // Tratamento especial para valores numéricos
        if (this.sortField === 'orcamento_previsto') {
          aVal = parseFloat(a.orcamento_previsto || 0);
          bVal = parseFloat(b.orcamento_previsto || 0);
        } else if (this.sortField === 'custo_real') {
          aVal = this.getCustoTotal(a);
          bVal = this.getCustoTotal(b);
        }
        
        if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase();
          bVal = bVal.toLowerCase();
        }
        
        if (this.sortDirection === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
      
      return filtered;
    },
    
    // Paginação
    totalPages() {
      return Math.ceil(this.pedidosFiltrados.length / this.itemsPerPage);
    },
    
    pedidosPaginados() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.pedidosFiltrados.slice(start, end);
    },

    // Computed para a aba Visão Geral

    topCategorias() {
      const categoriasCusto = {};
      
      this.pedidosComFinancas.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        const custo = this.getCustoTotal(pedido);
        categoriasCusto[categoria] = (categoriasCusto[categoria] || 0) + custo;
      });
      
      const maxValue = Math.max(...Object.values(categoriasCusto));
      
      return Object.entries(categoriasCusto)
        .map(([name, value]) => ({
          name,
          value,
          percentage: maxValue > 0 ? Math.round((value / maxValue) * 100) : 0
        }))
        .sort((a, b) => b.value - a.value)
        .slice(0, 5);
    },

    financialAlerts() {
      const alerts = [];
      let alertId = 1;
      
      // Obter alertas dispensados
      const dismissedAlerts = JSON.parse(localStorage.getItem('dismissed_alerts') || '[]');

      // Alerta de orçamento estourado
      if (this.saldoFinanceiro < 0 && !dismissedAlerts.includes(alertId)) {
        alerts.push({
          id: alertId++,
          type: 'danger',
          icon: 'error',
          title: 'Orçamento Excedido',
          message: `O custo real excedeu o orçamento em R$ ${this.formatCurrency(Math.abs(this.saldoFinanceiro))}`,
          action: true,
          actionIcon: 'filter_list',
          actionText: 'Ver Pedidos Acima do Orçamento'
        });
      } else {
        alertId++;
      }

      // Alerta de eficiência baixa
      if (this.eficienciaFinanceira < 50 && !dismissedAlerts.includes(alertId)) {
        alerts.push({
          id: alertId++,
          type: 'warning',
          icon: 'warning',
          title: 'Eficiência Baixa',
          message: 'A eficiência financeira está abaixo de 50%. Revise os processos de controle de custos.',
          action: true,
          actionIcon: 'analytics',
          actionText: 'Analisar Eficiência'
        });
      } else {
        alertId++;
      }

      // Alerta de muitos pedidos sem orçamento
      const pedidosSemOrcamento = this.pedidos.filter(p => !parseFloat(p.orcamento_previsto || 0)).length;
      if (pedidosSemOrcamento > this.pedidos.length * 0.3 && !dismissedAlerts.includes(alertId)) {
        alerts.push({
          id: alertId++,
          type: 'info',
          icon: 'info',
          title: 'Pedidos sem Orçamento',
          message: `${pedidosSemOrcamento} pedidos não possuem orçamento definido. Considere definir orçamentos para melhor controle.`,
          action: true,
          actionIcon: 'edit',
          actionText: 'Ver Pedidos sem Orçamento'
        });
      } else {
        alertId++;
      }

      // Alerta de tendência de aumento de custos
      if (this.custoTrend > 20 && !dismissedAlerts.includes(alertId)) {
        alerts.push({
          id: alertId++,
          type: 'warning',
          icon: 'trending_up',
          title: 'Tendência de Aumento',
          message: `Os custos aumentaram ${this.custoTrend}% em relação ao período anterior.`,
          action: true,
          actionIcon: 'timeline',
          actionText: 'Ver Tendência'
        });
      }

      return alerts;
    },

    // Novos computed para ações rápidas e estatísticas
    pedidosAcimaOrcamento() {
      return this.pedidosComFinancas.filter(p => this.isOverBudget(p)).length;
    },

    pedidosAltoValor() {
      const valorAlto = this.custoRealTotal / this.pedidosComFinancas.length * 2; // Acima da média * 2
      return this.pedidosComFinancas.filter(p => this.getCustoTotal(p) > valorAlto).length;
    },

    pedidosRecentes() {
      const umaSemanaAtras = new Date();
      umaSemanaAtras.setDate(umaSemanaAtras.getDate() - 7);
      return this.pedidos.filter(p => {
        const dataPedido = new Date(p.created_at || p.data_criacao);
        return dataPedido >= umaSemanaAtras;
      }).length;
    },

    maiorGastoCategoria() {
      if (this.topCategorias.length === 0) {
        return { nome: 'N/A', valor: 0 };
      }
      const maior = this.topCategorias[0];
      return { nome: maior.name, valor: maior.value };
    },

    categoriaMaisPedidos() {
      const categoriaCount = {};
      this.pedidosComFinancas.forEach(pedido => {
        const categoria = pedido.categoria || 'Sem Categoria';
        categoriaCount[categoria] = (categoriaCount[categoria] || 0) + 1;
      });
      
      const maior = Object.entries(categoriaCount)
        .sort(([,a], [,b]) => b - a)[0];
      
      return maior ? { nome: maior[0], count: maior[1] } : { nome: 'N/A', count: 0 };
    },

    mediaMensal() {
      const tresMesesAtras = new Date();
      tresMesesAtras.setMonth(tresMesesAtras.getMonth() - 3);
      
      const pedidosRecentes = this.pedidosComFinancas.filter(p => {
        const dataPedido = new Date(p.created_at || p.data_criacao);
        return dataPedido >= tresMesesAtras;
      });
      
      if (pedidosRecentes.length === 0) return 0;
      
      const totalCusto = pedidosRecentes.reduce((sum, p) => sum + this.getCustoTotal(p), 0);
      return totalCusto / 3; // Dividir por 3 meses
    },

    // Novos computed para os cards adicionais
    pedidosPendentes() {
      return this.pedidos.filter(p => p.status === 'Pendente').length;
    },

    valorPendente() {
      return this.pedidos
        .filter(p => p.status === 'Pendente')
        .reduce((total, p) => total + parseFloat(p.orcamento_previsto || 0), 0);
    },

    mediaPorPedido() {
      if (this.pedidosComFinancas.length === 0) return 0;
      return this.custoRealTotal / this.pedidosComFinancas.length;
    },

    // Computed para cards de resumo executivo
    tempoMedioExecucao() {
      const pedidosConcluidos = this.pedidos.filter(p => p.status === 'Concluído');
      if (pedidosConcluidos.length === 0) return 0;
      
      const tempos = pedidosConcluidos.map(p => {
        const inicio = new Date(p.created_at || p.data_criacao);
        const fim = new Date(p.updated_at || p.data_atualizacao || p.created_at || p.data_criacao);
        return Math.ceil((fim - inicio) / (1000 * 60 * 60 * 24));
      });
      
      return Math.round(tempos.reduce((sum, tempo) => sum + tempo, 0) / tempos.length);
    },

    maiorPedidoValor() {
      if (this.pedidosComFinancas.length === 0) return 0;
      return Math.max(...this.pedidosComFinancas.map(p => this.getCustoTotal(p)));
    },

    maiorPedidoCategoria() {
      if (this.pedidosComFinancas.length === 0) return 'N/A';
      const maiorPedido = this.pedidosComFinancas.reduce((max, p) => 
        this.getCustoTotal(p) > this.getCustoTotal(max) ? p : max
      );
      return maiorPedido.categoria || 'Sem categoria';
    },

    taxaConclusao() {
      if (this.pedidos.length === 0) return 0;
      const concluidos = this.pedidos.filter(p => p.status === 'Concluído').length;
      return Math.round((concluidos / this.pedidos.length) * 100);
    },

    economiaMensal() {
      const umMesAtras = new Date();
      umMesAtras.setMonth(umMesAtras.getMonth() - 1);
      
      const pedidosMes = this.pedidosComFinancas.filter(p => {
        const dataPedido = new Date(p.created_at || p.data_criacao);
        return dataPedido >= umMesAtras;
      });
      
      const orcamentoMes = pedidosMes.reduce((sum, p) => sum + parseFloat(p.orcamento_previsto || 0), 0);
      const custoMes = pedidosMes.reduce((sum, p) => sum + this.getCustoTotal(p), 0);
      
      return Math.max(0, orcamentoMes - custoMes);
    }
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.fetchPedidos();
        this.resetFilters();
        this.calculateSetoresGastos();
      }
    },
    
    searchTerm() {
      this.currentPage = 1;
    },
    
    filterStatus() {
      this.currentPage = 1;
    },

    quickSearchTerm(val) {
      if (val.length > 2) {
        this.generateSearchSuggestions();
      } else {
        this.searchSuggestions = [];
      }
    }
  },
  async mounted() {
    if (this.isOpen) {
      await this.fetchPedidos();
      this.calculateSetoresGastos();
    }
    // Tentar carregar configurações da API primeiro, depois localStorage
    await this.loadBudgetConfigFromAPI();
  },
  methods: {
    setActiveTab(tabId) {
      this.activeTab = tabId;
    },

    async fetchPedidos() {
      this.isLoading = true;
      
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/pedidos`, {
          headers: authService.getAuthHeaders()
        });
        
        this.pedidos = response.data || [];
        this.lastUpdate = new Date().toLocaleTimeString('pt-BR');
        this.calculateSetoresGastos();
      } catch (error) {
        console.error("Erro ao carregar dados financeiros:", error);
      } finally {
        this.isLoading = false;
      }
    },
    
    async refreshData() {
      await this.fetchPedidos();
    },
    
    resetFilters() {
      this.searchTerm = '';
      this.filterStatus = '';
      this.currentPage = 1;
    },

    // Métodos para configuração de orçamentos
    calculateSetoresGastos() {
      // Mapear categorias para setores (usando dados reais do sistema)
      const categoriaParaSetor = {
        'Matérias-primas': 1, // Produção
        'Matérias-Primas': 1, // Produção (variação)
        'Peças de Reposição': 2, // Manutenção
        'Peças de reposição': 2, // Manutenção (variação)
        'Equipamentos e Máquinas': 3, // Equipamentos
        'Equipamentos e máquinas': 3, // Equipamentos (variação)
        'Equipamentos': 3, // Equipamentos (simplificado)
        'Máquinas': 3, // Equipamentos (simplificado)
        'Serviços': 4, // Serviços
        'Serviços terceirizados': 4, // Serviços (variação)
        'Mercadorias diversas': 5, // Diversos
        'Mercadorias Diversas': 5, // Diversos (variação)
        'Diversos': 5, // Diversos (simplificado)
        'Outros': 5, // Diversos (simplificado)
        'Geral': 5 // Diversos (simplificado)
      };

      // Resetar gastos
      this.setores.forEach(setor => {
        setor.gasto_atual = 0;
      });

      // Calcular gastos por setor baseado nos pedidos reais
        this.pedidos.forEach(pedido => {
        const categoria = pedido.categoria || 'Diversos';
        const setorId = categoriaParaSetor[categoria] || 5; // Default para Diversos
        const setor = this.setores.find(s => s.id === setorId);
        if (setor) {
          const custo = this.getCustoTotal(pedido);
          if (custo > 0) {
            setor.gasto_atual += custo;
          }
        }
      });

      // Log para debug
      console.log('Gastos por setor calculados:', this.setores.map(s => ({
        nome: s.nome,
        gasto_atual: s.gasto_atual,
        orcamento: s.orcamento_mensal
      })));
    },

    getDisponibilidadeClass(setor) {
      const disponivel = (setor.orcamento_mensal || 0) - (setor.gasto_atual || 0);
      if (disponivel < 0) return 'negative';
      if (disponivel < (setor.orcamento_mensal || 0) * 0.2) return 'warning';
      return 'positive';
    },

    async saveBudgetConfig() {
      this.isSavingConfig = true;
      
      try {
        // Salvar no backend via API
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/configuracoes/orcamento`, {
          setores: this.setores
        }, {
          headers: authService.getAuthHeaders()
        });
        
        if (response.status === 200 || response.status === 201) {
          // Salvar também no localStorage como backup
          localStorage.setItem('budget_config', JSON.stringify(this.setores));
          
          // Mostrar mensagem de sucesso
          this.$toast?.success?.('Configurações de orçamento salvas com sucesso!') || 
          alert('Configurações de orçamento salvas com sucesso!');
        }
      } catch (error) {
        console.error('Erro ao salvar configurações:', error);
        
        // Se falhar na API, salvar apenas no localStorage
        localStorage.setItem('budget_config', JSON.stringify(this.setores));
        
        this.$toast?.warning?.('Configurações salvas localmente. Erro ao sincronizar com servidor.') ||
        alert('Configurações salvas localmente. Erro ao sincronizar com servidor.');
      } finally {
        this.isSavingConfig = false;
      }
    },

    async loadBudgetConfigFromAPI() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}/configuracoes/orcamento`, {
          headers: authService.getAuthHeaders()
        });
        
        if (response.data && response.data.setores) {
          // Mesclar configurações do servidor com as padrão
          this.setores = this.setores.map(setor => {
            const saved = response.data.setores.find(s => s.id === setor.id);
            return saved ? { ...setor, ...saved } : setor;
          });
          
          // Salvar também no localStorage como backup
          localStorage.setItem('budget_config', JSON.stringify(this.setores));
        }
      } catch (error) {
        console.error('Erro ao carregar configurações do servidor:', error);
        // Fallback para localStorage se API falhar
        this.loadBudgetConfig();
      }
    },
    
    // Métodos de cálculo
    getCustoTotal(pedido) {
      // Priorizar dados de conclusão detalhados
      if (pedido.conclusao_dados) {
        return parseFloat(pedido.conclusao_dados.valor_total_com_mao_de_obra || 
                         pedido.conclusao_dados.valor_total || 0);
      }
      // Fallback para custo_real simples
      return parseFloat(pedido.custo_real || 0);
    },
    
    getDifference(pedido) {
      const orcamento = parseFloat(pedido.orcamento_previsto || 0);
      const custo = this.getCustoTotal(pedido);
      return orcamento - custo;
    },
    
    isOverBudget(pedido) {
      return this.getDifference(pedido) < 0 && parseFloat(pedido.orcamento_previsto || 0) > 0;
    },
    
    // Métodos de formatação
    formatCurrency(value) {
      return parseFloat(value || 0).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },
    
    truncateText(text, maxLength) {
      if (!text) return '';
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    },
    
    // Métodos de classificação visual
    getDiffClass(diff) {
      if (diff > 0) return 'positive';
      if (diff < 0) return 'negative';
      return 'neutral';
    },
    
    getDiffIcon(diff) {
      if (diff > 0) return 'trending_down';
      if (diff < 0) return 'trending_up';
      return 'remove';
    },
    
    getStatusClass(status) {
      switch (status) {
        case 'Concluído': return 'completed';
        case 'Pendente': return 'pending';
        case 'Cancelado': return 'canceled';
        default: return '';
      }
    },
    
    // Métodos de ordenação
    sortBy(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortField = field;
        this.sortDirection = 'desc';
      }
      this.currentPage = 1;
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) return 'unfold_more';
      return this.sortDirection === 'asc' ? 'keyboard_arrow_up' : 'keyboard_arrow_down';
    },
    
    // Métodos de ação
    viewPedido(pedido) {
      this.$emit('view-pedido', pedido);
    },
    
    editPedido(pedido) {
      this.$emit('edit-pedido', pedido);
    },

    loadBudgetConfig() {
      try {
        const storedConfig = localStorage.getItem('budget_config');
        if (storedConfig) {
          const parsedConfig = JSON.parse(storedConfig);
          // Mesclar configurações salvas com as padrão
          this.setores = this.setores.map(setor => {
            const saved = parsedConfig.find(s => s.id === setor.id);
            return saved ? { ...setor, ...saved } : setor;
          });
        }
      } catch (error) {
        console.error('Erro ao carregar configurações de orçamento:', error);
      }
    },

    // Novos métodos para a aba Visão Geral
    getEfficiencyClass() {
      if (this.eficienciaFinanceira >= 90) return 'excellent';
      if (this.eficienciaFinanceira >= 70) return 'good';
      if (this.eficienciaFinanceira >= 50) return 'average';
      return 'poor';
    },

    getEfficiencyLabel() {
      if (this.eficienciaFinanceira >= 90) return 'Excelente';
      if (this.eficienciaFinanceira >= 70) return 'Boa';
      if (this.eficienciaFinanceira >= 50) return 'Regular';
      return 'Baixa';
    },

    // Novos métodos para funcionalidades da visão geral
    getEfficiencyIcon() {
      if (this.eficienciaFinanceira >= 90) return 'star';
      if (this.eficienciaFinanceira >= 70) return 'thumb_up';
      if (this.eficienciaFinanceira >= 50) return 'remove';
      return 'thumb_down';
    },

    // Métodos para ações rápidas
    performQuickSearch() {
      if (!this.quickSearchTerm.trim()) return;
      
      this.searchTerm = this.quickSearchTerm;
      this.filterStatus = '';
      this.quickFilter = '';
      this.setActiveTab('reports');
      this.searchSuggestions = [];
      this.currentPage = 1;
    },

    generateSearchSuggestions() {
      const term = this.quickSearchTerm.toLowerCase();
      const suggestions = [];

      // Sugestões de pedidos
      this.pedidos.forEach(pedido => {
        if (pedido.descricao.toLowerCase().includes(term)) {
          suggestions.push({
            id: `pedido-${pedido.id}`,
            text: `#${pedido.id} - ${pedido.descricao.substring(0, 30)}...`,
            type: 'Pedido',
            icon: 'receipt',
            data: pedido
          });
        }
      });

      // Sugestões de categorias
      const categorias = [...new Set(this.pedidos.map(p => p.categoria).filter(Boolean))];
      categorias.forEach(categoria => {
        if (categoria.toLowerCase().includes(term)) {
          suggestions.push({
            id: `categoria-${categoria}`,
            text: categoria,
            type: 'Categoria',
            icon: 'category',
            data: categoria
          });
        }
      });

      this.searchSuggestions = suggestions.slice(0, 5);
    },

    selectSuggestion(suggestion) {
      if (suggestion.type === 'Pedido') {
        this.viewPedido(suggestion.data);
      } else if (suggestion.type === 'Categoria') {
        this.filterByCategory(suggestion.data);
      }
      this.searchSuggestions = [];
      this.quickSearchTerm = '';
    },

    applyQuickFilter(filterType) {
      // Se o mesmo filtro for clicado, remove o filtro
      if (this.quickFilter === filterType) {
        this.quickFilter = '';
        this.searchTerm = '';
        this.filterStatus = '';
      } else {
        this.quickFilter = filterType;
        this.searchTerm = '';
        this.filterStatus = '';
        
        // Aplicar filtros específicos
        switch (filterType) {
          case 'over-budget':
            // Filtro será aplicado no computed pedidosFiltrados
            break;
          case 'high-value':
            // Filtro será aplicado no computed pedidosFiltrados
            break;
          case 'recent':
            // Filtro será aplicado no computed pedidosFiltrados
            break;
        }
      }
      
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    filterByStatus(status) {
      this.filterStatus = status;
      this.searchTerm = '';
      this.quickFilter = '';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    filterByCategory(categoria) {
      this.searchTerm = categoria;
      this.filterStatus = '';
      this.quickFilter = '';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    // Métodos para setor
    getSectorPercentage(setor) {
      if (!setor.orcamento_mensal || setor.orcamento_mensal === 0) return 0;
      return Math.round((setor.gasto_atual / setor.orcamento_mensal) * 100);
    },

    getSectorProgressClass(setor) {
      const percentage = this.getSectorPercentage(setor);
      if (percentage < 70) return 'good';
      if (percentage < 90) return 'warning';
      return 'danger';
    },

    showSectorDetails(setor) {
      // Filtrar pedidos por setor/categoria
      const categoriaParaSetor = {
        1: ['Matérias-primas', 'Matérias-Primas'],
        2: ['Peças de Reposição', 'Peças de reposição'],
        3: ['Equipamentos e Máquinas', 'Equipamentos e máquinas', 'Equipamentos', 'Máquinas'],
        4: ['Serviços', 'Serviços terceirizados'],
        5: ['Mercadorias diversas', 'Mercadorias Diversas', 'Diversos', 'Outros', 'Geral']
      };
      
      const categorias = categoriaParaSetor[setor.id] || [];
      if (categorias.length > 0) {
        this.searchTerm = categorias[0];
        this.setActiveTab('reports');
      }
    },

    getCategoryCount(categoryName) {
      return this.pedidosComFinancas.filter(p => p.categoria === categoryName).length;
    },

    showAllCategories() {
      this.searchTerm = '';
      this.filterStatus = '';
      this.quickFilter = '';
      this.sortField = 'categoria';
      this.sortDirection = 'asc';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    // Métodos para alertas
    dismissAlert(alertId) {
      // Remover alerta específico da lista
      const alertIndex = this.financialAlerts.findIndex(alert => alert.id === alertId);
      if (alertIndex > -1) {
        // Salvar alertas dispensados no localStorage
        const dismissedAlerts = JSON.parse(localStorage.getItem('dismissed_alerts') || '[]');
        dismissedAlerts.push(alertId);
        localStorage.setItem('dismissed_alerts', JSON.stringify(dismissedAlerts));
      }
    },

    dismissAllAlerts() {
      // Dispensar todos os alertas atuais
      const allAlertIds = this.financialAlerts.map(alert => alert.id);
      const dismissedAlerts = JSON.parse(localStorage.getItem('dismissed_alerts') || '[]');
      const updatedDismissed = [...new Set([...dismissedAlerts, ...allAlertIds])];
      localStorage.setItem('dismissed_alerts', JSON.stringify(updatedDismissed));
    },

    executeAlertAction(alert) {
      // Executar ações específicas baseadas no tipo de alerta
      switch (alert.type) {
        case 'danger':
          this.quickFilter = 'over-budget';
          this.setActiveTab('reports');
          break;
        case 'warning':
          this.showEfficiencyDetails();
          break;
        case 'info':
          this.sortField = 'orcamento_previsto';
          this.sortDirection = 'asc';
          this.setActiveTab('reports');
          break;
      }
    },

    // Métodos para análises detalhadas
    showBudgetAnalysis() {
      // Mostrar análise detalhada do orçamento
      this.searchTerm = '';
      this.filterStatus = '';
      this.quickFilter = '';
      this.sortField = 'orcamento_previsto';
      this.sortDirection = 'desc';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    showEfficiencyDetails() {
      // Mostrar pedidos ordenados por eficiência (diferença orçamento vs custo)
      this.searchTerm = '';
      this.filterStatus = '';
      this.quickFilter = '';
      this.sortField = 'custo_real';
      this.sortDirection = 'desc';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    showCategoryDetails(type) {
      if (type === 'maior-gasto') {
        this.filterByCategory(this.maiorGastoCategoria.nome);
      } else if (type === 'mais-pedidos') {
        this.filterByCategory(this.categoriaMaisPedidos.nome);
      }
    },

    showMonthlyTrend() {
      // Mostrar pedidos dos últimos 3 meses ordenados por data
      this.searchTerm = '';
      this.filterStatus = '';
      this.quickFilter = 'recent';
      this.sortField = 'id';
      this.sortDirection = 'desc';
      this.currentPage = 1;
      this.setActiveTab('reports');
    },

    getEfficiencyLevel() {
      if (this.eficienciaFinanceira >= 90) return 'Excelente';
      if (this.eficienciaFinanceira >= 70) return 'Boa';
      if (this.eficienciaFinanceira >= 50) return 'Regular';
      return 'Baixa';
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Variáveis CSS */
:root {
  --primary-color: #ff6f61;
  --secondary-color: #4db6ac;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --danger-color: #e74c3c;
  --info-color: #3498db;
  --dark-bg: #1f1f1f;
  --card-bg: #2a2a2a;
  --border-color: #333;
  --text-primary: #f5f5f5;
  --text-secondary: #999;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  --border-radius: 12px;
  --border-radius-sm: 6px;
  --border-radius-lg: 16px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* Font Sizes */
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 24px;
  
  /* Z-index */
  --z-index-modal: 1000;
}

/* Modal Base - Similar ao Dashboard */
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

/* Aviso de Desenvolvimento */
.development-warning-banner {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.15), rgba(255, 152, 0, 0.1));
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-left: 4px solid #ffc107;
  padding: 16px 24px;
  margin: 0;
  flex-shrink: 0;
}

.warning-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.warning-icon {
  color: #ffc107;
  font-size: 24px;
  flex-shrink: 0;
}

.warning-text h4 {
  margin: 0 0 8px 0;
  color: #ffc107;
  font-size: 16px;
  font-weight: 600;
}

.warning-text p {
  margin: 0;
  color: #ddd;
  font-size: 14px;
  line-height: 1.4;
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
  font-size: 14px;
  font-weight: 500;
}

.tab-button:hover {
  color: #ff6f61;
  background: rgba(255, 111, 97, 0.1);
}

.tab-button.active {
  color: #ff6f61;
  border-bottom-color: #ff6f61;
  background: rgba(255, 111, 97, 0.1);
}

.tab-badge {
  background: #ff6f61;
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 600;
  min-width: 18px;
  text-align: center;
}

/* Dashboard Content */
.dashboard-content {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dashboard-loading {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 111, 97, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-text {
  font-size: 16px;
  margin: 0;
}

.tabs-container {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.tab-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  padding: 24px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.tab-content.tab-active {
  opacity: 1;
  visibility: visible;
}

/* Métricas Section - Seguindo padrão do Dashboard */
.metrics-section {
  margin-bottom: var(--spacing-lg);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.section-header h3 i {
  color: var(--primary-color);
  font-size: 1.2em;
}

.refresh-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: var(--font-size-sm);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.metric-card {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: var(--primary-color);
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  color: white;
  flex-shrink: 0;
}

.metric-icon.pending {
  background: var(--warning-color);
}

.metric-icon.success {
  background: var(--success-color);
}

.metric-icon.danger {
  background: var(--danger-color);
}

.metric-icon.time {
  background: var(--info-color);
}

.metric-icon i {
  font-size: 24px;
}

.metric-content {
  flex: 1;
  min-width: 0;
}

.metric-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
  margin-bottom: var(--spacing-xs);
}

.metric-subtitle {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  margin: 0;
}

/* Progress Section */
.progress-section {
  margin-bottom: var(--spacing-lg);
}

.budget-progress {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
}

.progress-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
}

.progress-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.progress-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.progress-bar-container {
  position: relative;
}

.progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: var(--transition);
}

.progress-fill.good {
  background: var(--success-color);
}

.progress-fill.warning {
  background: var(--warning-color);
}

.progress-fill.danger {
  background: var(--danger-color);
}

.progress-markers {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.marker {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  position: absolute;
  transform: translateX(-50%);
}

/* Status Section */
.status-section {
  margin-bottom: var(--spacing-lg);
}

.status-overview {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: var(--transition);
}

.status-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.status-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.status-fill {
  height: 100%;
  border-radius: 4px;
  transition: var(--transition);
}

.status-item.completed .status-fill {
  background: var(--success-color);
}

.status-item.pending .status-fill {
  background: var(--warning-color);
}

.status-item.canceled .status-fill {
  background: var(--danger-color);
}

.status-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 200px;
}

.status-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.status-count {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* Categories Section */
.categories-section {
  margin-bottom: var(--spacing-lg);
}

.categories-list {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: var(--transition);
}

.category-item:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(4px);
}

.category-rank {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.category-content {
  flex: 1;
  min-width: 0;
}

.category-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.category-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: var(--spacing-xs);
}

.category-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
  transition: var(--transition);
}

.category-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--primary-color);
  text-align: right;
  flex-shrink: 0;
}

/* Alerts Section */
.alerts-section {
  margin-bottom: var(--spacing-lg);
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.alert-item {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  transition: var(--transition);
}

.alert-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.alert-item.danger {
  border-color: var(--danger-color);
  background: rgba(231, 76, 60, 0.05);
}

.alert-item.warning {
  border-color: var(--warning-color);
  background: rgba(243, 156, 18, 0.05);
}

.alert-item.info {
  border-color: var(--info-color);
  background: rgba(52, 152, 219, 0.05);
}

.alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.alert-item.danger .alert-icon {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.alert-item.warning .alert-icon {
  background: rgba(243, 156, 18, 0.1);
  color: var(--warning-color);
}

.alert-item.info .alert-icon {
  background: rgba(52, 152, 219, 0.1);
  color: var(--info-color);
}

.alert-icon i {
  font-size: 20px;
}

.alert-content {
  flex: 1;
}

.alert-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.alert-message {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: 1.4;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text-secondary);
  background: var(--card-bg);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
}

.empty-state i {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: var(--font-size-sm);
}

/* Novos estilos para a Visão Geral melhorada */

/* Fix para a aba Visão Geral */
.financial-overview {
  background: var(--dark-bg) !important;
  padding: var(--spacing-lg) !important;
  overflow-y: auto !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 0 !important;
}

.financial-overview * {
  box-sizing: border-box;
}

/* Reset de estilos que podem estar interferindo */
.financial-overview .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  width: 100%;
}

.financial-overview .section-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.financial-overview .section-header h3 i {
  color: var(--primary-color);
  font-size: 1.2em;
}

/* Overview Header */
.financial-overview .overview-header {
  background: linear-gradient(135deg, #2a2a2a 0%, rgba(255, 111, 97, 0.05) 100%);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
  border: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-xl);
  width: 100%;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
  min-height: 120px;
}

.financial-overview .overview-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff6f61, #ff8a80);
  opacity: 0.7;
}

@media (max-width: 1024px) {
  .financial-overview .overview-header {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    min-height: auto;
  }
  
  .financial-overview .overview-actions {
    display: flex;
    flex-direction: row;
    gap: var(--spacing-sm);
    justify-content: flex-start;
    flex-wrap: wrap;
  }
  
  .financial-overview .action-btn {
    flex: 1;
    min-width: 130px;
    max-width: 180px;
  }
}

@media (max-width: 480px) {
  .financial-overview .overview-actions {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .financial-overview .action-btn {
    flex: none;
    min-width: auto;
    max-width: none;
    width: 100%;
  }
}

.overview-title h2 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.overview-title h2 i {
  color: var(--primary-color);
  font-size: 32px;
}

.overview-subtitle {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}

.last-update {
  color: var(--primary-color);
  font-weight: 500;
}

.overview-actions {
  display: flex;
  gap: var(--spacing-md);
  flex-shrink: 0;
  align-items: center;
  flex-wrap: nowrap;
}

.action-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: var(--transition);
  text-decoration: none;
  white-space: nowrap;
  min-height: 44px;
  flex-shrink: 0;
  min-width: 140px;
  justify-content: center;
}

.btn-text {
  display: inline-block;
  line-height: 1.2;
}

.action-btn.primary {
  background: var(--primary-color);
  color: white;
}

.action-btn.primary:hover {
  background: #e55b55;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 111, 97, 0.3);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.action-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--primary-color);
  transform: translateY(-1px);
}

/* Main Metrics Container */
.financial-overview .main-metrics-container {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.financial-overview .metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  width: 100%;
  margin-bottom: var(--spacing-lg);
}

.metric-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
  min-height: 120px;
  display: flex;
  flex-direction: column;
}

.metric-card::before {
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

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-card.primary-card {
  border-left: 4px solid var(--primary-color);
}

.metric-card.warning-card {
  border-left: 4px solid var(--warning-color);
}

.metric-card.success-card {
  border-left: 4px solid var(--success-color);
}

.metric-card.danger-card {
  border-left: 4px solid var(--danger-color);
}

.metric-card.info-card {
  border-left: 4px solid var(--info-color);
}

.metric-card.neutral-card {
  border-left: 4px solid #6c757d;
}

.metric-card.secondary-card {
  border-left: 4px solid var(--secondary-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md) 0;
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.card-icon.primary {
  background: linear-gradient(135deg, var(--primary-color), #e55b55);
}

.card-icon.warning {
  background: linear-gradient(135deg, var(--warning-color), #e67e22);
}

.card-icon.success {
  background: linear-gradient(135deg, var(--success-color), #27ae60);
}

.card-icon.danger {
  background: linear-gradient(135deg, var(--danger-color), #c0392b);
}

.card-icon.info {
  background: linear-gradient(135deg, var(--info-color), #2980b9);
}

.card-icon.neutral {
  background: linear-gradient(135deg, #6c757d, #5a6268);
}

.card-icon.secondary {
  background: linear-gradient(135deg, var(--secondary-color), #26a69a);
}

.card-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.mini-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.mini-btn:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
  transform: scale(1.1);
}

.card-content {
  padding: var(--spacing-xs) var(--spacing-md) var(--spacing-md);
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-title {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  line-height: 1;
}

.card-value.primary {
  color: var(--primary-color);
}

.card-value.warning {
  color: var(--warning-color);
}

.card-value.success {
  color: var(--success-color);
}

.card-value.danger {
  color: var(--danger-color);
}

.card-value.info {
  color: var(--info-color);
}

.card-value.neutral {
  color: #6c757d;
}

.card-value.secondary {
  color: var(--secondary-color);
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.detail-item i {
  font-size: 16px;
  opacity: 0.7;
  flex-shrink: 0;
}

.detail-text {
  word-break: break-word;
  line-height: 1.3;
  font-size: var(--font-size-xs);
}

/* Summary Cards Container */
.financial-overview .summary-cards-container {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.financial-overview .summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--spacing-sm);
  width: 100%;
}

.summary-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  transition: all 0.3s ease;
  min-height: 80px;
  position: relative;
  overflow: hidden;
}

.summary-card::before {
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

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.summary-card:hover::before {
  opacity: 1;
}

.summary-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 24px;
}

.time-card .summary-icon {
  background: rgba(52, 152, 219, 0.1);
  color: var(--info-color);
}

.value-card .summary-icon {
  background: rgba(243, 156, 18, 0.1);
  color: var(--warning-color);
}

.completion-card .summary-icon {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

.savings-card .summary-icon {
  background: rgba(155, 89, 182, 0.1);
  color: #9b59b6;
}

.summary-content {
  flex: 1;
  min-width: 0;
}

.summary-content h4 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.summary-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
  line-height: 1.2;
}

.summary-content p {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: 1.3;
}

/* Quick Actions Container */
.financial-overview .quick-actions-container {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.financial-overview .quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  width: 100%;
}

.action-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  overflow: hidden;
  transition: all 0.3s ease;
  min-height: 200px;
  position: relative;
}

.action-card::before {
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

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.action-card:hover::before {
  opacity: 1;
}

.action-header {
  background: rgba(255, 255, 255, 0.02);
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.action-header i {
  color: var(--primary-color);
  font-size: 20px;
}

.action-header h4 {
  margin: 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.action-content {
  padding: var(--spacing-lg);
}

/* Search Card */
.search-container {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.quick-search-input {
  flex: 1;
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  transition: var(--transition);
}

.quick-search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 0.08);
}

.search-btn {
  padding: var(--spacing-sm);
  background: var(--primary-color);
  border: none;
  border-radius: var(--border-radius);
  color: white;
  cursor: pointer;
  transition: var(--transition);
}

.search-btn:hover {
  background: #e55b55;
  transform: scale(1.05);
}

.search-suggestions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition);
}

.suggestion-item:hover {
  background: rgba(255, 111, 97, 0.1);
  transform: translateX(4px);
}

.suggestion-item i {
  color: var(--primary-color);
  font-size: 16px;
}

.suggestion-item span {
  flex: 1;
  font-size: var(--font-size-xs);
  color: var(--text-primary);
}

.suggestion-item small {
  font-size: 10px;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
}

/* Filter Card */
.filter-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  color: var(--text-primary);
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
}

.filter-btn:hover {
  background: rgba(255, 111, 97, 0.1);
  border-color: var(--primary-color);
}

.filter-btn.active {
  background: rgba(255, 111, 97, 0.2);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.filter-btn i {
  margin-right: var(--spacing-xs);
}

.filter-count {
  background: var(--primary-color);
  color: white;
  border-radius: 12px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

/* Stats Card */
.stats-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition);
}

.stat-item:hover {
  background: rgba(255, 111, 97, 0.1);
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 111, 97, 0.1);
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.stat-info small {
  font-size: 11px;
  color: var(--text-secondary);
}

/* Budget Progress Container */
.financial-overview .budget-progress-container {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.financial-overview .budget-sectors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
  width: 100%;
}

.sector-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  padding: var(--spacing-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 140px;
  position: relative;
  overflow: hidden;
}

.sector-card::before {
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

.sector-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.sector-card:hover::before {
  opacity: 1;
}

.sector-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.sector-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 111, 97, 0.1);
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  font-size: 24px;
  flex-shrink: 0;
}

.sector-info {
  flex: 1;
}

.sector-info h4 {
  margin: 0 0 4px 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.sector-info p {
  margin: 0;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: 1.3;
}

.sector-percentage {
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-color);
}

.sector-progress {
  margin-top: var(--spacing-md);
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-xs);
}

.progress-labels .used {
  color: var(--warning-color);
}

.progress-labels .available {
  color: var(--success-color);
}

/* Categories Section */
.financial-overview .categories-section {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.status-card,
.categories-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.status-card::before,
.categories-card::before {
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

.status-card:hover,
.categories-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.status-card:hover::before,
.categories-card:hover::before {
  opacity: 1;
}

.card-header {
  background: rgba(255, 255, 255, 0.02);
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.card-header h3 i {
  color: var(--primary-color);
}

.status-overview {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.status-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition);
}

.status-item:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(4px);
}

.status-visual {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
}

.status-circle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-circle.completed {
  background: var(--success-color);
}

.status-circle.pending {
  background: var(--warning-color);
}

.status-circle.canceled {
  background: var(--danger-color);
}

.status-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.status-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.status-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.status-count {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

/* Categories List */
.categories-list {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: var(--transition);
}

.category-item:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(4px);
}

.category-rank {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.category-content {
  flex: 1;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.category-name {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

.category-value {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--primary-color);
}

.category-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: var(--spacing-xs);
}

.category-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  border-radius: 2px;
  transition: var(--transition);
}

.category-details {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

/* Alerts Container */
.financial-overview .alerts-container {
  margin-bottom: var(--spacing-xl);
  width: 100%;
}

.financial-overview .alerts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  width: 100%;
}

.alert-card {
  background: linear-gradient(135deg, #2a2a2a 0%, #252525 100%);
  border-radius: var(--border-radius);
  border: 1px solid #333;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.alert-card::before {
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

.alert-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #444;
}

.alert-card:hover::before {
  opacity: 1;
}

.alert-card.danger {
  border-left: 4px solid var(--danger-color);
  background: rgba(231, 76, 60, 0.03);
}

.alert-card.warning {
  border-left: 4px solid var(--warning-color);
  background: rgba(243, 156, 18, 0.03);
}

.alert-card.info {
  border-left: 4px solid var(--info-color);
  background: rgba(52, 152, 219, 0.03);
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border-color);
}

.alert-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.alert-card.danger .alert-icon {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.alert-card.warning .alert-icon {
  background: rgba(243, 156, 18, 0.1);
  color: var(--warning-color);
}

.alert-card.info .alert-icon {
  background: rgba(52, 152, 219, 0.1);
  color: var(--info-color);
}

.alert-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.alert-content {
  padding: var(--spacing-lg);
}

.alert-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--text-primary);
}

.alert-message {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  line-height: 1.4;
}

.alert-footer {
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.alert-action-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius);
  font-size: var(--font-size-xs);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: var(--transition);
}

.alert-action-btn:hover {
  background: #e55b55;
  transform: translateY(-1px);
}



/* Progress Section (mantido para compatibilidade) */
.budget-progress-section {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 24px;
  border: 1px solid var(--border-color);
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h3 i {
  color: var(--primary-color);
}

.progress-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.stat-separator {
  color: var(--border-color);
}

.progress-container {
  position: relative;
}

.progress-bar-modern {
  height: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  margin-bottom: 16px;
}

.progress-fill {
  height: 100%;
  border-radius: 6px;
  position: relative;
  transition: var(--transition);
}

.progress-fill.good {
  background: linear-gradient(90deg, var(--success-color), #27ae60);
}

.progress-fill.warning {
  background: linear-gradient(90deg, var(--warning-color), #e67e22);
}

.progress-fill.danger {
  background: linear-gradient(90deg, var(--danger-color), #c0392b);
}

.progress-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: progressGlow 2s ease-in-out infinite;
}

@keyframes progressGlow {
  0%, 100% { transform: translateX(-100%); }
  50% { transform: translateX(100%); }
}

.progress-markers {
  position: absolute;
  top: -8px;
  left: 0;
  right: 0;
  height: 28px;
  pointer-events: none;
}

.marker {
  position: absolute;
  top: 0;
  transform: translateX(-50%);
  font-size: 10px;
  color: var(--text-secondary);
  text-align: center;
}

.marker::before {
  content: '';
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 8px;
  background: var(--border-color);
}

.marker.critical {
  color: var(--danger-color);
  font-weight: 600;
}

.progress-legend {
  display: flex;
  gap: 24px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-item.good .legend-color {
  background: var(--success-color);
}

.legend-item.warning .legend-color {
  background: var(--warning-color);
}

.legend-item.danger .legend-color {
  background: var(--danger-color);
}

/* Budget Config Section */
.budget-config-section {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 24px;
  border: 1px solid var(--border-color);
}

.btn-save-config {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition);
}

.btn-save-config:hover:not(:disabled) {
  background: #e55b55;
  transform: translateY(-1px);
}

.btn-save-config:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.budget-config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.budget-config-card {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  padding: 20px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.budget-config-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.config-card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.setor-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 111, 97, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.setor-icon i {
  color: var(--primary-color);
  font-size: 24px;
}

.setor-info h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  color: var(--text-primary);
  font-weight: 600;
}

.setor-info p {
  margin: 0;
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.config-card-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 12px;
  color: var(--text-secondary);
  font-weight: 500;
}

.budget-input {
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 14px;
  transition: var(--transition);
}

.budget-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 0.08);
}

.config-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-value {
  font-size: 12px;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.stat-value.positive {
  color: var(--success-color);
}

.stat-value.warning {
  color: var(--warning-color);
}

.stat-value.negative {
  color: var(--danger-color);
}

/* Table Section */
.financial-table-section {
  background: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 24px;
  border: 1px solid var(--border-color);
}

.table-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 200px;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-size: 18px;
}

.search-input {
  width: 100%;
  padding: 12px 12px 12px 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  transition: var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 0.08);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.filter-select {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition);
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.filter-select option {
  background: var(--card-bg);
  color: var(--text-primary);
}

/* Table */
.table-container {
  overflow-x: auto;
  margin: 24px 0;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.financial-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--dark-bg);
}

.financial-table th {
  background: rgba(255, 255, 255, 0.02);
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 10;
}

.financial-table th.sortable {
  cursor: pointer;
  user-select: none;
  transition: var(--transition);
}

.financial-table th.sortable:hover {
  background: rgba(255, 111, 97, 0.1);
  color: var(--primary-color);
}

.sort-icon {
  font-size: 16px;
  margin-left: 4px;
  opacity: 0.6;
}

.financial-table td {
  padding: 16px 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  font-size: 14px;
}

.table-row {
  transition: var(--transition);
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.02);
}

.table-row.over-budget {
  background: rgba(231, 76, 60, 0.05);
  border-left: 3px solid var(--danger-color);
}

.empty-row {
  background: transparent;
}

.empty-cell {
  text-align: center;
  padding: 60px 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--text-secondary);
}

.empty-state i {
  font-size: 48px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}

/* Table Cells */
.pedido-id {
  font-weight: 600;
  color: var(--primary-color);
}

.description-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.description-text {
  line-height: 1.4;
}

.description-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.meta-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: rgba(255, 111, 97, 0.1);
  border-radius: 4px;
  font-size: 10px;
  color: var(--primary-color);
}

.meta-tag i {
  font-size: 12px;
}

.category-badge {
  padding: 4px 8px;
  background: rgba(77, 182, 172, 0.1);
  color: var(--secondary-color);
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.currency-value {
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.cost-breakdown {
  margin-top: 4px;
  font-size: 10px;
  color: var(--text-secondary);
  line-height: 1.3;
}

.difference-value {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
}

.difference-value.positive {
  color: var(--success-color);
}

.difference-value.negative {
  color: var(--danger-color);
}

.difference-value.neutral {
  color: var(--text-secondary);
}

.diff-icon {
  font-size: 16px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.completed {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
}

.status-badge.pending {
  background: rgba(243, 156, 18, 0.1);
  color: var(--warning-color);
}

.status-badge.canceled {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.view:hover {
  background: var(--info-color);
  border-color: var(--info-color);
  color: white;
}

.action-btn.edit:hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.action-btn i {
  font-size: 16px;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
  padding: 16px 0;
}

.pagination-btn {
  width: 36px;
  height: 36px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.pagination-btn:not(:disabled):hover {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--text-primary);
}

.pagination-total {
  font-size: 12px;
  color: var(--text-secondary);
}

/* Responsividade */
@media (max-width: 1200px) {
  .financial-overview .metrics-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--spacing-sm);
  }
  
  .financial-overview .quick-actions-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  
  .financial-overview .budget-sectors-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
  
  .budget-config-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  }
}

@media (max-width: 992px) {
  .financial-overview .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  /* Status categories container removido */
  
  .financial-overview .quick-actions-grid {
    grid-template-columns: 1fr;
  }
  
  .financial-overview .summary-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
}

@media (max-width: 576px) {
  .financial-overview .metrics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  
  .financial-overview .summary-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  
  .financial-overview .budget-sectors-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  
  .financial-overview .alerts-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
}

@media (max-width: 768px) {
  .modal-overlay {
    padding: 8px;
  }
  
  .modal-content {
    margin: 0;
    max-height: 100vh;
    height: 100vh;
    border-radius: 0;
  }
  
  .modal-header {
    padding: 16px;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .header-actions {
    align-self: stretch;
    justify-content: space-between;
  }
  
  .tab-content {
    padding: 16px;
  }
  
  /* Overview Header Responsivo - Removido (duplicado) */
  
  /* Metrics Grid Responsivo */
  .financial-overview .metrics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }
  
  .financial-overview .metric-card {
    margin-bottom: var(--spacing-sm);
    min-height: 110px;
  }
  
  .financial-overview .card-header {
    padding: var(--spacing-sm) var(--spacing-md) 0;
  }
  
  .financial-overview .card-content {
    padding: var(--spacing-sm) var(--spacing-md) var(--spacing-md);
  }
  
  .financial-overview .card-value {
    font-size: 20px;
  }
  
  .financial-overview .card-title {
    font-size: 11px;
  }
  
  .financial-overview .detail-text {
    font-size: 10px;
  }
  
  /* Summary Cards Responsivo */
  .financial-overview .summary-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }
  
  .financial-overview .summary-card {
    min-height: 80px;
    padding: var(--spacing-md);
  }
  
  .financial-overview .summary-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .financial-overview .summary-value {
    font-size: 16px;
  }
  
  .financial-overview .summary-content h4 {
    font-size: var(--font-size-xs);
  }
  
  .financial-overview .summary-content p {
    font-size: 10px;
  }

  /* Quick Actions Responsivo */
  .financial-overview .quick-actions-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .financial-overview .action-card {
    margin-bottom: var(--spacing-sm);
  }
  
  .financial-overview .filter-buttons {
    gap: var(--spacing-xs);
  }
  
  .financial-overview .filter-btn {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-xs);
  }
  
  /* Budget Sectors Responsivo */
  .financial-overview .budget-sectors-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .sector-card {
    padding: var(--spacing-md);
  }
  
  .sector-header {
    gap: var(--spacing-sm);
  }
  
  .sector-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .sector-percentage {
    font-size: 16px;
  }
  
  /* Status Categories Responsivo */
  .financial-overview .status-categories-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .financial-overview .status-overview,
  .financial-overview .categories-list {
    padding: var(--spacing-md);
  }
  
  .financial-overview .status-item,
  .financial-overview .category-item {
    padding: var(--spacing-xs);
  }
  
  .financial-overview .status-info {
    min-width: auto;
    flex-direction: column;
    align-items: flex-end;
    gap: 2px;
  }
  
  .financial-overview .category-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }
  
  /* Alerts Responsivo */
  .financial-overview .alerts-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .financial-overview .alert-header {
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .financial-overview .alert-content {
    padding: var(--spacing-md);
  }
  
  /* Outros elementos responsivos */
  .budget-config-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-info {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  
  .table-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .progress-legend {
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .modal-overlay {
    padding: 5px;
  }
  
  .financial-overview {
    padding: var(--spacing-sm) !important;
  }
  
  .financial-overview .overview-header {
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    min-height: auto;
  }
  
  .financial-overview .overview-title h2 {
    font-size: 18px;
  }
  
  .financial-overview .metrics-grid {
    gap: var(--spacing-xs);
  }
  
  .financial-overview .metric-card {
    min-height: 100px;
  }
  
  .financial-overview .card-value {
    font-size: 18px;
  }
  
  .financial-overview .card-title {
    font-size: 10px;
  }
  
  .financial-overview .detail-text {
    font-size: 9px;
  }
  
  .financial-overview .card-icon {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }
  
  .financial-overview .mini-btn {
    width: 28px;
    height: 28px;
  }
  
  .financial-overview .action-card {
    min-height: 160px;
  }
  
  .financial-overview .summary-card {
    min-height: 70px;
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
  }
  
  .financial-overview .summary-icon {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }
  
  .financial-overview .summary-value {
    font-size: 14px;
  }
  
  .financial-overview .summary-content h4 {
    font-size: 10px;
  }
  
  .financial-overview .summary-content p {
    font-size: 9px;
  }
  
  .financial-overview .sector-card {
    min-height: 120px;
    padding: var(--spacing-md);
  }
  
  /* Regras movidas para breakpoint específico */
  
  .financial-table th,
  .financial-table td {
    padding: 12px 8px;
    font-size: 12px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
}

/* Scrollbar personalizada */
.tab-content::-webkit-scrollbar {
  width: 8px;
}

.tab-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.tab-content::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

.tab-content::-webkit-scrollbar-thumb:hover {
  background: #e55b55;
}

.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}
</style> 