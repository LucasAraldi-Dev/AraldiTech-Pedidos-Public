<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="edit-order-form" @click.stop>
      <h2>EDITAR PEDIDO</h2>

      
      <form @submit.prevent="submitForm">
        
        <div class="form-group">
          <label for="descricao">Descrição</label>
          <input type="text" id="descricao" v-model="editedOrder.descricao" required />
        </div>

        
        <div class="form-group">
          <label for="observacao">Observação</label>
          <textarea id="observacao" v-model="editedOrder.observacao"></textarea>
        </div>

        
        <div class="form-group">
          <label for="quantidade">Quantidade</label>
          <input type="number" id="quantidade" v-model="editedOrder.quantidade" required />
        </div>

        
        <div class="form-group">
          <label for="dataEntrega">Data de Entrega</label>
          <input type="date" id="dataEntrega" v-model="editedOrder.dataEntrega" required />
        </div>

        
        <div class="form-group">
          <label for="responsavel">Responsável pela Compra</label>
          <input type="text" id="responsavel" v-model="editedOrder.responsavel" required />
        </div>

        
        <div class="form-buttons">
          <button type="submit" class="save-btn">Salvar</button>
          <button type="button" class="cancel-btn" @click="closeModal">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    order: Object, 
    onClose: Function,
    onSave: Function, 
  },
  data() {
    return {
      editedOrder: {
        id: this.order.id || '',
        descricao: this.order.descricao || '',
        observacao: this.order.observacao || '',
        quantidade: this.order.quantidade || '',
        dataEntrega: this.order.dataEntrega || '',
        responsavel: this.order.responsavel || ''
      }
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    submitForm() {
      
      if (this.editedOrder.descricao && this.editedOrder.quantidade) {
        this.$emit('save', this.editedOrder);
        this.closeModal();
      } else {
        alert("Preencha os campos obrigatórios.");
      }
    }
  }
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
</style>
