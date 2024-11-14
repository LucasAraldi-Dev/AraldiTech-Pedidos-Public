<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="print-modal" @click.stop ref="orderContent">
      <div class="modal-header">
        <img src="@/assets/logo.png" alt="Logo" class="logo" />
        <h2>DETALHES DO PEDIDO</h2>
      </div>

      <div class="order-details">
        <p><strong>Descrição:</strong> {{ pedido.descricao }}</p>
        <p><strong>Quantidade:</strong> {{ pedido.quantidade }}</p>
        <p><strong>Urgência:</strong> {{ pedido.urgencia ? "Sim" : "Não" }}</p>
        <p><strong>Data de Entrega:</strong> {{ pedido.deliveryDate }}</p>
        <p><strong>Observação:</strong> {{ pedido.observacao }}</p>
        <p><strong>Responsável:</strong> {{ pedido.sender }}</p>
        <div v-if="pedido.anexo">
          <p><strong>Anexo:</strong></p>
          <img :src="'data:image/png;base64,' + pedido.anexo" alt="Anexo" class="order-attachment" />
        </div>
      </div>

      <button @click="printOrder">IMPRIMIR</button>
      <button class="close-btn" @click="closeModal">FECHAR</button>
    </div>
  </div>
</template>

<script>
import html2canvas from "html2canvas";
import jsPDF from "jspdf";

export default {
  props: {
    isOpen: Boolean,
    pedido: Object, 
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    async printOrder() {
      const orderElement = this.$refs.orderContent; 
      if (orderElement) {
        // Captura do conteúdo com html2canvas
        const canvas = await html2canvas(orderElement, {
          useCORS: true, // Tentar carregar imagens de outros domínios
          scrollX: 0,
          scrollY: -window.scrollY, // Ajuste para capturar a tela inteira
        });
        
        // Converte o conteúdo para um formato de imagem
        const imgData = canvas.toDataURL("image/png");

        // Cria o PDF com jsPDF
        const pdf = new jsPDF();
        pdf.addImage(imgData, "PNG", 10, 10, 180, 0); 
        pdf.save("pedido.pdf"); // Salva o PDF com o nome "pedido.pdf"
      }
    },
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
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  box-sizing: border-box;
  text-align: left;
  position: relative;
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
  width: 320px; 
  margin-bottom: 10px;
}

.order-details p {
  margin-bottom: 15px;
  font-size: 1rem;
}

.order-details strong {
  color: #ff6f61;
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

button:hover {
  background-color: #ff6f61;
  color: #1f1f1f;
}

.order-attachment {
  margin-top: 15px;
  max-width: 100%;
  border-radius: 5px;
}

@media (max-width: 768px) {
  .print-modal {
    width: 90%;
    max-width: 400px;
  }
}
</style>
