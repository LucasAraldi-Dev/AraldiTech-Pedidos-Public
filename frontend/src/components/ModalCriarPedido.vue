<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeForm">
    <div class="order-form" @click.stop>
      <h2>ADICIONAR PEDIDO</h2>

      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

      <form v-show="!successMessage" @submit.prevent="handleCreateOrder">
        
        <div class="form-group">
          <label for="orderDescription">DESCRIÇÃO DO PEDIDO</label>
          <textarea id="orderDescription" v-model="orderDescription" placeholder="DESCRIÇÃO DO PEDIDO" required></textarea>
        </div>

        
        <div class="form-group">
          <label for="orderQuantity">QUANTIDADE SOLICITADA</label>
          <input id="orderQuantity" type="number" v-model="orderQuantity" required />
        </div>

        
        <div class="form-group">
          <label for="orderUrgency">URGÊNCIA</label>
          <select v-model="orderUrgency" required>
            <option :value="true">SIM</option>
            <option :value="false">NÃO</option>
          </select>
        </div>

        
        <div class="form-group">
          <label for="orderDeliveryDate">DATA DE ENTREGA</label>
          <input id="orderDeliveryDate" type="date" v-model="orderDeliveryDate" required />
        </div>

        
        <div class="form-group">
          <label for="orderNotes">OBSERVAÇÃO</label>
          <textarea id="orderNotes" v-model="orderNotes" placeholder="OBSERVAÇÃO"></textarea>
        </div>

        
        <div class="form-group">
          <label for="orderFile">ANEXO (IMAGEM/ARQUIVO)</label>
          <input id="orderFile" type="file" @change="handleFileUpload" />
        </div>

        
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
      orderNotes: "",
      orderUrgency: false,
      orderDeliveryDate: "",
      orderSender: "",
      orderFile: null,
      orderFileBase64: "",
      userEmail: null,
      successMessage: "", 
    };
  },
  mounted() {
    this.userEmail = localStorage.getItem("user_name");
  },
  methods: {
    async handleCreateOrder() {
      if (!this.userEmail) {
        console.error("Usuário não autenticado.");
        return;
      }

      const token = localStorage.getItem("access_token");

      const payload = {
        descricao: this.orderDescription,
        quantidade: this.orderQuantity,
        observacao: this.orderNotes,
        urgencia: this.orderUrgency,
        deliveryDate: this.orderDeliveryDate,
        sender: this.orderSender,
        usuario_id: this.userEmail,
        anexo: this.orderFileBase64,
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

        
        this.successMessage = `PEDIDO Nº ${response.data.id} foi criado com sucesso!`;

        
        this.$emit("create-order", response.data);

        
        setTimeout(() => {
          this.resetForm();
        }, 2000);
      } catch (error) {
        console.error("Erro ao criar pedido:", error.response ? error.response.data : error);
      }
    },
    resetForm() {
      this.orderDescription = "";
      this.orderQuantity = 0;
      this.orderNotes = "";
      this.orderUrgency = false;
      this.orderDeliveryDate = "";
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
      if (file) {
        const reader = new FileReader();
        reader.onloadend = () => {
          this.orderFileBase64 = reader.result.split(",")[1];
        };
        reader.readAsDataURL(file);
      }
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
}

/* Estilo do Formulário */
.order-form {
  background-color: #1f1f1f; 
  color: #f5f5f5;
  padding: 25px; 
  border-radius: 10px;
  width: 100%;
  max-width: 400px; 
  box-sizing: border-box;
  position: relative;
  text-transform: none;
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