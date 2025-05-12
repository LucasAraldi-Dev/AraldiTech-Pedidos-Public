<template>
  <main class="help-page">
    <section class="help-section">
      <div class="logo-container">
        <img src="../assets/logo.png" alt="AraldiTech" class="logo" onerror="this.src='favicon.ico'">
      </div>
      
      <h1>Central de Ajuda</h1>
      <p>Encontre as respostas para suas dúvidas mais frequentes</p>
      
      <!-- Botão para iniciar/rever o tutorial (apenas para usuários comuns) -->
      <div v-if="isCommonUser" class="tutorial-actions">
        <button @click="startTutorial" class="btn-tutorial">
          <span class="tutorial-icon">🎓</span>
          Rever Tutorial Interativo
        </button>
        <p class="tutorial-tip">O tutorial irá mostrar passo a passo as principais funcionalidades do sistema.</p>
      </div>
      
      <div class="help-container">
        <div class="faq-section">
          <h2>Perguntas Frequentes</h2>
          
          <div class="accordion">
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(0)">
                <span>Como criar um novo pedido?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 0 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 0 }">
                <p>Para criar um novo pedido, acesse o painel principal e clique no botão "Criar Pedido". Preencha todos os campos obrigatórios no formulário e clique em "Salvar".</p>
              </div>
            </div>
            
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(1)">
                <span>Como editar um pedido existente?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 1 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 1 }">
                <p>Para editar um pedido existente, acesse a lista de pedidos, localize o pedido desejado e clique no ícone de edição. Faça as alterações necessárias no formulário e clique em "Salvar".</p>
              </div>
            </div>
            
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(2)">
                <span>Como filtrar pedidos por setor?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 2 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 2 }">
                <p>Use o menu suspenso de filtros na parte superior da lista de pedidos. Selecione o setor desejado e a lista será automaticamente atualizada para mostrar apenas os pedidos daquele setor.</p>
              </div>
            </div>
            
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(3)">
                <span>Como acessar o relatório financeiro?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 3 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 3 }">
                <p>O relatório financeiro está disponível apenas para administradores e gestores. Acesse o menu principal e clique em "Relatório Financeiro" para visualizar os dados.</p>
              </div>
            </div>
            
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(4)">
                <span>Como concluir um pedido?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 4 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 4 }">
                <p>Para marcar um pedido como concluído, abra a consulta do pedido desejado e clique no botão "Concluir Pedido". Confirme a ação no modal que será exibido. Uma vez concluído, o pedido não poderá mais ser editado.</p>
              </div>
            </div>
            
            <div class="accordion-item">
              <div class="accordion-header" @click="toggleAccordion(5)">
                <span>Como visualizar o histórico de edições?</span>
                <div class="accordion-icon" :class="{ 'active': activeAccordion === 5 }">
                  <i class="fas fa-chevron-down"></i>
                </div>
              </div>
              <div class="accordion-content" :class="{ 'active': activeAccordion === 5 }">
                <p>Para visualizar o histórico de edições de um pedido, acesse o menu de pedidos, encontre o pedido desejado e clique no ícone de histórico. Será exibido um registro de todas as alterações realizadas, incluindo a data, hora e usuário responsável.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="support-area">
        <h3>Precisa de mais ajuda?</h3>
        <router-link to="/contato" class="support-button">
          <i class="fas fa-headset"></i> Contatar Suporte Técnico
        </router-link>
      </div>
      
      <div class="action-buttons">
        <router-link to="/" class="btn-secondary">Voltar para Home</router-link>
        <router-link to="/menu" class="btn-primary">Ir para Menu</router-link>
      </div>
    </section>
    
    <!-- Modal de Tutorial -->
    <TutorialModal
      v-if="isTutorialOpen"
      :isOpen="isTutorialOpen"
      @close="closeTutorial"
    />
  </main>
</template>

<script>
import { ref, computed } from 'vue';
import TutorialModal from '@/components/TutorialModal.vue';

export default {
  name: 'AppAjuda',
  components: {
    TutorialModal
  },
  setup() {
    const activeAccordion = ref(null);
    const isTutorialOpen = ref(false);
    
    // Verificar se o usuário é do tipo "comum"
    const isCommonUser = computed(() => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        return user && user.tipo_usuario === 'comum';
      } catch (error) {
        console.error("Erro ao verificar tipo de usuário:", error);
        return false;
      }
    });
    
    const toggleAccordion = (index) => {
      activeAccordion.value = activeAccordion.value === index ? null : index;
    };
    
    const startTutorial = () => {
      isTutorialOpen.value = true;
    };
    
    const closeTutorial = () => {
      isTutorialOpen.value = false;
    };
    
    return {
      activeAccordion,
      toggleAccordion,
      isTutorialOpen,
      startTutorial,
      closeTutorial,
      isCommonUser
    };
  }
}
</script>

<style scoped>
/* Componentes específicos desta página */
.logo-container {
  margin-bottom: 20px;
}

.logo {
  max-width: 150px;
  height: auto;
}

.help-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Sobrescrever estilos específicos */
p {
  text-align: center;
}

.help-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-bottom: 30px;
  max-width: 800px;
}

.faq-section {
  width: 100%;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #fff;
  text-align: center;
}

.accordion {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.accordion-item {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.accordion-header {
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.accordion-header:hover {
  background: rgba(255, 255, 255, 0.05);
}

.accordion-header span {
  font-size: 16px;
  font-weight: 600;
  color: #eee;
}

.accordion-icon {
  width: 24px;
  height: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease;
}

.accordion-icon.active {
  transform: rotate(180deg);
}

.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.accordion-content.active {
  max-height: 200px;
}

.accordion-content p {
  padding: 0 20px 20px;
  margin: 0;
  font-size: 15px;
  text-align: left;
  color: #aaa;
}

.support-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin: 30px 0;
}

.support-area h3 {
  font-size: 20px;
  color: #eee;
  margin: 0;
}

.support-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 25px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.support-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

.support-button i {
  font-size: 18px;
  color: #66ccff;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn-primary {
  padding: 12px 24px;
  background-color: #66ccff;
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #99ddff;
  transform: translateY(-2px);
}

.btn-secondary {
  padding: 12px 24px;
  background-color: transparent;
  color: #fff;
  border: 1px solid #666;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Estilos para o botão de tutorial */
.tutorial-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
  padding: 20px;
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.btn-tutorial {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background-color: #5cb85c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-tutorial:hover {
  background-color: #4cae4c;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.tutorial-icon {
  font-size: 20px;
}

.tutorial-tip {
  margin-top: 15px;
  font-size: 14px;
  color: #aaa;
  text-align: center;
}

/* Responsividade */
@media (max-width: 1024px) {
  .help-section {
    padding: 30px 20px;
  }
  
  .help-container {
    max-width: 700px;
  }
}

@media (max-width: 768px) {
  .accordion-header {
    padding: 15px;
  }
  
  .accordion-content p {
    padding: 0 15px 15px;
    font-size: 14px;
  }
  
  .support-button {
    padding: 12px 20px;
  }
}

@media (max-width: 480px) {
  .help-section {
    padding: 20px 15px;
  }
  
  .accordion-header span {
    font-size: 14px;
  }
  
  h2 {
    font-size: 20px;
  }
  
  .support-area h3 {
    font-size: 18px;
  }
  
  .support-button {
    padding: 10px 16px;
    font-size: 14px;
  }
  
  .support-button i {
    font-size: 16px;
  }
}
</style>
