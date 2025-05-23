<template>
  <div v-if="isOpen && pedido" class="modal-overlay" @click="closeModal">
    <!-- Banner de depuração removido conforme solicitado -->
    
    <div class="print-modal" @click.stop ref="orderContent">
      <!-- Header com o logo -->
      <div class="modal-header">
        <img src="@/assets/logo.png" alt="LOGO" class="logo" />
        <h2>DETALHES DO PEDIDO</h2>

        <!-- ID do Pedido -->
        <div class="order-id">
          <p><strong>PEDIDO Nº:</strong> {{pedido.id }}</p>
        </div>
      </div>
      
      <!-- Grid para Detalhes do Pedido -->
      <div class="order-details-grid">
        <div class="detail-item">
          <strong>DESCRIÇÃO:</strong>
          <span>{{ (pedido.descricao || 'Não informado').toUpperCase() }}</span>
        </div>
        
        <div class="detail-item">
          <strong>QUANTIDADE:</strong>
          <span>{{ pedido.quantidade || 0 }}</span>
        </div>
        
        <div class="detail-item">
          <strong>URGÊNCIA:</strong> 
          <div class="badge-container">
            <span class="urgency-badge" :class="urgencyClass">
              {{ (pedido.urgencia || 'Normal').toUpperCase() }}
            </span>
          </div>
        </div>
        
        <div class="detail-item">
          <strong>CATEGORIA:</strong>
          <span>{{ (pedido.categoria || 'Não categorizado').toUpperCase() }}</span>
        </div>
        
        <div class="detail-item">
          <strong>DATA DO PEDIDO:</strong>
          <span>{{ formatDate(pedido.deliveryDate || new Date()).toUpperCase() }}</span>
        </div>
        
        <div v-if="pedido.status === 'Concluído'" class="detail-item">
          <strong>DATA DE CONCLUSÃO:</strong>
          <span>{{ formatDate(pedido.conclusao_data || new Date()).toUpperCase() }}</span>
        </div>
        
        <div class="detail-item full-width">
          <strong>OBSERVAÇÃO:</strong>
          <span>{{ pedido.observacao ? pedido.observacao.toUpperCase() : "NENHUMA" }}</span>
        </div>
        
        <div class="detail-item">
          <strong>RESPONS. PELA COMPRA:</strong>
          <span>{{ (pedido.sender || 'Não informado').toUpperCase() }}</span>
        </div>
        
        <div v-if="pedido.status" class="detail-item">
          <strong>STATUS:</strong>
          <span class="status-badge" :class="statusClass">
            {{ pedido.status.toUpperCase() }}
          </span>
        </div>
        
        <div class="detail-item">
          <strong>CRIADO POR:</strong>
          <span>{{ (pedido.usuario_nome || getCurrentUser() || 'Não informado').toUpperCase() }}</span>
        </div>

        <!-- Setor -->
        <div class="detail-item" v-if="pedido.setor">
          <strong>SETOR:</strong>
          <span>{{ pedido.setor.toUpperCase() }}</span>
        </div>

        <!-- Tempo de Processamento (se estiver concluído) -->
        <div class="detail-item" v-if="pedido.status === 'Concluído' && pedido.conclusao_data && pedido.deliveryDate">
          <strong>TEMPO DE PROCESSAMENTO:</strong>
          <span>{{ calculateProcessingTime() }}</span>
        </div>
      </div>
        
      <!-- Anexo (se houver) -->
      <div v-if="pedido.anexo" class="attachment-section">
        <strong>ANEXO:</strong>
        <img :src="'data:image/png;base64,' + pedido.anexo" alt="ANEXO" class="order-attachment" />
      </div>

      <!-- Informações de Auditoria -->
      <div v-if="showAuditInfo && pedido.audit_info" class="audit-section">
        <div class="audit-header" @click="toggleAuditInfo">
          <strong>INFORMAÇÕES DE AUDITORIA</strong>
          <i class="fas" :class="auditInfoExpanded ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
        </div>
        <div v-if="auditInfoExpanded" class="audit-details">
          <div class="audit-item" v-if="pedido.audit_info.created_at_exact">
            <strong>Data e Hora Exata:</strong>
            <span>{{ formatExactDateTime(pedido.audit_info.created_at_exact) }}</span>
          </div>
          <div class="audit-item" v-if="pedido.audit_info.browser_info">
            <strong>Dispositivo:</strong>
            <span>{{ getBrowserInfo() }}</span>
          </div>
          <div class="audit-item" v-if="pedido.audit_info.user_email">
            <strong>Email do Usuário:</strong>
            <span>{{ pedido.audit_info.user_email }}</span>
          </div>
          <div class="audit-item" v-if="pedido.audit_info.user_type">
            <strong>Tipo de Usuário:</strong>
            <span>{{ getUserType(pedido.audit_info.user_type) }}</span>
          </div>
        </div>
      </div>

      <!-- Botões -->
      <div class="action-buttons">
        <button @click="generateImage" class="print-btn" :disabled="isGeneratingImage">
          <i class="fas fa-image"></i> GERAR IMAGEM
        </button>
        <!-- Mostrar o botão de novo pedido apenas se for do contexto de criação -->
        <button v-if="origin === 'creation'" class="primary-btn" @click="createNewOrder">
          <i class="fas fa-plus"></i> NOVO PEDIDO
        </button>
        <button class="close-btn" @click="closeModal">
          <i class="fas fa-times"></i> FECHAR
        </button>
      </div>
    </div>
    
    <!-- Indicador de loading durante a geração da imagem -->
    <loading-indicator 
      v-if="isGeneratingImage" 
      overlay 
      size="large" 
      message="Gerando imagem do pedido..." 
    />
  </div>
</template>

<script>
import html2canvas from "html2canvas";
import { useToast } from 'vue-toastification';
import LoadingIndicator from '@/components/ui/LoadingIndicator.vue';

export default {
  name: 'ModalImprimirPedido',
  components: {
    LoadingIndicator
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    pedido: {
      type: Object,
      default: () => ({})
    },
    origin: {
      type: String,
      default: 'creation' // 'creation' ou 'consultation'
    }
  },
  data() {
    return {
      modalId: `print-modal-${Date.now()}`, // ID único para o modal
      isGeneratingImage: false,
      showAuditInfo: true, // Controla se as informações de auditoria devem ser exibidas
      auditInfoExpanded: false, // Controla se as informações de auditoria estão expandidas
      currentUser: null // Armazenará os dados do usuário atual
    };
  },
  computed: {
    // Determinar a classe da badge com base na urgência
    urgencyClass() {
      const urgency = (this.pedido.urgencia || '').toLowerCase();
      if (urgency === 'urgente') return 'urgent';
      if (urgency === 'crítico' || urgency === 'critico') return 'critical';
      return 'normal';
    },
    // Determinar a classe do status
    statusClass() {
      const status = (this.pedido.status || '').toLowerCase();
      if (status === 'concluído' || status === 'concluido') return 'status-completed';
      if (status === 'cancelado') return 'status-canceled';
      return 'status-pending';
    },
    // Detectar se é um dispositivo móvel
    isMobile() {
      return window.innerWidth <= 600;
    },
    // Detectar a orientação do dispositivo
    isPortrait() {
      return window.innerHeight > window.innerWidth;
    }
  },
  created() {
    console.log('[INFO] ModalImprimirPedido criado', {
      isOpen: this.isOpen,
      pedidoId: this.pedido?.id,
      modalId: this.modalId,
      origin: this.origin
    });
    
    // Adicionar log detalhado do pedido recebido
    console.log('[DEBUG] Pedido completo recebido:', this.pedido);
    console.log('[DEBUG] Campo sender do pedido:', this.pedido?.sender);
    
    // Carregar dados do usuário atual do localStorage
    this.loadCurrentUser();
  },
  mounted() {
    if (this.isOpen) {
      // Impedir rolagem quando o modal está aberto
      document.body.style.overflow = 'hidden';
      
      // Verificar se o botão de novo pedido deve ser exibido
      console.log('[INFO] Modal aberto com origin:', this.origin);
    }
  },
  beforeUnmount() {
    // Restaurar a rolagem quando o componente for desmontado
    document.body.style.overflow = '';
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        // Impedir rolagem quando o modal está aberto
        document.body.style.overflow = 'hidden';
      } else {
        // Restaurar rolagem quando o modal é fechado
        document.body.style.overflow = '';
      }
    }
  },
  methods: {
    loadCurrentUser() {
      try {
        const userStr = localStorage.getItem("user");
        if (userStr) {
          this.currentUser = JSON.parse(userStr);
          console.log('[INFO] Usuário atual carregado:', this.currentUser.nome);
        } else {
          this.currentUser = {
            nome: localStorage.getItem("user_name") || "Usuário do Sistema"
          };
        }
      } catch (e) {
        console.error("Erro ao carregar dados do usuário:", e);
        this.currentUser = { nome: "Usuário do Sistema" };
      }
    },
    getCurrentUser() {
      if (this.currentUser && this.currentUser.nome) {
        return this.currentUser.nome;
      }
      
      // Tentar obter o nome do usuário do localStorage se não estiver carregado
      const userStr = localStorage.getItem("user");
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          return user.nome;
        } catch (e) {
          console.error("Erro ao parsear dados do usuário:", e);
        }
      }
      
      // Fallback para outros campos caso precise
      return localStorage.getItem("user_name") || "Usuário do Sistema";
    },
    closeModal() {
      // Restaurar a rolagem
      document.body.style.overflow = '';
      // Emitir evento de fechamento
      this.$emit("close");
    },
    createNewOrder() {
      this.closeModal();
      this.$emit("new-order");
    },
    formatDate(date) {
      if (!date) return 'Data não informada';
      
      try {
        const d = new Date(date);
        
        // Verificar se a data é válida
        if (isNaN(d.getTime())) {
          console.warn(`Data inválida: ${date}`);
          return 'Data inválida';
        }
        
        return d.toLocaleDateString("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
        });
      } catch (error) {
        console.error(`Erro ao formatar data: ${date}`, error);
        return 'Erro de formato';
      }
    },
    formatExactDateTime(dateTimeStr) {
      if (!dateTimeStr) return 'Não disponível';
      
      try {
        const d = new Date(dateTimeStr);
        
        // Verificar se a data é válida
        if (isNaN(d.getTime())) {
          return 'Data/hora inválida';
        }
        
        return d.toLocaleDateString("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit"
        });
      } catch (error) {
        return 'Erro de formato';
      }
    },
    calculateProcessingTime() {
      if (!this.pedido.conclusao_data || !this.pedido.deliveryDate) return 'N/A';
      
      try {
        const startDate = new Date(this.pedido.deliveryDate);
        const endDate = new Date(this.pedido.conclusao_data);
        
        if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
          return 'N/A';
        }
        
        const diffTime = Math.abs(endDate - startDate);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
          return 'Mesmo dia';
        } else if (diffDays === 1) {
          return '1 dia';
        } else {
          return `${diffDays} dias`;
        }
      } catch (error) {
        return 'N/A';
      }
    },
    getBrowserInfo() {
      if (!this.pedido.audit_info || !this.pedido.audit_info.browser_info) return 'Não disponível';
      
      const info = this.pedido.audit_info.browser_info;
      // Criar uma string simplificada com as informações mais relevantes
      return `${info.platform} - ${window.innerWidth}x${window.innerHeight}`;
    },
    getUserType(type) {
      const types = {
        'admin': 'Administrador',
        'gestor': 'Gestor',
        'usuario': 'Usuário Padrão'
      };
      
      return types[type] || type;
    },
    toggleAuditInfo() {
      this.auditInfoExpanded = !this.auditInfoExpanded;
    },
    async generateImage() {
      if (this.isGeneratingImage) return;
      this.isGeneratingImage = true;
        
      // Inicializar o toast
      const toast = useToast();
      toast.info("Preparando para gerar a imagem do pedido...");

      try {
        // Obter o elemento que contém o conteúdo do pedido
        const orderElement = this.$refs.orderContent;
        
        if (!orderElement) {
          toast.error("Erro: Elemento do pedido não encontrado.");
          this.isGeneratingImage = false;
          return;
        }

        // Usar as propriedades computadas para detectar dispositivo móvel e orientação
        const isMobile = this.isMobile;
        const isPortrait = this.isPortrait;
        
        // Criando um clone do elemento para ser usado na captura
        // Isso evita modificar o elemento original e possíveis efeitos colaterais
        const cloneDiv = orderElement.cloneNode(true);
        document.body.appendChild(cloneDiv);
        
        // Configurando o clone para captura
        cloneDiv.style.position = 'absolute';
        cloneDiv.style.top = '-9999px';
        cloneDiv.style.left = '-9999px';
        cloneDiv.style.width = isMobile ? '100%' : `${orderElement.offsetWidth}px`;
        cloneDiv.style.maxHeight = 'none';
        cloneDiv.style.height = 'auto';
        cloneDiv.style.overflowY = 'visible';
        cloneDiv.style.background = '#1c1c1c';
        cloneDiv.style.zIndex = '-1';
        cloneDiv.style.transform = 'none';
        cloneDiv.style.transition = 'none';
        cloneDiv.style.padding = '30px';
        cloneDiv.style.margin = '0';
        cloneDiv.style.boxSizing = 'border-box';
        cloneDiv.style.display = 'flex';
        cloneDiv.style.flexDirection = 'column';
        cloneDiv.style.gap = '24px';
        
        // Adicionar uma classe especial para captura
        cloneDiv.setAttribute('data-capture-clone', 'true');
        
        // Configurações específicas para dispositivos móveis
        if (isMobile) {
          // Mantendo as configurações originais para Mobile
          cloneDiv.style.width = '540px'; // Largura fixa para evitar distorção
          cloneDiv.style.fontSize = '14px'; // Reduzir tamanho da fonte
          
          // Ajustar layout com base na orientação
          const cloneGrid = cloneDiv.querySelector('.order-details-grid');
          if (cloneGrid) {
            cloneGrid.style.display = 'grid';
            cloneGrid.style.gridTemplateColumns = '1fr'; // Sempre uma coluna em mobile
            cloneGrid.style.gap = '12px';
          }
          
          // Ajustar tamanho de elementos específicos
          const detailItems = cloneDiv.querySelectorAll('.detail-item');
          detailItems.forEach(item => {
            item.style.padding = '10px';
            item.style.margin = '0';
          });
          
          // Ajustar cabeçalho para ocupar menos espaço vertical
          const modalHeader = cloneDiv.querySelector('.modal-header');
          if (modalHeader) {
            modalHeader.style.marginBottom = '8px';
          }
          
          // Ajustar logo com base na orientação
          const logo = cloneDiv.querySelector('.logo');
          if (logo) {
            logo.style.width = isPortrait ? '100px' : '120px';
            logo.style.marginBottom = '10px';
          }
          
          // Ajustar título
          const title = cloneDiv.querySelector('.modal-header h2');
          if (title) {
            title.style.fontSize = isPortrait ? '1.1rem' : '1.2rem';
            title.style.marginBottom = '10px';
          }
          
          // Ajustar ID do pedido
          const orderId = cloneDiv.querySelector('.order-id p');
          if (orderId) {
            orderId.style.fontSize = isPortrait ? '0.9rem' : '1rem';
          }
          
          // Garantir que a imagem final tenha tamanho adequado para visualização no dispositivo
          cloneDiv.setAttribute('data-orientation', isPortrait ? 'portrait' : 'landscape');
        } else {
          // Configurações específicas para desktop para evitar cortes e espaço excessivo
          cloneDiv.style.width = `${orderElement.offsetWidth}px`;
          
          // Aumentar o tamanho da logo no desktop
          const logo = cloneDiv.querySelector('.logo');
          if (logo) {
            logo.style.width = '200px'; // Logo maior
            logo.style.marginBottom = '12px';
          }
          
          // Reduzir espaçamentos no clone para versão desktop
          cloneDiv.style.gap = '16px'; // Menor espaçamento entre seções
          
          // Reduzir o padding inferior
          cloneDiv.style.paddingBottom = '30px'; // Reduzido de 60px para 30px
          
          // Reduzir espaçamento do grid
          const grid = cloneDiv.querySelector('.order-details-grid');
          if (grid) {
            grid.style.gap = '12px'; // Reduzir espaço entre itens
            grid.style.padding = '16px'; // Reduzir padding interno
            grid.style.marginBottom = '10px'; // Reduzir margem inferior
          }
          
          // Ajustar cabeçalho para ser mais compacto
          const modalHeader = cloneDiv.querySelector('.modal-header');
          if (modalHeader) {
            modalHeader.style.marginBottom = '10px';
          }
          
          // Reorganizar o grid para layout mais compacto
          this.reorganizeGridForImageCapture(cloneDiv);
        }
        
        // Garantir que elementos fixos sejam renderizados corretamente
        const fixElements = (container) => {
          // Processar elementos diretamente
          for (let i = 0; i < container.children.length; i++) {
            const child = container.children[i];
            // Remover efeitos de hover, transições e transformações
            if (child.style) {
              child.style.transition = 'none';
              child.style.transform = 'none';
              child.style.boxShadow = 'none';
              
              // Garantir que conteúdo seja visível
              if (child.classList.contains('detail-item') || 
                  child.classList.contains('order-details-grid') ||
                  child.classList.contains('attachment-section')) {
                child.style.opacity = '1';
                child.style.visibility = 'visible';
                child.style.overflow = 'visible';
                child.style.display = child.classList.contains('order-details-grid') ? 'grid' : 'flex';
                
                if (!isMobile && child.classList.contains('detail-item')) {
                  child.style.padding = '12px'; // Reduzir padding dos itens no desktop
                  child.style.marginBottom = '0';
                }
              }
            }
            
            // Processar filhos recursivamente
            if (child.children && child.children.length > 0) {
              fixElements(child);
            }
          }
        };
        
        // Aplicar processamento recursivo
        fixElements(cloneDiv);
        
        // Ocultar botões e seções desnecessárias no clone
        const cloneButtons = cloneDiv.querySelectorAll('button');
        cloneButtons.forEach(btn => {
          btn.style.display = 'none';
        });
        
        const cloneAuditSection = cloneDiv.querySelector('.audit-section');
        if (cloneAuditSection) {
          cloneAuditSection.style.display = 'none';
        }
        
        // Garantir layout específico do grid
        const cloneGrid = cloneDiv.querySelector('.order-details-grid');
        if (cloneGrid) {
          cloneGrid.style.display = 'grid';
          cloneGrid.style.gridTemplateColumns = isMobile ? '1fr' : '1fr 1fr';
          cloneGrid.style.gap = isMobile ? '12px' : '16px';
        }
        
        // Dar tempo para o DOM renderizar o clone completamente
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Adicionar um elemento de espaçamento extra no final
        if (!isMobile) {
          const spacer = document.createElement('div');
          spacer.style.height = '50px';
          spacer.style.width = '100%';
          cloneDiv.appendChild(spacer);
        }
        
        // Forçar recálculo de layout
        void cloneDiv.offsetHeight;
        
        console.log('[DEBUG] Dimensões do clone para captura:', {
          isMobile,
          scrollHeight: cloneDiv.scrollHeight,
          offsetHeight: cloneDiv.offsetHeight,
          clientHeight: cloneDiv.clientHeight,
          width: cloneDiv.offsetWidth
        });
        
        try {
          // Certificar que a altura do clone foi calculada corretamente
          const fullHeight = cloneDiv.scrollHeight || cloneDiv.offsetHeight;
          console.log('[DEBUG] Altura final para captura:', fullHeight);
          
          // Usar html2canvas com configurações otimizadas
          const canvas = await html2canvas(cloneDiv, {
            useCORS: true,
            allowTaint: true,
            backgroundColor: "#1c1c1c",
            scale: isMobile ? 1.5 : 2, // Reduzir escala para dispositivos móveis
            height: isMobile ? (fullHeight + 100) : fullHeight, // Remover margem extra para desktop
            width: cloneDiv.offsetWidth,
            windowHeight: isMobile ? (fullHeight + 100) : fullHeight, // Sem margem extra para desktop
            windowWidth: cloneDiv.offsetWidth,
            scrollY: 0,
            scrollX: 0,
            logging: false, 
            removeContainer: false,
            foreignObjectRendering: false // Desativar para evitar problemas em alguns navegadores
          });

          // Converter para PNG e baixar
          const imgData = canvas.toDataURL('image/png');
          const link = document.createElement('a');
          link.href = imgData;
          link.download = `pedido_${this.pedido.id || 'novo'}.png`; 
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
      
          toast.success("Imagem gerada com sucesso!");
        } catch (error) {
          console.error("Primeiro método falhou, tentando método alternativo:", error);
          // Tentativa com método de fallback
          await this.generateImageFallback(orderElement);
        } finally {
          // Remover o clone do DOM quando terminar
          if (cloneDiv && cloneDiv.parentNode) {
            cloneDiv.parentNode.removeChild(cloneDiv);
          }
        }
      } catch (error) {
        console.error("Erro ao processar captura:", error);
        toast.error("Erro ao processar captura: " + (error.message || "Erro desconhecido"));
      } finally {
        this.isGeneratingImage = false;
      }
    },
    
    // Método de fallback para captura de imagem
    async generateImageFallback(orderElement) {
      const toast = useToast();
      
      try {
        console.log('[DEBUG] Utilizando método de fallback para captura');
        
        // Usar as propriedades computadas para detectar dispositivo móvel e orientação
        const isMobile = this.isMobile;
        const isPortrait = this.isPortrait;
        
        // 1. Salvar as configurações originais
        const originalOverflow = document.body.style.overflow;
        const originalOverflowY = orderElement.style.overflowY;
        const originalHeight = orderElement.style.height;
        const originalMaxHeight = orderElement.style.maxHeight;
        const originalWidth = orderElement.style.width;
        
        // 2. Armazenar estado da seção de auditoria
        const auditInfoExpandedOriginal = this.auditInfoExpanded;
        this.auditInfoExpanded = false;
        
        // 3. Ocultar botões
        const actionButtons = orderElement.querySelector('.action-buttons');
        const originalButtonsDisplay = actionButtons ? actionButtons.style.display : null;
        if (actionButtons) {
          actionButtons.style.display = 'none';
        }
        
        // 4. Configurar elemento para captura
        document.body.style.overflow = 'hidden';
        orderElement.style.overflowY = 'visible';
        orderElement.style.height = 'auto';
        orderElement.style.maxHeight = 'none';
        
        // 5. Configurações específicas para dispositivos móveis
        if (isMobile) {
          // Fixar largura para evitar distorção
          orderElement.style.width = '540px';
          
          // Ajustar grid para uma coluna com base na orientação
          const grid = orderElement.querySelector('.order-details-grid');
          if (grid) {
            const originalGridStyle = grid.style.gridTemplateColumns;
            grid.style.gridTemplateColumns = '1fr';
            grid.style.gap = '12px';
            
            // Restaurar depois
            setTimeout(() => {
              grid.style.gridTemplateColumns = originalGridStyle;
            }, 2000);
          }
          
          // Marcar o elemento com a orientação
          orderElement.setAttribute('data-orientation', isPortrait ? 'portrait' : 'landscape');
        } else {
          // Configurações específicas para desktop para evitar cortes
          orderElement.style.width = `${orderElement.offsetWidth}px`;
          
          // Aumentar tamanho da logo
          const logo = orderElement.querySelector('.logo');
          if (logo) {
            const originalLogoWidth = logo.style.width;
            logo.style.width = '200px';
            
            // Restaurar depois
            setTimeout(() => {
              logo.style.width = originalLogoWidth;
            }, 2000);
          }
          
          // Ajustar espaçamentos para compactação no desktop
          const grid = orderElement.querySelector('.order-details-grid');
          if (grid) {
            const originalGridGap = grid.style.gap;
            const originalGridPadding = grid.style.padding;
            
            grid.style.gap = '12px';
            grid.style.padding = '16px';
            
            // Reduzir espaço nos itens
            const items = grid.querySelectorAll('.detail-item');
            const originalItemPaddings = [];
            
            items.forEach((item, index) => {
              originalItemPaddings[index] = item.style.padding;
              item.style.padding = '12px';
            });
            
            // Restaurar depois
            setTimeout(() => {
              grid.style.gap = originalGridGap;
              grid.style.padding = originalGridPadding;
              
              items.forEach((item, index) => {
                item.style.padding = originalItemPaddings[index];
              });
            }, 2000);
          }
          
          // Reorganizar completamente o grid para desktop na geração de imagem
          this.reorganizeGridForImageCapture(orderElement);
          
          // Reduzir padding inferior (sem adicionar padding extra)
          orderElement.style.paddingBottom = '20px';
        }
        
        try {
          // 6. Aguardar rendering
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          // Forçar recálculo de layout
          void orderElement.offsetHeight;
          
          // Calcular a altura total do conteúdo
          const fullHeight = orderElement.scrollHeight || orderElement.offsetHeight;
          console.log('[DEBUG] Altura total no método fallback:', fullHeight);
          
          // 7. Capturar com configurações mais básicas
          const canvas = await html2canvas(orderElement, {
            useCORS: true,
            allowTaint: true,
            backgroundColor: "#1c1c1c",
            scale: isMobile ? 1.5 : 2, // Escala menor para dispositivos móveis
            height: fullHeight + 100, // Aumentar margem extra para evitar cortes
            width: orderElement.offsetWidth,
            windowHeight: fullHeight + 100, // Margem maior para desktop
            windowWidth: orderElement.offsetWidth,
            scrollY: 0,
            scrollX: 0,
            onclone: (document, clonedOrderElement) => {
              // Garantir que elementos estejam visíveis no clone
              const allDetailItems = clonedOrderElement.querySelectorAll('.detail-item');
              allDetailItems.forEach(item => {
                item.style.opacity = '1';
                item.style.visibility = 'visible';
                item.style.display = 'flex';
                
                // Ajustes específicos para mobile
                if (isMobile) {
                  item.style.padding = '10px';
                  item.style.margin = '0';
                  item.style.minHeight = 'auto';
                }
              });
              
              // Ocultar botões e seção de auditoria
              const buttons = clonedOrderElement.querySelectorAll('button');
              buttons.forEach(btn => btn.style.display = 'none');
              
              const auditSection = clonedOrderElement.querySelector('.audit-section');
              if (auditSection) auditSection.style.display = 'none';
              
              // Configurações específicas para dispositivos móveis
              if (isMobile) {
                const grid = clonedOrderElement.querySelector('.order-details-grid');
                if (grid) {
                  grid.style.gridTemplateColumns = '1fr';
                  grid.style.gap = '12px';
                }
                
                // Ajustar cabeçalho
                const header = clonedOrderElement.querySelector('.modal-header');
                if (header) {
                  header.style.marginBottom = '8px';
                }
                
                // Ajustar logo com base na orientação
                const logo = clonedOrderElement.querySelector('.logo');
                if (logo) {
                  logo.style.width = isPortrait ? '100px' : '120px';
                  logo.style.marginBottom = '10px';
                }
                
                // Ajustar título
                const title = clonedOrderElement.querySelector('.modal-header h2');
                if (title) {
                  title.style.fontSize = isPortrait ? '1.1rem' : '1.2rem';
                  title.style.marginBottom = '10px';
                }
                
                // Ajustar ID do pedido
                const orderId = clonedOrderElement.querySelector('.order-id p');
                if (orderId) {
                  orderId.style.fontSize = isPortrait ? '0.9rem' : '1rem';
                }
                
                // Marcar o elemento com a orientação
                clonedOrderElement.setAttribute('data-orientation', isPortrait ? 'portrait' : 'landscape');
              } else {
                // Aumentar tamanho da logo no desktop
                const logo = clonedOrderElement.querySelector('.logo');
                if (logo) {
                  logo.style.width = '200px';
                  logo.style.marginBottom = '12px';
                }
                
                // Reduzir espaçamentos no clone para desktop
                clonedOrderElement.style.gap = '16px';
                clonedOrderElement.style.paddingBottom = '20px';
                
                const grid = clonedOrderElement.querySelector('.order-details-grid');
                if (grid) {
                  grid.style.gap = '12px';
                  grid.style.padding = '16px';
                  grid.style.marginBottom = '10px';
                  
                  // Reduzir padding dos itens
                  const items = grid.querySelectorAll('.detail-item');
                  items.forEach(item => {
                    item.style.padding = '12px';
                    item.style.marginBottom = '0';
                  });
                  
                  // Identificar o campo de observação para dar tratamento especial
                  const obsItem = Array.from(grid.querySelectorAll('.detail-item')).find(item => {
                    const label = item.querySelector('strong');
                    return label && label.textContent.includes('OBSERVAÇÃO');
                  });
                  
                  if (obsItem) {
                    obsItem.style.gridColumn = '1 / -1';
                    obsItem.style.padding = '12px';
                  }
                }
                
                // Aplicar o mesmo método de reorganização do grid no clone
                this.reorganizeClonedGrid(clonedOrderElement);
              }
            }
          });
          
          // 8. Baixar imagem
          const imgData = canvas.toDataURL('image/png');
          const link = document.createElement('a');
          link.href = imgData;
          link.download = `pedido_${this.pedido.id || 'novo'}_fallback.png`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          toast.success("Imagem gerada com método alternativo!");
        } catch (error) {
          console.error("Erro no método de fallback:", error);
          toast.error("Não foi possível gerar a imagem. Tente novamente mais tarde.");
        } finally {
          // 9. Restaurar configurações originais
          document.body.style.overflow = originalOverflow;
          orderElement.style.overflowY = originalOverflowY;
          orderElement.style.height = originalHeight;
          orderElement.style.maxHeight = originalMaxHeight;
          orderElement.style.width = originalWidth;
          this.auditInfoExpanded = auditInfoExpandedOriginal;
          
          if (actionButtons && originalButtonsDisplay !== null) {
            actionButtons.style.display = originalButtonsDisplay;
          }
        }
      } catch (error) {
        console.error("Erro no método de fallback:", error);
        toast.error("Não foi possível gerar a imagem. Tente novamente mais tarde.");
      }
    },
    // Método para reorganizar o grid durante a captura de imagem
    reorganizeGridForImageCapture(container) {
      // Obter o grid principal
      const grid = container.querySelector('.order-details-grid');
      if (!grid) return;
      
      // Configurar o grid para 2 colunas uniformes
      grid.style.display = 'grid';
      grid.style.gridTemplateColumns = '1fr 1fr';
      grid.style.gap = '12px'; // Reduzido de 16px para 12px
      grid.style.marginBottom = '10px'; // Reduzido de 20px para 10px
      
      // Obter todos os itens do grid
      const items = grid.querySelectorAll('.detail-item');
      
      // Retirar todos os items do grid para reordená-los
      const itemsArray = Array.from(items);
      itemsArray.forEach(item => grid.removeChild(item));
      
      // Compactação: reduzir o padding dos itens de detalhe
      itemsArray.forEach(item => {
        item.style.padding = '12px'; // Reduzido de 15px
        item.style.marginBottom = '0';
      });
      
      // Identificar o campo de observação
      const observacaoItem = itemsArray.find(item => {
        const label = item.querySelector('strong');
        return label && label.textContent.includes('OBSERVAÇÃO');
      });
      
      // Remover o campo de observação do array se encontrado
      if (observacaoItem) {
        const index = itemsArray.indexOf(observacaoItem);
        if (index > -1) {
          itemsArray.splice(index, 1);
        }
      }
      
      // Organizar os itens em duas colunas, exceto observação
      itemsArray.forEach(item => {
        // Remover classes que possam afetar o grid
        item.classList.remove('full-width');
        item.style.gridColumn = 'auto';
        
        // Adicionar de volta ao grid
        grid.appendChild(item);
      });
      
      // Adicionar o campo de observação como última linha ocupando toda a largura
      if (observacaoItem) {
        observacaoItem.style.gridColumn = '1 / -1'; // Ocupar todas as colunas
        observacaoItem.classList.add('full-width');
        // Compactar o campo de observação
        observacaoItem.style.padding = '12px';
        grid.appendChild(observacaoItem);
      }
      
      // Reduzir espaçamento para garantir maior compactação
      const lastItems = Array.from(grid.querySelectorAll('.detail-item')).slice(-3);
      lastItems.forEach(item => {
        item.style.marginBottom = '0'; // Reduzido de 10px para 0
        item.style.paddingBottom = '12px'; // Reduzido de 15px para 12px
      });
    },
    // Método para reorganizar o grid do clone no método de fallback
    reorganizeClonedGrid(container) {
      // Obter o grid principal
      const grid = container.querySelector('.order-details-grid');
      if (!grid) return;
      
      // Configurar o grid para 2 colunas uniformes
      grid.style.display = 'grid';
      grid.style.gridTemplateColumns = '1fr 1fr';
      grid.style.gap = '16px';
      grid.style.marginBottom = '20px';
      
      // Obter todos os itens do grid
      const items = grid.querySelectorAll('.detail-item');
      const itemsArray = Array.from(items);
      
      // Remover classes e configurações que possam afetar o grid
      itemsArray.forEach(item => {
        item.classList.remove('full-width');
        item.style.gridColumn = 'auto';
      });
      
      // Identificar o campo de observação
      const observacaoItem = itemsArray.find(item => {
        const label = item.querySelector('strong');
        return label && label.textContent.includes('OBSERVAÇÃO');
      });
      
      // Configurar o campo de observação para ocupar toda a largura
      if (observacaoItem) {
        observacaoItem.style.gridColumn = '1 / -1';
        observacaoItem.classList.add('full-width');
        
        // Mover para o final do grid
        grid.appendChild(observacaoItem);
      }
      
      // Adicionar espaçamento para garantir que nada seja cortado
      const lastItems = Array.from(grid.querySelectorAll('.detail-item')).slice(-3);
      lastItems.forEach(item => {
        item.style.marginBottom = '10px';
        item.style.paddingBottom = '15px';
      });
    },
  },
};
</script>

<style scoped>
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
  z-index: 999999;
  padding: 20px;
}

.print-modal {
  background-color: #1c1c1c;
  color: #f5f5f5;
  width: 100%;
  max-width: 550px;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow-y: auto;
  max-height: 85vh;
}

/* Aplicando estilos à versão clonada do modal para captura de imagem */
[style*="position:absolute"][style*="top:-9999px"] {
  /* Garantindo que o clone seja renderizado corretamente */
  background-color: #1c1c1c !important;
  padding: 30px !important;
  width: 550px !important;
  border-radius: 0 !important; /* Remover para evitar problemas de recorte */
  box-shadow: none !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 24px !important;
  overflow: visible !important;
  height: auto !important;
  max-height: none !important;
}

/* Estilos específicos para o elemento usado para captura */
[data-capture-clone="true"] {
  color: #f5f5f5 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol" !important;
  line-height: 1.5 !important;
  letter-spacing: 0.5px !important;
}

[data-capture-clone="true"] .detail-item {
  background-color: #333 !important;
  padding: 15px !important;
  border: 1px solid #424242 !important;
  border-radius: 10px !important;
  margin-bottom: 0 !important;
}

[data-capture-clone="true"] .order-details-grid {
  background-color: #2a2a2a !important;
  padding: 20px !important;
  border-radius: 12px !important;
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 16px !important;
}

[data-capture-clone="true"] .detail-item strong {
  color: #ff6f61 !important;
  display: block !important;
  margin-bottom: 8px !important;
  font-weight: bold !important;
}

[data-capture-clone="true"] .detail-item span {
  color: #f5f5f5 !important;
  display: block !important;
}

[data-capture-clone="true"] .detail-item.full-width {
  grid-column: 1 / -1 !important;
}

.modal-header {
  text-align: center;
  margin-bottom: 10px;
  position: relative;
}

.logo {
  width: 160px;
  margin-bottom: 15px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.modal-header h2 {
  color: #ff6f61;
  font-size: 1.4rem;
  margin: 0 0 15px 0;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.order-id {
  margin: 0 auto;
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 12px 15px;
  text-align: center;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15) inset;
}

.order-id p {
  margin: 0;
  font-size: 1.2rem;
  color: #ff6f61;
  font-weight: 600;
}

/* Layout em grid para os detalhes */
.order-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.detail-item {
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
  background-color: #333;
  border-radius: 10px;
  padding: 15px;
  border: 1px solid #424242;
  transition: all 0.2s ease;
}

.detail-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  border-color: rgba(255, 111, 97, 0.4);
}

.detail-item.full-width {
  grid-column: span 2;
}

.detail-item strong {
  color: #ff6f61;
  margin-bottom: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.detail-item span {
  line-height: 1.5;
  font-size: 1rem;
}

/* Badges de urgência */
.badge-container {
  display: flex;
  align-items: center;
}

.urgency-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.urgency-badge.normal {
  background-color: #3498db;
  color: white;
}

.urgency-badge.urgent {
  background-color: #f39c12;
  color: white;
}

.urgency-badge.critical {
  background-color: #e74c3c;
  color: white;
}

/* Status badges */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.status-badge.status-completed {
  background-color: #2ecc71;
  color: white;
}

.status-badge.status-progress {
  background-color: #3498db;
  color: white;
}

.status-badge.status-pending {
  background-color: #f39c12;
  color: white;
}

.status-badge.status-canceled {
  background-color: #e74c3c;
  color: white;
}

/* Seção de anexo */
.attachment-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  background-color: #2a2a2a;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.attachment-section strong {
  color: #ff6f61;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.order-attachment {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 5px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Seção de auditoria */
.audit-section {
  background-color: #2a2a2a;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 5px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border: 1px solid #424242;
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #333;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.audit-header:hover {
  background-color: #3a3a3a;
}

.audit-header strong {
  color: #ff6f61;
  font-size: 0.9rem;
  font-weight: 600;
}

.audit-header i {
  color: #ff6f61;
  font-size: 0.9rem;
}

.audit-details {
  padding: 15px 20px;
  background-color: #2a2a2a;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.audit-item {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
}

.audit-item strong {
  color: #bbb;
  margin-bottom: 4px;
  font-weight: 600;
}

.audit-item span {
  color: #f5f5f5;
}

/* Botões */
.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 5px;
}

button {
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #424242;
  color: white;
  text-transform: uppercase;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  letter-spacing: 0.5px;
}

button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

button:active:not(:disabled) {
  transform: translateY(-1px);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button.close-btn {
  grid-column: span 2;
  background-color: #555;
}

button.close-btn:hover:not(:disabled) {
  background-color: #ff6f61;
}

button.print-btn {
  background-color: #ff6f61;
  position: relative;
  overflow: hidden;
}

button.print-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateX(-100%);
  transition: transform 0.4s ease;
}

button.print-btn:hover::after {
  transform: translateX(0);
}

button.print-btn:hover:not(:disabled) {
  background-color: #e05648;
}

button.primary-btn {
  background-color: #2ecc71;
  position: relative;
  overflow: hidden;
}

button.primary-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateX(-100%);
  transition: transform 0.4s ease;
}

button.primary-btn:hover::after {
  transform: translateX(0);
}

button.primary-btn:hover:not(:disabled) {
  background-color: #27ae60;
}

/* Responsividade */
@media screen and (max-width: 1024px) {
  .print-modal {
    width: var(--modal-width-md);
    max-width: var(--modal-max-width);
    padding: var(--spacing-md);
  }
}

@media screen and (max-width: 768px) {
  .order-details-grid {
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-sm);
  }

  .print-modal {
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding: var(--spacing-md);
  }
  
  .action-buttons {
    gap: var(--spacing-sm);
  }
}

@media screen and (max-width: 600px) {
  .order-details-grid {
    grid-template-columns: 1fr;
  }

  .detail-item.full-width {
    grid-column: 1;
  }
  
  .print-modal {
    padding: var(--spacing-sm);
    border-radius: var(--border-radius-lg);
    width: var(--modal-width-lg);
    max-width: var(--modal-max-width);
    padding-bottom: 120px; /* Espaço adicional para os botões fixos */
  }
  
  .action-buttons {
    grid-template-columns: 1fr;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #1f1f1f;
    z-index: 10;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
    padding: 10px;
    margin: 0;
    gap: 10px;
  }
  
  .close-btn {
    grid-column: 1 !important;
  }

  .order-id p {
    font-size: var(--font-size-lg);
  }

  .modal-header h2 {
    font-size: var(--font-size-lg);
  }

  button {
    padding: var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
}

/* Ajustes específicos para notebooks com zoom */
@media screen and (min-resolution: 1.25dppx) {
  .print-modal {
    max-height: var(--modal-max-height);
  }
}

/* Ajustes para telas 720p */
@media (min-height: 720px) and (max-height: 768px) {
  .modal-overlay {
    align-items: flex-start;
    padding-top: 2vh;
  }
  
  .print-modal {
    max-height: 85vh;
  }
}

/* Ajustes para monitores pequenos de 14 polegadas */
@media screen and (max-width: 1366px) and (max-height: 768px) {
  .print-modal {
    padding: var(--spacing-md);
  }
}

/* Quando o modal estiver sendo impresso/capturado */
@media print {
  .modal-overlay {
    background-color: transparent;
    padding: 0;
  }
  
  .print-modal {
    box-shadow: none;
  }
  
  .action-buttons {
    display: none;
  }

  .audit-section {
    display: none;
  }
}

[data-capture-clone="true"] .action-buttons,
[style*="position:absolute"][style*="top:-9999px"] .action-buttons {
  display: none !important;
}

/* Versão otimizada para captura de imagem - mantida por compatibilidade */
.print-modal.print-capture {
  /* Removendo limitações de altura durante a captura */
  max-height: none !important;
  overflow: visible !important;
  /* Garantindo que não haja sombras */
  box-shadow: none !important;
  /* Garantir que todos os elementos sejam visíveis */
  transform: none !important;
  transition: none !important;
  /* Mostrar todos os detalhes */
  display: flex !important;
  flex-direction: column !important;
}

/* Estilos específicos para o clone em dispositivos móveis */
@media screen and (max-width: 600px) {
  [data-capture-clone="true"] {
    width: 540px !important;
    font-size: 14px !important;
  }
  
  [data-capture-clone="true"] .order-details-grid {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  
  [data-capture-clone="true"] .detail-item {
    padding: 10px !important;
    margin: 0 !important;
    min-height: auto !important;
  }
  
  [data-capture-clone="true"] .logo {
    width: 120px !important;
    margin-bottom: 10px !important;
  }
  
  [data-capture-clone="true"] .modal-header h2 {
    font-size: 1.2rem !important;
    margin-bottom: 10px !important;
  }
  
  [data-capture-clone="true"] .order-id p {
    font-size: 1rem !important;
  }
  
  /* Ajustes específicos para orientação retrato */
  [data-capture-clone="true"][data-orientation="portrait"] {
    width: 480px !important; /* Largura um pouco menor para retrato */
  }
  
  [data-capture-clone="true"][data-orientation="portrait"] .logo {
    width: 100px !important;
  }
  
  [data-capture-clone="true"][data-orientation="portrait"] .modal-header h2 {
    font-size: 1.1rem !important;
  }
  
  [data-capture-clone="true"][data-orientation="portrait"] .order-id p {
    font-size: 0.9rem !important;
  }
  
  /* Garantir que elementos do componente original não afetem a captura */
  .print-modal {
    transform: none !important;
  }
}

/* Estilos específicos para desktop na captura de imagem */
@media screen and (min-width: 601px) {
  [data-capture-clone="true"] {
    max-width: 650px !important; /* Largura máxima mais ampla para desktop */
    padding: 40px 30px !important; /* Padding maior para evitar cortes */
    padding-bottom: 80px !important; /* Padding extra na parte inferior */
  }
  
  [data-capture-clone="true"] .detail-item {
    padding: 15px !important;
    margin-bottom: 0 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
  }
  
  /* Garantir que os últimos itens não sejam cortados */
  [data-capture-clone="true"] .detail-item:nth-last-child(-n+3) {
    padding-bottom: 20px !important;
    margin-bottom: 15px !important;
  }
  
  /* Estilo específico para o campo de observação */
  [data-capture-clone="true"] .detail-item.full-width {
    grid-column: 1 / -1 !important;
    width: 100% !important;
    background-color: #333 !important;
    border: 1px solid rgba(255, 111, 97, 0.4) !important;
    padding: 20px !important;
    margin-top: 15px !important;
  }
  
  /* Garantir que o texto da observação tenha uma apresentação adequada */
  [data-capture-clone="true"] .detail-item.full-width span {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    line-height: 1.6 !important;
  }
  
  [data-capture-clone="true"] .order-details-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 16px !important;
    padding: 20px !important;
    margin-bottom: 30px !important; /* Margem extra no final do grid */
  }
}

/* Estilos globais para o clone de captura em dispositivos móveis */
@media print, screen and (max-width: 600px) {
  [data-capture-clone="true"] {
    /* Garantir que o clone tenha tamanho adequado em dispositivos móveis */
    width: 540px !important;
    transform: none !important;
    background-color: #1c1c1c !important;
  }
  
  /* Ajustar para orientação retrato */
  [data-capture-clone="true"][data-orientation="portrait"] {
    width: 480px !important;
  }
}

/* Estilos específicos para o clone de captura em desktops */
@media print, screen and (min-width: 601px) {
  [data-capture-clone="true"] {
    max-width: 650px !important;
    background-color: #1c1c1c !important;
    transform: none !important;
  }
  
  /* Destacar o campo de observação na captura */
  [data-capture-clone="true"] .detail-item.full-width strong {
    color: #ff6f61 !important;
    margin-bottom: 15px !important;
    font-size: 1rem !important;
  }
}

/* Dispositivos móveis muito pequenos */
@media screen and (max-width: 480px) {
  .print-modal {
    padding-bottom: 140px; /* Ainda mais espaço para os botões fixos */
  }
  
  .action-buttons {
    gap: 8px;
    padding: 8px;
  }
  
  button {
    padding: 12px 8px;
    font-size: 0.85rem;
  }
}
</style>

