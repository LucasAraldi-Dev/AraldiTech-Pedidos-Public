<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="edit-order-form" @click.stop>
      <h2>EDITAR PEDIDO</h2>

      <form @submit.prevent="submitForm">
        <!-- Status -->
        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="editedOrder.status" required>
            <option value="Pendente">Pendente</option>
            <option value="Concluído">Concluído</option>
            <option value="Cancelado">Cancelado</option>
          </select>
        </div>

        <!-- Descrição -->
        <div class="form-group">
          <label for="descricao">Descrição</label>
          <input type="text" id="descricao" v-model="editedOrder.descricao" required />
        </div>

        <!-- Observação -->
        <div class="form-group">
          <label for="observacao">Observação</label>
          <textarea id="observacao" v-model="editedOrder.observacao"></textarea>
        </div>

        <!-- Quantidade -->
        <div class="form-group">
          <label for="quantidade">Quantidade</label>
          <input type="number" id="quantidade" v-model="editedOrder.quantidade" required />
        </div>

        <!-- Urgência -->
        <div class="form-group">
          <label for="urgencia">Urgente</label>
          <select id="urgencia" v-model="editedOrder.urgencia" required>
            <option :value="true">Sim</option>
            <option :value="false">Não</option>
          </select>
        </div>

        <!-- Data de Entrega -->
        <div class="form-group">
          <label for="deliveryDate">Data de Entrega</label>
          <input
            type="text"
            id="deliveryDate"
            v-model="editedOrder.deliveryDate"
            placeholder="dd-MM-yyyy"
            pattern="\d{2}-\d{2}-\d{4}"
            required
          />
        </div>

        <!-- Responsável pela Compra -->
        <div class="form-group">
          <label for="sender">Responsável pela Compra</label>
          <input type="text" id="sender" v-model="editedOrder.sender" required />
        </div>

        <!-- Botões -->
        <div class="form-buttons">
          <button type="submit" class="save-btn">Salvar</button>
          <button type="button" class="cancel-btn" @click="closeModal">Cancelar</button>
        </div>

        <!-- Mensagem de sucesso -->
        <p v-if="showSuccessMessage" class="success-message">Pedido atualizado com sucesso!</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    order: Object,
  },
  data() {
    return {
      editedOrder: {
        id: this.order?.id || null,
        descricao: this.order?.descricao || "",
        quantidade: this.order?.quantidade || 0,
        observacao: this.order?.observacao || "",
        urgencia: this.order?.urgencia ?? false, 
        deliveryDate: this.formatToDDMMYYYY(this.order?.deliveryDate) || "",
        sender: this.order?.sender || "",
        status: this.order?.status || "Pendente",
        anexo: this.order?.anexo || null,
      },
      showSuccessMessage: false,
    };
  },
  watch: {
    order: {
      immediate: true,
      handler(newOrder) {
        this.editedOrder = {
          ...newOrder,
          deliveryDate: this.formatToDDMMYYYY(newOrder?.deliveryDate),
        };
      },
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
      this.showSuccessMessage = false;
    },
    submitForm() {
      if (this.editedOrder.descricao && this.editedOrder.quantidade && this.editedOrder.deliveryDate) {
        const orderToSave = {
          ...this.editedOrder,
          deliveryDate: this.formatToYYYYMMDD(this.editedOrder.deliveryDate),
        };
        this.$emit("save", orderToSave);
        this.showSuccessMessage = true;
      } else {
        alert("Preencha todos os campos obrigatórios.");
      }
    },
    formatToDDMMYYYY(date) {
      if (!date) return "";
      const d = new Date(date);
      const day = String(d.getDate()).padStart(2, "0");
      const month = String(d.getMonth() + 1).padStart(2, "0");
      const year = d.getFullYear();
      return `${day}-${month}-${year}`;
    },
    formatToYYYYMMDD(date) {
      if (!date) return "";
      const [day, month, year] = date.split("-");
      return `${year}-${month}-${day}`;
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
}

.edit-order-form {
  background-color: #1f1f1f;
  color: white;
  padding: 25px;
  border-radius: 10px;
  width: 100%;
  max-width: 600px;
  box-sizing: border-box;
}

.edit-order-form h2 {
  text-align: center;
  color: #ff6f61;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 1rem;
  color: #f5f5f5;
}

input, textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  background-color: #333;
  color: #f5f5f5;
}

textarea {
  resize: vertical;
  height: 100px;
}

button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.save-btn {
  background-color: #ff6f61;
  color: white;
  border: none;
  margin-right: 10px;
}

.cancel-btn {
  background-color: #4f5b62;
  color: white;
  border: none;
}

.save-btn:hover {
  background-color: #e05545;
}

.cancel-btn:hover {
  background-color: #3b484d;
}

select {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  background-color: #333;
  color: #f5f5f5;
}

.success-message {
  color: #28a745;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

</style>
