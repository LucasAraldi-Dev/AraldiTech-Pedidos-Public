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
        <p><strong>DESCRIÇÃO:</strong> {{ pedido.descricao.toUpperCase() }}</p>
        <p><strong>QUANTIDADE:</strong> {{ pedido.quantidade }}</p>
        <p><strong>URGÊNCIA:</strong> {{ pedido.urgencia.toUpperCase() }}</p>
        <p><strong>CATEGORIA:</strong> {{ pedido.categoria.toUpperCase() }}</p>
        <p><strong>DATA DE ENTREGA:</strong> {{ formatDate(pedido.deliveryDate).toUpperCase() }}</p>
        <p><strong>OBSERVAÇÃO:</strong> {{ pedido.observacao ? pedido.observacao.toUpperCase() : "NENHUMA" }}</p>
        <p><strong>RESPONSÁVEL:</strong> {{ pedido.sender.toUpperCase() }}</p>
        <div v-if="pedido.anexo">
          <p><strong>ANEXO:</strong></p>
          <img :src="'data:image/png;base64,' + pedido.anexo" alt="ANEXO" class="order-attachment" />
        </div>
      </div>

      <!-- Botões -->
      <button @click="generateImage">GERAR IMAGEM</button>
      <button class="close-btn" @click="closeModal">FECHAR</button>
    </div>
  </div>
</template>

<script>
import html2canvas from "html2canvas";

export default {
  props: {
    isOpen: Boolean,
    pedido: Object,
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    formatDate(date) {
      const d = new Date(date);
      return d.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      });
    },
    async generateImage() {
      const orderElement = this.$refs.orderContent;
      const printButton = this.$el.querySelector('button'); 
      const closeButton = this.$el.querySelectorAll('button')[1]; 

      if (orderElement) {
        // Ocultar os botões antes de gerar a imagem
        if (printButton && closeButton) {
          printButton.classList.add('hidden');
          closeButton.classList.add('hidden');
        }

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
        link.download = 'pedido.png'; 
        link.click();

        // Restaurar a visibilidade dos botões
        if (printButton && closeButton) {
          printButton.classList.remove('hidden');
          closeButton.classList.remove('hidden');
        }
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
  border-radius: 0px;
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

.hidden {
  display: none;
}

@media (max-width: 768px) {
  .print-modal {
    width: 80%;
    max-width: 400px;
  }
}
</style>
