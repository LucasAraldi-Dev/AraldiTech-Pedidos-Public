<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleOverlayClick">
    <div class="order-form" @click.stop>
      <div class="form-header">
        <h2>EDITAR PEDIDO <span class="order-id">#{{ pedido?.id }}</span></h2>
        <div class="user-info" v-if="userName">
          <span class="user-label">Editado por:</span>
          <span class="user-name">{{ userName }}</span>
        </div>
      </div>

      <!-- Formulário de Edição do Pedido -->
      <form v-show="!successMessage" @submit.prevent="handleUpdateOrder">
        <div class="form-grid">
          <div class="form-group full-width">
            <label for="orderDescription">
              <i class="material-icons">description</i>
              DESCRIÇÃO DO PEDIDO
            </label>
            <textarea
              id="orderDescription"
              v-model="orderDescription"
              placeholder="DESCRIÇÃO DO PEDIDO"
              required
            ></textarea>
          </div>

          <div class="form-group">
            <label for="orderQuantity">
              <i class="material-icons">format_list_numbered</i>
              QUANTIDADE
            </label>
            <div class="quantity-input-container">
              <button type="button" class="quantity-btn" @click="decrementQuantity" :disabled="orderQuantity <= 1">
                <i class="material-icons">remove</i>
              </button>
              <input 
                id="orderQuantity" 
                type="number" 
                v-model.number="orderQuantity" 
                min="1" 
                @input="validateQuantity"
                required 
                :class="{ 'invalid': validationErrors.quantity }"
              />
              <button type="button" class="quantity-btn" @click="incrementQuantity">
                <i class="material-icons">add</i>
              </button>
            </div>
            <div class="input-note">
              Quantidade mínima: 1
            </div>
          </div>

          <div class="form-group">
            <label for="orderCategory">
              <i class="material-icons">category</i>
              CATEGORIA
            </label>
            <select id="orderCategory" v-model="orderCategory" required>
              <option value="" disabled>SELECIONE A CATEGORIA</option>
              <option value="Matérias-primas">Matérias-primas</option>
              <option value="Equipamentos e Máquinas">Equipamentos e Máquinas</option>
              <option value="Peças de Reposição">Peças de Reposição</option>
              <option value="Serviços">Serviços</option>
              <option value="Mercadorias diversas">Mercadorias diversas</option>
            </select>
          </div>

          <div class="form-group">
            <label for="orderUrgency">
              <i class="material-icons">priority_high</i>
              URGÊNCIA
            </label>
            <select id="orderUrgency" v-model="orderUrgency" required>
              <option value="Padrão">Padrão (Sem prioridade)</option>
              <option value="Urgente">Urgente (Para o mesmo dia)</option>
              <option value="Crítico">Crítico (Fábrica parada)</option>
            </select>
          </div>

          <div class="form-group">
            <label for="orderDeliveryDate">
              <i class="material-icons">event</i>
              DATA DO PEDIDO
            </label>
            <div class="date-input-container">
              <input 
                id="orderDeliveryDate" 
                type="date" 
                v-model="orderDeliveryDate" 
                :disabled="!isAdmin"
                required 
                class="date-picker"
              />
              <i class="material-icons date-icon">calendar_today</i>
            </div>
            <div class="input-note">
              {{ isAdmin ? 'Como administrador, você pode alterar a data do pedido' : 'A data do pedido só pode ser alterada por administradores' }}
            </div>
          </div>

          <div class="form-group full-width">
            <label for="orderNotes">
              <i class="material-icons">notes</i>
              OBSERVAÇÃO
            </label>
            <textarea
              id="orderNotes"
              v-model="orderNotes"
              placeholder="OBSERVAÇÃO"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="orderSender">
              <i class="material-icons">person</i>
              RESPONSÁVEL PELA COMPRA
            </label>
            <input id="orderSender" type="text" v-model="orderSender" required />
          </div>

          <div class="form-group">
            <label for="orderSenderSector">
              <i class="material-icons">business</i>
              SETOR DO RESPONSÁVEL
            </label>
            <select 
              id="orderSenderSector" 
              v-model="orderSenderSector" 
              :disabled="!isAdminOrGestor"
              required 
            >
              <option value="Escritório">Escritório</option>
              <option value="Fábrica de Ração">Fábrica de Ração</option>
              <option value="CPO">CPO</option>
              <option value="Granjas">Granjas</option>
              <option value="Abatedouro">Abatedouro</option>
              <option value="Transporte">Transporte</option>
              <option value="Incubatório">Incubatório</option>
              <option value="Favorito">Favorito</option>
            </select>
            <div class="input-note" v-if="!isAdminOrGestor">
              O setor é definido pelo sistema e só pode ser alterado por administradores ou gestores
            </div>
          </div>

          <div class="form-group" v-if="orderStatus">
            <label for="orderStatus">
              <i class="material-icons">offline_pin</i>
              STATUS
            </label>
            <select id="orderStatus" v-model="orderStatus" required>
              <option value="Pendente">Pendente</option>
              <option value="Concluído">Concluído</option>
              <option value="Cancelado">Cancelado</option>
            </select>
          </div>
          
          <!-- Novos campos para orçamento -->
          <div class="separator full-width">
            <h3 class="section-title">
              <i class="material-icons">account_balance</i>
              Informações de Orçamento
            </h3>
          </div>

          <div class="form-group">
            <label for="orderBudget">
              <i class="material-icons">attach_money</i>
              ORÇAMENTO PREVISTO (R$)
            </label>
            <input 
              id="orderBudget" 
              type="number" 
              step="0.01" 
              min="0"
              v-model.number="orderBudget" 
              placeholder="0.00"
              @input="validateBudget"
              :class="{ 'invalid': validationErrors.budget }"
            />
            <div class="input-note" v-if="validationErrors.budget">
              {{ validationErrors.budget }}
            </div>
          </div>

          <div class="form-group">
            <label for="orderRealCost">
              <i class="material-icons">money</i>
              CUSTO REAL (R$)
            </label>
            <input 
              id="orderRealCost" 
              type="number" 
              step="0.01" 
              min="0"
              v-model.number="orderRealCost" 
              placeholder="0.00"
              @input="validateRealCost"
              :class="{ 'invalid': validationErrors.realCost }"
            />
            <div class="input-note" v-if="validationErrors.realCost">
              {{ validationErrors.realCost }}
            </div>
          </div>

          <div class="form-group">
            <label for="orderSupplier">
              <i class="material-icons">storefront</i>
              FORNECEDOR
            </label>
            <input 
              id="orderSupplier"
              type="text" 
              v-model="orderSupplier" 
              placeholder="Nome do fornecedor" 
            />
          </div>

          <div class="form-group full-width">
            <label for="orderBudgetNotes">
              <i class="material-icons">description</i>
              OBSERVAÇÕES DO ORÇAMENTO
            </label>
            <textarea 
              id="orderBudgetNotes" 
              v-model="orderBudgetNotes" 
              placeholder="Informações adicionais sobre orçamento e custos" 
              rows="3"
            ></textarea>
          </div>

          <!-- Status financeiro -->
          <div class="form-group full-width" v-if="isDiffVisible">
            <div class="financial-status" :class="financialStatusClass">
              <i class="material-icons status-icon">{{ financialStatusIcon }}</i>
              <div class="status-info">
                <h4>{{ financialStatusText }}</h4>
                <p>Diferença: R$ {{ budgetDifference.toFixed(2) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Histórico de alterações -->
        <div class="history-section" v-if="historicoAlteracoes.length > 0">
          <h3 class="history-title">
            <i class="material-icons">history</i>
            Histórico de alterações
          </h3>
          <div class="history-list">
            <div v-for="(item, index) in historicoAlteracoes" :key="index" class="history-item">
              <div class="history-header">
                <span class="history-date">{{ formatarData(item.data_edicao) }}</span>
                <span class="history-user">{{ item.usuario_nome }}</span>
              </div>
              <div class="history-content">
                <p>
                  <span class="history-field">{{ item.campo_alterado }}</span>: 
                  <span class="history-old-value">{{ item.valor_anterior }}</span> → 
                  <span class="history-new-value">{{ item.valor_novo }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="form-buttons">
          <button type="submit" class="submit-btn">
            <i class="material-icons">save</i>
            SALVAR ALTERAÇÕES
          </button>
          <button type="button" class="close-btn" @click="closeForm">
            <i class="material-icons">close</i>
            CANCELAR
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from 'vue-toastification';

export default {
  props: {
    isOpen: Boolean,
    pedido: Object,
    onClose: Function,
  },
  data() {
    return {
      orderDescription: "",
      orderQuantity: 1,
      orderCategory: "", 
      orderUrgency: "Padrão", 
      orderDeliveryDate: new Date().toISOString().split('T')[0],
      orderNotes: "",
      orderSender: "",
      orderSenderSector: "",
      orderStatus: "Pendente",
      // Novos campos para orçamento
      orderBudget: 0,
      orderRealCost: 0,
      orderSupplier: "",
      orderBudgetNotes: "",
      userEmail: null,
      userName: null,
      userType: null,
      token: null,
      validationErrors: {
        quantity: "",
        budget: "",
        realCost: ""
      },
      successMessage: false,
      historicoAlteracoes: [],
      toast: useToast()
    };
  },
  mounted() {
    // Obter informações do usuário do localStorage
    const userStr = localStorage.getItem("user");
    if (userStr) {
      try {
        const userObj = JSON.parse(userStr);
        this.userName = userObj.nome;
        this.userType = userObj.tipo_usuario;
        console.log("Tipo de usuário:", this.userType);
      } catch (e) {
        console.error("Erro ao parsear dados do usuário:", e);
      }
    }
    
    // Fallback para outros campos caso precise
    if (!this.userName) {
      this.userName = localStorage.getItem("user_name");
    }
    
    this.userEmail = localStorage.getItem("user_email"); 
    this.token = localStorage.getItem("access_token");
    
    // Verificar autenticação
    if (!this.token) {
      console.error("Usuário não autenticado.");
      this.$emit("close");
      this.toast.error("É necessário estar autenticado para editar pedidos.");
    }
    
    // Inicializar dados do pedido quando o componente for montado
    this.carregarDadosPedido();
    
    // Carregar histórico de alterações
    this.carregarHistoricoAlteracoes();
  },
  computed: {
    budgetDifference() {
      return this.orderBudget - this.orderRealCost;
    },
    isDiffVisible() {
      return this.orderBudget > 0 && this.orderRealCost > 0;
    },
    financialStatusClass() {
      if (this.budgetDifference > 0) return 'status-under-budget';
      if (this.budgetDifference < 0) return 'status-over-budget';
      return 'status-on-budget';
    },
    financialStatusText() {
      if (this.budgetDifference > 0) return 'Abaixo do orçamento';
      if (this.budgetDifference < 0) return 'Acima do orçamento';
      return 'Dentro do orçamento';
    },
    financialStatusIcon() {
      if (this.budgetDifference > 0) return 'trending_down';
      if (this.budgetDifference < 0) return 'trending_up';
      return 'trending_flat';
    },
    isAdminOrGestor() {
      return this.userType === "admin" || this.userType === "gestor";
    },
    isAdmin() {
      return this.userType === "admin";
    }
  },
  watch: {
    pedido() {
      this.carregarDadosPedido();
      this.carregarHistoricoAlteracoes();
    }
  },
  methods: {
    carregarDadosPedido() {
      if (this.pedido) {
        this.orderDescription = this.pedido.descricao || "";
        this.orderQuantity = this.pedido.quantidade || 1;
        this.orderCategory = this.pedido.categoria || "";
        this.orderUrgency = this.pedido.urgencia || "Padrão";
        
        // Formatar a data corretamente
        if (this.pedido.deliveryDate) {
          const dateObj = new Date(this.pedido.deliveryDate);
          this.orderDeliveryDate = dateObj.toISOString().split('T')[0];
        } else {
          this.orderDeliveryDate = new Date().toISOString().split('T')[0];
        }
        
        this.orderNotes = this.pedido.observacao || "";
        this.orderSender = this.pedido.sender || "";
        this.orderSenderSector = this.pedido.setor || "";
        this.orderStatus = this.pedido.status || "Pendente";
        
        // Novos campos de orçamento
        this.orderBudget = this.pedido.orcamento_previsto || 0;
        this.orderRealCost = this.pedido.custo_real || 0;
        this.orderSupplier = this.pedido.fornecedor || "";
        this.orderBudgetNotes = this.pedido.observacao_orcamento || "";
      }
    },
    async carregarHistoricoAlteracoes() {
      if (this.pedido && this.pedido.id) {
        try {
          const response = await axios.get(
            `${process.env.VUE_APP_API_URL}/pedidos/${this.pedido.id}/historico`,
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
              },
            }
          );
          this.historicoAlteracoes = response.data;
        } catch (error) {
          console.error("Erro ao carregar histórico:", error);
        }
      }
    },
    async handleUpdateOrder() {
      const toast = useToast();

      // Validar quantidade
      if (this.orderQuantity < 1) {
        this.orderQuantity = 1;
        this.validationErrors.quantity = "A quantidade deve ser maior que zero";
        toast.warning("A quantidade deve ser maior que zero!");
        return;
      }
      
      // Verificar token novamente
      this.token = localStorage.getItem("access_token");
      
      if (!this.token) {
        console.error("Usuário não autenticado.");
        toast.error("É necessário estar autenticado para editar pedidos. Faça login novamente.");
        return;
      }
      
      // Verificar campos obrigatórios
      if (!this.orderDescription || !this.orderQuantity || !this.orderSender || !this.orderCategory) {
        toast.warning("Por favor, preencha todos os campos obrigatórios!");
        return;
      }

      // Criar o payload para atualização
      const payload = {
        descricao: this.orderDescription,
        quantidade: this.orderQuantity,
        categoria: this.orderCategory,
        urgencia: this.orderUrgency,
        observacao: this.orderNotes,
        deliveryDate: this.orderDeliveryDate,
        sender: this.orderSender,
        setor: this.orderSenderSector,
        usuario_nome: this.userName || "Usuário do Sistema",
        status: this.orderStatus,
        orcamento_previsto: this.orderBudget,
        custo_real: this.orderRealCost,
        fornecedor: this.orderSupplier,
        observacao_orcamento: this.orderBudgetNotes
      };
      
      console.log("Pedido original:", this.pedido);
      console.log("Novos dados do pedido:", payload);
      
      // Gerar histórico de alterações
      this.gerarHistoricoAlteracoes(payload);
      
      try {
        // Enviar alterações com histórico
        const response = await axios.put(
          `${process.env.VUE_APP_API_URL}/pedidos/${this.pedido.id}/com-historico`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
              "Content-Type": "application/json",
            },
          }
        );
        
        console.log("Resposta do servidor:", response.data);

        // Mostrar notificação de sucesso
        toast.success("Pedido atualizado com sucesso!");
        
        // Emitir evento e fechar o modal
        this.$emit("update-order", { id: this.pedido.id, ...payload });
        this.closeForm();
      } catch (error) {
        console.error("Erro detalhado:", error.response?.data);
        toast.error(error.response?.data?.detail || "Erro ao atualizar o pedido. Verifique sua autenticação.");
        console.error("Erro ao atualizar pedido:", error.response ? error.response.data : error);
      }
    },
    gerarHistoricoAlteracoes(novosDados) {
      // Verificar alterações significativas comparando os dados do pedido original com os novos dados
      const registrosHistorico = [];
      
      // Verificar alteração na descrição
      if (novosDados.descricao !== this.pedido.descricao) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Descrição",
          valor_anterior: this.pedido.descricao || "Não definida",
          valor_novo: novosDados.descricao
        });
      }
      
      // Verificar alteração na data do pedido (apenas para admins)
      if (this.isAdmin && novosDados.deliveryDate !== this.pedido.deliveryDate) {
        // Formatar as datas para exibição
        const dataAnterior = this.formatarData(this.pedido.deliveryDate);
        const dataNova = this.formatarData(novosDados.deliveryDate);
        
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Data do Pedido",
          valor_anterior: dataAnterior || "Não definida",
          valor_novo: dataNova
        });
      }
      
      // Verificar alteração na quantidade
      if (novosDados.quantidade !== this.pedido.quantidade) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Quantidade",
          valor_anterior: String(this.pedido.quantidade || 0),
          valor_novo: String(novosDados.quantidade)
        });
      }
      
      // Verificar alteração na categoria
      if (novosDados.categoria !== this.pedido.categoria) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Categoria",
          valor_anterior: this.pedido.categoria || "Não definida",
          valor_novo: novosDados.categoria
        });
      }
      
      // Verificar alteração na urgência
      if (novosDados.urgencia !== this.pedido.urgencia) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Urgência",
          valor_anterior: this.pedido.urgencia || "Padrão",
          valor_novo: novosDados.urgencia
        });
      }
      
      // Verificar alteração no status
      if (novosDados.status !== this.pedido.status) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Status",
          valor_anterior: this.pedido.status || "Pendente",
          valor_novo: novosDados.status
        });
      }
      
      // Verificar alteração no orçamento previsto
      if (novosDados.orcamento_previsto !== this.pedido.orcamento_previsto) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Orçamento Previsto",
          valor_anterior: `R$ ${parseFloat(this.pedido.orcamento_previsto || 0).toFixed(2)}`,
          valor_novo: `R$ ${parseFloat(novosDados.orcamento_previsto).toFixed(2)}`
        });
      }
      
      // Verificar alteração no custo real
      if (novosDados.custo_real !== this.pedido.custo_real) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Custo Real",
          valor_anterior: `R$ ${parseFloat(this.pedido.custo_real || 0).toFixed(2)}`,
          valor_novo: `R$ ${parseFloat(novosDados.custo_real).toFixed(2)}`
        });
      }
      
      // Verificar alteração no fornecedor
      if (novosDados.fornecedor !== this.pedido.fornecedor) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Fornecedor",
          valor_anterior: this.pedido.fornecedor || "Não definido",
          valor_novo: novosDados.fornecedor || "Não definido"
        });
      }
      
      // Verificar alteração no setor do responsável
      if (novosDados.setor !== this.pedido.setor) {
        registrosHistorico.push({
          pedido_id: this.pedido.id,
          usuario_nome: this.userName,
          campo_alterado: "Setor do Responsável",
          valor_anterior: this.pedido.setor || "Não definido",
          valor_novo: novosDados.setor || "Não definido"
        });
      }
      
      // Adicionar o histórico ao payload se houver alterações
      if (registrosHistorico.length > 0) {
        novosDados.historico = registrosHistorico;
      }
    },
    closeForm() {
      this.$emit("close");
    },
    handleOverlayClick(event) {
      event.stopPropagation(); 
    },
    decrementQuantity() {
      this.orderQuantity--;
    },
    incrementQuantity() {
      this.orderQuantity++;
    },
    validateQuantity() {
      if (this.orderQuantity < 1) {
        this.validationErrors.quantity = "A quantidade deve ser maior que zero";
      } else {
        this.validationErrors.quantity = "";
      }
    },
    validateBudget() {
      if (this.orderBudget < 0) {
        this.validationErrors.budget = "O orçamento não pode ser negativo";
        this.orderBudget = 0;
      } else {
        this.validationErrors.budget = "";
      }
    },
    validateRealCost() {
      if (this.orderRealCost < 0) {
        this.validationErrors.realCost = "O custo real não pode ser negativo";
        this.orderRealCost = 0;
      } else {
        this.validationErrors.realCost = "";
      }
    },
    formatarData(data) {
      if (!data) return "N/A";
      
      try {
        const d = new Date(data);
        
        // Verificar se a data é válida
        if (isNaN(d.getTime())) {
          console.warn(`Data inválida: ${data}`);
          return 'Data inválida';
        }
        
        return d.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        });
      } catch (error) {
        console.error(`Erro ao formatar data: ${data}`, error);
        return 'Erro de formato';
      }
    }
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

/* Modal Overlay */
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
  transition: opacity 0.3s ease-in-out;
  overflow-y: auto;
  padding: 15px;
  box-sizing: border-box;
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 30px; 
  border-radius: 10px;
  width: 100%;
  max-width: 800px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  overflow-y: auto;
  max-height: 90vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

/* Cabeçalho do formulário */
.form-header {
  margin-bottom: 25px;
  border-bottom: 1px solid #333;
  padding-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

/* Título do formulário */
.form-header h2 {
  color: #ff6f61; 
  font-size: 1.4rem;
  margin: 0;
  display: flex;
  align-items: center;
}

.order-id {
  margin-left: 10px;
  background-color: #333;
  color: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

/* Informações do usuário */
.user-info {
  background-color: #333;
  padding: 5px 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.user-label {
  color: #999;
  margin-right: 5px;
}

.user-name {
  color: #ff6f61;
  font-weight: bold;
}

/* Grid para o formulário */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.full-width {
  grid-column: 1 / -1;
}

/* Estilo dos campos do formulário */
.form-group {
  margin-bottom: 15px; 
}

.form-group label {
  font-weight: bold;
  margin-bottom: 8px; 
  display: flex;
  align-items: center;
  color: #ff6f61; 
  font-size: 0.9rem;
}

.form-group label i {
  margin-right: 8px;
  font-size: 18px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px; 
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #333;
  color: #f5f5f5;
  font-size: 14px; 
  box-sizing: border-box;
  resize: vertical;
  text-transform: uppercase;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 111, 97, 0.2);
}

textarea {
  min-height: 90px; 
}

/* Estilo para validação de campos */
input.invalid,
select.invalid,
textarea.invalid {
  border-color: #e74c3c;
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
}

.error-message {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 5px;
}

/* Botões do formulário */
.form-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  gap: 15px;
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

button i {
  margin-right: 8px;
  font-size: 18px;
}

.submit-btn {
  background-color: #ff6f61;
  color: #1f1f1f;
}

.submit-btn:hover {
  background-color: #e05545;
}

.close-btn {
  background-color: transparent;
  color: #999;
  border: 1px solid #555;
}

.close-btn:hover {
  background-color: #333;
  color: #fff;
}

/* Quantidade Input Container */
.quantity-input-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  border: 1px solid #444;
  border-radius: 5px;
  overflow: hidden;
  background-color: #333;
}

.quantity-input-container input {
  border: none;
  text-align: center;
  width: 60%;
  padding: 12px 0;
  margin: 0;
  background-color: transparent;
}

.quantity-input-container input:focus {
  box-shadow: none;
  border: none;
  outline: none;
}

.quantity-btn {
  background-color: #444;
  border: none;
  color: #f5f5f5;
  cursor: pointer;
  padding: 12px 15px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.quantity-btn:hover:not(:disabled) {
  background-color: #555;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-note {
  font-size: 0.8rem;
  color: #999;
  margin-top: 5px;
}

/* Date Input Container */
.date-input-container {
  position: relative;
}

.date-input-container input[type="date"] {
  padding-right: 40px; /* Espaço para o ícone */
}

.date-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  pointer-events: none; /* Para não interferir com cliques no input */
}

/* Histórico de alterações */
.history-section {
  margin-top: 30px;
  border-top: 1px solid #333;
  padding-top: 20px;
}

.history-title {
  color: #ff6f61;
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.history-title i {
  margin-right: 8px;
}

.history-list {
  max-height: 200px;
  overflow-y: auto;
  background-color: #2a2a2a;
  border-radius: 5px;
  padding: 10px;
}

.history-item {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #444;
}

.history-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.history-date {
  font-size: 0.8rem;
  color: #999;
}

.history-user {
  font-size: 0.8rem;
  font-weight: bold;
  color: #ff6f61;
}

.history-content {
  font-size: 0.9rem;
}

.history-field {
  font-weight: bold;
  color: #f5f5f5;
}

.history-old-value {
  color: #e74c3c;
  text-decoration: line-through;
}

.history-new-value {
  color: #2ecc71;
}

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .order-form {
    max-width: 90%;
    padding: 25px;
  }
  
  .form-header h2 {
    font-size: 1.3rem;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .order-form {
    max-width: 95%;
    padding: 20px;
  }
  
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-info {
    margin-top: 10px;
  }
  
  .history-list {
    max-height: 150px;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .order-form {
    padding: 15px;
    max-width: 100%;
  }
  
  .form-header h2 {
    font-size: 1.2rem;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  button {
    margin-top: 10px;
  }
}

.section-title {
  margin: 10px 0;
  color: #eee;
  font-size: 1.2em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.separator {
  margin: 20px 0;
  border-top: 1px solid #444;
  padding-top: 15px;
  width: 100%;
}

.financial-status {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  margin-top: 10px;
  gap: 15px;
}

.status-icon {
  font-size: 32px;
}

.status-info h4 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.status-info p {
  margin: 0;
  font-size: 16px;
}

.status-under-budget {
  background-color: rgba(46, 204, 113, 0.2);
  border: 1px solid #2ecc71;
  color: #2ecc71;
}

.status-over-budget {
  background-color: rgba(231, 76, 60, 0.2);
  border: 1px solid #e74c3c;
  color: #e74c3c;
}

.status-on-budget {
  background-color: rgba(52, 152, 219, 0.2);
  border: 1px solid #3498db;
  color: #3498db;
}
</style>
