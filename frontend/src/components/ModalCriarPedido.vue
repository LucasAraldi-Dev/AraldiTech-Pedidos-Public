<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleOverlayClick">
    <div class="order-form" @click.stop>
      <h2>ADICIONAR PEDIDO</h2>

      <form v-show="!successMessage" @submit.prevent="handleCreateOrder">
        
        <!-- Descrição do Pedido -->
        <div class="form-group">
          <label for="orderDescription">DESCRIÇÃO DO PEDIDO</label>
          <textarea
            id="orderDescription"
            v-model="orderDescription"
            placeholder="DESCRIÇÃO DO PEDIDO"
            required
          ></textarea>
        </div>

        <!-- Quantidade Solicitada -->
        <div class="form-group">
          <label for="orderQuantity">QUANTIDADE SOLICITADA</label>
          <input id="orderQuantity" type="number" v-model="orderQuantity" required />
        </div>

        <!-- Categoria do Pedido -->
        <div class="form-group">
          <label for="orderCategory">CATEGORIA</label>
          <select id="orderCategory" v-model="orderCategory" required>
            <option value="" disabled selected>SELECIONE A CATEGORIA</option>
            <option value="Matérias-primas">Matérias-primas</option>
            <option value="Equipamentos e Máquinas">Equipamentos e Máquinas</option>
            <option value="Peças de Reposição">Peças de Reposição</option>
            <option value="Serviços">Serviços</option>
            <option value="Mercadorias diversas">Mercadorias diversas</option>
          </select>
        </div>

        <!-- Urgência -->
        <div class="form-group">
          <label for="orderUrgency">URGÊNCIA</label>
          <select id="orderUrgency" v-model="orderUrgency" required>
            <option value="Padrão">Padrão</option>
            <option value="Urgente">Urgente</option>
            <option value="Crítico">Crítico</option>
          </select>
        </div>

        <!-- Data de Entrega -->
        <div class="form-group">
          <label for="orderDeliveryDate">DATA DE ENTREGA</label>
          <input id="orderDeliveryDate" type="date" v-model="orderDeliveryDate" required />
        </div>

        <!-- Observações -->
        <div class="form-group">
          <label for="orderNotes">OBSERVAÇÃO</label>
          <textarea
            id="orderNotes"
            v-model="orderNotes"
            placeholder="OBSERVAÇÃO"
          ></textarea>
        </div>

        <!-- Anexo -->
        <div class="form-group">
          <label for="orderFile">ANEXO (IMAGEM/ARQUIVO)</label>
          <input id="orderFile" type="file" @change="handleFileUpload" />
        </div>

        <!-- Responsável pela Compra -->
        <div class="form-group">
          <label for="orderSender">RESPONSÁVEL PELA COMPRA</label>
          <input id="orderSender" type="text" v-model="orderSender" required />
        </div>

        <button type="submit">ENVIAR PEDIDO</button>
      </form>

      <button v-show="!successMessage" class="close-btn" @click="closeForm">FECHAR</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    isOpen: Boolean,
    onClose: Function,
  },
  data() {
    return {
      orderDescription: "",
      orderQuantity: 0,
      orderCategory: "", 
      orderUrgency: "Padrão", 
      orderDeliveryDate: "",
      orderNotes: "",
      orderSender: "",
      orderFile: null,
      orderFileBase64: "",
      userEmail: null,
      successMessage: "",
    };
  },
  mounted() {
    this.userEmail = localStorage.getItem("user_email"); 
    this.userName = localStorage.getItem("user_name"); 
    this.token = localStorage.getItem("access_token");
},
  methods: {
    async handleCreateOrder() {
      if (!this.orderFileBase64 && this.orderFile) {
        alert("Aguarde o processamento do arquivo antes de enviar o pedido.");
        return;
      }
      if (!this.userEmail) {
        console.error("Usuário não autenticado.");
        return;
      }
      if (!this.orderDescription || !this.orderQuantity || !this.orderSender || !this.orderCategory) {
        alert("Por favor, preencha todos os campos obrigatórios!");
        return;
      }

      const token = localStorage.getItem("access_token");

      const payload = {
    descricao: this.orderDescription,
    quantidade: this.orderQuantity,
    categoria: this.orderCategory,
    urgencia: this.orderUrgency,
    observacao: this.orderNotes,
    deliveryDate: this.orderDeliveryDate,
    sender: this.orderSender,
    usuario_nome: this.userName,  
    file: this.orderFileBase64,
    status: "Pendente",
};

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/pedidos/`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.$emit("create-order", response.data);
        this.$emit("open-print-modal", response.data);

        this.resetForm();
      } catch (error) {
        console.error("Erro ao criar pedido:", error.response ? error.response.data : error);
      }
    },
    resetForm() {
      this.orderDescription = "";
      this.orderQuantity = 0;
      this.orderCategory = "";
      this.orderUrgency = "Padrão";
      this.orderDeliveryDate = "";
      this.orderNotes = "";
      this.orderSender = "";
      this.orderFile = null;
      this.orderFileBase64 = "";
      this.successMessage = "";
    },
    closeForm() {
      this.$emit("close");
    },
    handleFileUpload(event) {
  const file = event.target.files[0];

  if (!file) {
    console.error("Nenhum arquivo selecionado.");
    return;
  }

  console.log("Arquivo selecionado:", file);

  const reader = new FileReader();

  reader.onloadend = () => {
    const result = reader.result;
    console.log("FileReader resultado bruto:", result);

    // Garante que só pega a parte Base64 (removendo o prefixo data:image/png;base64,)
    if (result.includes(",")) {
      this.orderFileBase64 = result.split(",")[1];
    } else {
      this.orderFileBase64 = result;
    }

    console.log("Base64 gerado:", this.orderFileBase64);
  };

  reader.onerror = (error) => {
    console.error("Erro ao ler o arquivo:", error);
  };

  reader.readAsDataURL(file);
},
    handleOverlayClick(event) {
      event.stopPropagation(); 
    },
  },
};
</script>

<style scoped>
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
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 30px; 
  border-radius: 10px;
  width: 100%;
  max-width: 500px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
  overflow-y: auto;

}

/* Título do formulário */
.order-form h2 {
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.4rem;
  color: #ff6f61; 
}

/* Mensagem de sucesso */
.success-message {
  color: #28a745;
  font-weight: bold;
  margin-bottom: 15px;
  text-align: center;
}

/* Estilo dos campos do formulário - EDITAR DEPOIS  */
.form-group {
  margin-bottom: 15px; 
}

.form-group label {
  font-weight: bold;
  margin-bottom: 8px; 
  display: inline-block;
  color: #ff6f61; 
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px; 
  border-radius: 5px;
  border: none;
  background-color: #333;
  color: #f5f5f5;
  font-size: 14px; 
  box-sizing: border-box;
  resize: vertical;
  text-transform: uppercase;
}

textarea {
  min-height: 90px; 
}

/* Botão enviar */
button[type="submit"] {
  padding: 12px 20px;
  background-color: #ff6f61;
  color: #1f1f1f;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-top: 20px;
  font-weight: bold;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #e05545;
}

button[type="submit"]:focus {
  outline: none;
}

/* Botão para fechar */
.close-btn {
  padding: 12px 20px;
  background-color: transparent;
  color: #ff6f61;
  border: 2px solid #ff6f61;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #ff6f61;
  color: #1f1f1f;
}

.close-btn:focus {
  outline: none;
}

</style>
