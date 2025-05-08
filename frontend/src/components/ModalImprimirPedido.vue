<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="print-modal" @click.stop ref="orderContent">
      <!-- Header com o logo -->
      <div class="modal-header">
        <img src="@/assets/logo.png" alt="LOGO" class="logo" />
        <h2>DETALHES DO PEDIDO</h2>
      </div>

      <!-- ID do Pedido destacado -->
      <div class="order-id">
        <p><strong>PEDIDO Nº :    </strong> {{pedido.id }}</p>
      </div>

      <!-- Detalhes do Pedido -->
      <div class="order-details">
        <p><strong>DESCRIÇÃO:</strong> {{ (pedido.descricao || 'Não informado').toUpperCase() }}</p>
        <p><strong>QUANTIDADE:</strong> {{ pedido.quantidade || 0 }}</p>
        <p><strong>URGÊNCIA:</strong> {{ (pedido.urgencia || 'Normal').toUpperCase() }}</p>
        <p><strong>CATEGORIA:</strong> {{ (pedido.categoria || 'Não categorizado').toUpperCase() }}</p>
        <p><strong>DATA DO PEDIDO:</strong> {{ formatDate(pedido.deliveryDate || new Date()).toUpperCase() }}</p>
        <p v-if="pedido.status === 'Concluído'"><strong>DATA DE CONCLUSÃO:</strong> {{ formatDate(pedido.conclusao_data || new Date()).toUpperCase() }}</p>
        <p><strong>OBSERVAÇÃO:</strong> {{ pedido.observacao ? pedido.observacao.toUpperCase() : "NENHUMA" }}</p>
        <p><strong>RESPONSÁVEL:</strong> {{ (pedido.sender || 'Não informado').toUpperCase() }}</p>
        <p v-if="pedido.status"><strong>STATUS:</strong> {{ pedido.status.toUpperCase() }}</p>
        <div v-if="pedido.anexo">
          <p><strong>ANEXO:</strong></p>
          <img :src="'data:image/png;base64,' + pedido.anexo" alt="ANEXO" class="order-attachment" />
        </div>
      </div>
      
      <!-- Histórico de Alterações Expansível -->
      <div class="order-history">
        <div class="history-header" @click="toggleHistory">
          <strong>HISTÓRICO DE ALTERAÇÕES</strong>
          <span class="toggle-icon">{{ isHistoryExpanded ? '▼' : '►' }}</span>
        </div>
        <div v-if="isHistoryExpanded" class="history-content">
          <div v-if="isLoadingHistory" class="loading-history">
            Carregando histórico...
          </div>
          <div v-else-if="historico.length === 0" class="empty-history">
            Nenhuma alteração registrada.
          </div>
          <div v-else class="history-list">
            <div v-for="(item, index) in historico" :key="index" class="history-item">
              <div class="history-header">
                <span class="history-user">{{ item.usuario_nome }}</span>
                <span class="history-date">{{ formatDateTime(item.data_edicao) }}</span>
              </div>
              <div class="history-details">
                <span class="field">{{ item.campo_alterado }}</span>:
                <span class="old-value">{{ item.valor_anterior }}</span> →
                <span class="new-value">{{ item.valor_novo }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Botões -->
      <button @click="generateImage">GERAR IMAGEM</button>
      <button class="primary-btn" @click="createNewOrder">NOVO PEDIDO</button>
      <button class="close-btn" @click="closeModal">FECHAR</button>
    </div>
  </div>
</template>

<script>
import html2canvas from "html2canvas";
// Importação modificada para evitar o erro de 'module is not defined'
import * as axiosModule from "axios";
const axios = axiosModule.default || axiosModule;

export default {
  name: 'ModalImprimirPedido',
  props: {
    isOpen: Boolean,
    pedido: Object,
  },
  data() {
    return {
      isHistoryExpanded: false,
      historico: [],
      isLoadingHistory: false,
      ultimaAtualizacao: null
    };
  },
  mounted() {
    // Quando o componente for montado, já carregamos os dados do histórico
    // mas mantemos ele recolhido por padrão
    if (this.isOpen && this.pedido && this.pedido.id) {
      console.log("Modal montado, pré-carregando histórico");
      // Pré-carregar o histórico mantendo-o recolhido
      this.carregarHistorico();
    }
  },
  watch: {
    isOpen(newVal) {
      if (newVal && this.pedido) {
        // Resetar o estado do histórico
        this.isHistoryExpanded = false;
        // Pré-carregar o histórico em segundo plano
        this.carregarHistorico();
      }
    },
    pedido(newVal) {
      if (newVal && this.isOpen) {
        // Caso o pedido mude enquanto o modal estiver aberto
        console.log("Pedido mudou, recarregando histórico");
        this.isHistoryExpanded = false;
        this.historico = [];
        // Carregar o histórico do novo pedido
        this.carregarHistorico();
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    createNewOrder() {
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
    formatDateTime(dateTime) {
      if (!dateTime) return 'Data não informada';
      
      try {
        const d = new Date(dateTime);
        
        // Verificar se a data é válida
        if (isNaN(d.getTime())) {
          console.warn(`Data inválida: ${dateTime}`);
          return 'Data inválida';
        }
        
        return new Intl.DateTimeFormat('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false  // Garantir formato 24h
        }).format(d);
      } catch (error) {
        console.error(`Erro ao formatar data: ${dateTime}`, error);
        return 'Erro de formato';
      }
    },
    async generateImage() {
      const orderElement = this.$refs.orderContent;
      const buttons = this.$el.querySelectorAll('button'); 

      if (orderElement) {
        // Ocultar os botões antes de gerar a imagem
        buttons.forEach(btn => btn.classList.add('hidden'));

        // Escalar o conteúdo para caber em uma única página
        const originalScale = orderElement.style.transform;
        const originalWidth = orderElement.style.width;

        // Garantir que a largura da área de impressão seja fixa
        orderElement.style.width = '800px'; 
        orderElement.style.transform = 'scale(1)'; 

        // Captura o canvas após o ajuste
        const canvas = await html2canvas(orderElement, {
          useCORS: true,
          scrollX: 0,
          scrollY: -window.scrollY,
        });

        // Reverter os estilos ao estado original
        orderElement.style.transform = originalScale || '';
        orderElement.style.width = originalWidth || '';

        // Gerar imagem PNG
        const imgData = canvas.toDataURL('image/png');

        // Criar um link para baixar a imagem
        const link = document.createElement('a');
        link.href = imgData;
        link.download = `pedido_${this.pedido.id}.png`; 
        link.click();

        // Restaurar a visibilidade dos botões
        buttons.forEach(btn => btn.classList.remove('hidden'));
      }
    },
    toggleHistory() {
      this.isHistoryExpanded = !this.isHistoryExpanded;
      
      // Se estamos expandindo e não temos dados ou eles estão desatualizados
      if (this.isHistoryExpanded) {
        console.log("Expandindo seção de histórico");
        
        // Se não temos histórico ou já se passaram mais de 5 segundos desde a última carga
        const forcarRecarga = this.historico.length === 0 || 
                              (this.ultimaAtualizacao && 
                               (Date.now() - this.ultimaAtualizacao > 5000));
        
        if (forcarRecarga) {
          console.log("Recarregando histórico ao expandir");
          this.carregarHistorico();
        }
      }
    },
    async carregarHistorico() {
      if (!this.pedido || !this.pedido.id) {
        console.log("Não é possível carregar histórico: pedido inválido ou sem ID");
        this.isLoadingHistory = false;
        return;
      }
      
      this.isLoadingHistory = true;
      console.log("Carregando histórico para o pedido ID:", this.pedido.id);
      
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          console.warn("Token de autenticação não encontrado");
          this.isLoadingHistory = false;
          return;
        }
        
        const url = `${process.env.VUE_APP_API_URL}/pedidos/${this.pedido.id}/historico`;
        console.log("URL da requisição:", url);
        
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        // Verificar se a resposta contém dados válidos
        if (response.data && Array.isArray(response.data)) {
          console.log("Histórico recebido:", response.data);
          this.historico = response.data;
          
          // Filtrar quaisquer entradas inválidas
          this.historico = this.historico.filter(item => 
            item && 
            item.campo_alterado && 
            (item.valor_anterior !== undefined || item.valor_novo !== undefined)
          );
          
          if (this.historico.length === 0) {
            console.log("Nenhum histórico válido encontrado para este pedido");
          } else {
            console.log(`Encontrados ${this.historico.length} registros no histórico`);
          }
        } else {
          console.warn("Resposta inválida ao carregar histórico:", response.data);
          this.historico = [];
        }
        
        this.ultimaAtualizacao = Date.now();
      } catch (error) {
        console.error("Erro ao carregar histórico do pedido:", error);
        if (error.response) {
          console.error("Detalhes do erro:", error.response.data);
          console.error("Status do erro:", error.response.status);
        }
        this.historico = [];
      } finally {
        this.isLoadingHistory = false;
      }
    }
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.print-modal {
  background-color: #1f1f1f;
  color: #f5f5f5;
  padding: 25px;
  border-radius: 0px;
  width: 100%;
  max-width: 500px;
  box-sizing: border-box;
  text-align: left;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.print-modal h2 {
  color: #ff6f61;
  text-align: center;
  font-size: 1.4rem;
  margin-bottom: 20px;
}

.modal-header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  width: 180px;
  margin-bottom: 10px;
}

.order-id {
  text-align: center;
  margin: 20px 0;
  font-size: 1.2rem;
  background-color: #333;
  color: #ff6f61;
  padding: 10px;
  border-radius: 8px;
}

.order-details p {
  margin-bottom: 15px;
  font-size: 1rem;
  text-transform: uppercase;
}

.order-details strong {
  color: #ff6f61;
}

.order-attachment {
  margin-top: 15px;
  max-width: 200px; 
  max-height: 200px; 
  width: auto; 
  height: auto; 
  border-radius: 5px;
  object-fit: contain; 
}

/* Estilos para o histórico de alterações */
.order-history {
  margin-top: 20px;
  border-top: 1px solid #444;
  padding-top: 15px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 10px;
  background-color: #333;
  border-radius: 5px;
  margin-bottom: 5px;
  user-select: none;
}

.history-header strong {
  color: #ff6f61;
}

.toggle-icon {
  color: #ff6f61;
  font-size: 14px;
}

.history-content {
  padding: 10px;
  background-color: #272727;
  border-radius: 5px;
  margin-top: 5px;
  max-height: 200px;
  overflow-y: auto;
}

.loading-history, .empty-history {
  padding: 15px;
  text-align: center;
  color: #aaa;
  font-style: italic;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  background-color: #333;
  border-radius: 5px;
  padding: 10px;
}

.history-item .history-header {
  background-color: transparent;
  padding: 0;
  margin-bottom: 5px;
}

.history-user {
  font-weight: bold;
  color: #e0e0e0;
}

.history-date {
  color: #aaa;
  font-size: 0.85em;
}

.history-details {
  font-size: 0.9em;
  color: #ddd;
}

.field {
  font-weight: bold;
  color: #ff6f61;
}

.old-value {
  color: #ff6f61;
  text-decoration: line-through;
  margin: 0 5px;
}

.new-value {
  color: #2ecc71;
  margin-left: 5px;
}

button {
  background-color: #424242;
  color: #f5f5f5;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  margin-top: 20px;
  width: 100%;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button.close-btn {
  background-color: #555;
}

button.primary-btn {
  background-color: #2ecc71;
  color: #1f1f1f;
  margin-top: 10px;
}

button.primary-btn:hover {
  background-color: #27ae60;
}

button:hover {
  background-color: #ff6f61;
  color: #1f1f1f;
}

.order-attachment {
  margin-top: 15px;
  max-width: 100%;
  border-radius: 5px;
}

.hidden {
  display: none;
}

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .print-modal {
    max-width: 90%;
    padding: 20px;
  }
  
  .logo {
    width: 150px;
  }
  
  .order-details p {
    font-size: 0.95rem;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .print-modal {
    width: 90%;
    max-width: 400px;
    padding: 15px;
  }
  
  .logo {
    width: 120px;
  }
  
  .order-details p {
    font-size: 0.9rem;
  }
  
  button {
    padding: 10px 15px;
    font-size: 0.9rem;
  }
}

.activity-details a {
  color: #8ab4f8;
  cursor: pointer;
  text-decoration: underline;
}

/* Estilo atualizado para o hiperlink de ver pedido */
.activity-details a {
  display: inline-block;
  background-color: #4a6da7;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.85em;
  margin-top: 5px;
  transition: background-color 0.3s, transform 0.2s;
}

.activity-details a:hover {
  background-color: #5e82bc;
  transform: translateY(-2px);
}
</style>
