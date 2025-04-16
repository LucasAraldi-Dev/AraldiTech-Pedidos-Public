<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="edit-form" @click.stop>
      <h2>EDITAR PEDIDO</h2>
      <form @submit.prevent="saveOrder">
        <!-- Descrição -->
        <div class="form-group">
          <label for="descricao">Descrição</label>
          <input type="text" id="descricao" v-model="editedOrder.descricao" required />
        </div>

        <!-- Quantidade -->
        <div class="form-group">
          <label for="quantidade">Quantidade</label>
          <input type="number" id="quantidade" v-model="editedOrder.quantidade" required />
        </div>

        <!-- Urgência -->
        <div class="form-group">
          <label for="urgencia">Urgência</label>
          <select id="urgencia" v-model="editedOrder.urgencia">
            <option value="Padrão">Padrão</option>
            <option value="Urgente">Urgente</option>
            <option value="Crítico">Crítico</option>
          </select>
        </div>

        <!-- Data de Entrega -->
        <div class="form-group">
          <label for="deliveryDate">Data de Entrega</label>
          <input 
            type="date" 
            id="deliveryDate" 
            v-model="editedOrder.deliveryDate" 
            required 
          />
        </div>

        <!-- Observação -->
        <div class="form-group">
          <label for="observacao">Observação</label>
          <textarea id="observacao" v-model="editedOrder.observacao"></textarea>
        </div>

        <!-- Botões -->
        <div class="form-buttons">
          <button type="submit" class="save-btn">Salvar</button>
          <button type="button" class="cancel-btn" @click="closeForm">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from 'vue-toastification';  // Importando Vue Toastification

export default {
  props: {
    isOpen: Boolean,
    order: Object,
  },
  data() {
    return {
      editedOrder: { ...this.order },
    };
  },
  watch: {
    order: {
      immediate: true,
      handler(newOrder) {
        this.editedOrder = { ...newOrder };
      },
    },
  },
  methods: {
    async saveOrder() {
      const toast = useToast();  // Instanciando o Toastification
      try {
        const payload = {
          descricao: this.editedOrder.descricao,
          quantidade: this.editedOrder.quantidade,
          urgencia: this.editedOrder.urgencia,
          deliveryDate: this.editedOrder.deliveryDate, // ISO format
          observacao: this.editedOrder.observacao,
        };

        const response = await axios.put(
          `${process.env.VUE_APP_API_URL}/pedidos/${this.editedOrder.id}`,
          payload,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              "Content-Type": "application/json",
            },
          }
        );

        this.$emit("order-updated", response.data);

        // Notificar sucesso
        toast.success("Pedido atualizado com sucesso!");
        this.closeForm();
      } catch (error) {
        console.error("Erro ao salvar pedido:", error.response?.data || error);

        // Notificar erro
        toast.error("Erro ao salvar as alterações do pedido.");
      }
    },
    closeForm() {
      this.$emit("close");
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

.edit-form {
  background-color: #1f1f1f;
  color: white;
  padding: 25px;
  border-radius: 10px;
  width: 100%;
  max-width: 600px;
  box-sizing: border-box;
}

.edit-form h2 {
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

input,
textarea,
select {
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

.form-buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
}

.save-btn {
  background-color: #ff6f61;
  color: white;
}

.cancel-btn {
  background-color: #4f5b62;
  color: white;
}

.save-btn:hover {
  background-color: #e05545;
}

.cancel-btn:hover {
  background-color: #3b484d;
}

/* Responsividade para diferentes dispositivos */
/* Tablets e telas menores (1024x768) */
@media (max-width: 1024px) {
  .edit-form {
    max-width: 90%;
    padding: 25px;
  }
  
  .edit-form h2 {
    font-size: 1.8rem;
  }
  
  input,
  textarea,
  select {
    padding: 10px;
  }
}

/* Tablets e dispositivos médios */
@media (max-width: 768px) {
  .edit-form {
    max-width: 90%;
    padding: 20px;
  }
  
  .edit-form h2 {
    font-size: 1.6rem;
    margin-bottom: 15px;
  }
  
  .form-group {
    margin-bottom: 12px;
  }
  
  label {
    font-size: 0.9rem;
    margin-bottom: 5px;
  }
  
  input,
  textarea,
  select {
    padding: 10px;
    font-size: 0.9rem;
  }
  
  textarea {
    height: 80px;
  }
  
  button {
    padding: 10px 15px;
    font-size: 0.9rem;
  }
}

/* Dispositivos móveis */
@media (max-width: 480px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .edit-form {
    padding: 15px;
    max-width: 95%;
  }
  
  .edit-form h2 {
    font-size: 1.4rem;
    margin-bottom: 12px;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  label {
    font-size: 0.85rem;
  }
  
  input,
  textarea,
  select {
    padding: 8px;
    font-size: 0.85rem;
  }
  
  textarea {
    height: 70px;
  }
  
  .form-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    font-size: 0.85rem;
  }
}
</style>
