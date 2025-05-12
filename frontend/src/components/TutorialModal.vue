<template>
  <Teleport to="body">
    <div v-if="isOpen" class="tutorial-modal-overlay" @click="handleOverlayClick">
      <div class="tutorial-modal" @click.stop>
        <div class="tutorial-modal-header">
          <h2>Tutorial do Sistema</h2>
          <div class="tutorial-actions">
            <button @click="skipTutorial" class="tutorial-skip-btn">Pular Tutorial</button>
          </div>
        </div>
        
        <div class="tutorial-content">
          <div class="tutorial-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${(currentStep / tutorialSteps.length) * 100}%` }"></div>
            </div>
            <div class="progress-text">{{ currentStep }} de {{ tutorialSteps.length }}</div>
          </div>
          
          <div class="tutorial-step">
            <div class="tutorial-illustration">
              <div class="tutorial-image" :class="'tutorial-image-' + currentStep">
                <!-- Simulação visual da interface -->
                <div v-if="currentStep === 1" class="tutorial-menu-simulation">
                  <div class="tutorial-sidebar">
                    <div class="tutorial-logo"></div>
                    <div class="tutorial-menu-button active">Criar Pedido</div>
                    <div class="tutorial-menu-button">Consultar Pedidos</div>
                    <div class="tutorial-menu-button">Ajuda</div>
                    <div class="tutorial-menu-button logout">Sair</div>
                  </div>
                  <div class="tutorial-content-area">
                    <div class="tutorial-welcome">
                      <div class="tutorial-welcome-icon"></div>
                      <div class="tutorial-welcome-text">Bem-vindo ao Sistema de Pedidos</div>
                    </div>
                  </div>
                </div>
                
                <div v-if="currentStep === 2" class="tutorial-pedido-simulation">
                  <div class="tutorial-modal-header-sim">Criar Novo Pedido</div>
                  <div class="tutorial-form">
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Produto</div>
                      <div class="tutorial-form-field"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Quantidade</div>
                      <div class="tutorial-form-field"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Data do Pedido</div>
                      <div class="tutorial-form-field"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Observações</div>
                      <div class="tutorial-form-textarea"></div>
                    </div>
                    <div class="tutorial-form-buttons">
                      <div class="tutorial-form-button cancel">Cancelar</div>
                      <div class="tutorial-form-button save">Salvar</div>
                    </div>
                  </div>
                </div>
                
                <div v-if="currentStep === 3" class="tutorial-consulta-simulation">
                  <div class="tutorial-modal-header-sim">CONSULTAR PEDIDOS</div>
                  <div class="tutorial-filter-container">
                    <label class="tutorial-filter-label">
                      <i class="material-icons">filter_list</i>
                      Status:
                    </label>
                    <div class="tutorial-filter-select">PENDENTE</div>
                  </div>
                  <div class="tutorial-cards-container">
                    <div class="tutorial-card">
                      <div class="tutorial-card-header">
                        <span class="tutorial-order-id">#001</span>
                      </div>
                      <div class="tutorial-card-title">Manutenção de Equipamento</div>
                      <div class="tutorial-card-details">
                        <div class="tutorial-card-detail">
                          <i class="material-icons">format_list_numbered</i>
                          <span><strong>Quantidade:</strong> 1</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">category</i>
                          <span><strong>Categoria:</strong> Serviços</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">priority_high</i>
                          <span><strong>Urgência:</strong> Padrão</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">event</i>
                          <span><strong>Data do Pedido:</strong> 15/05/2025</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">person</i>
                          <span><strong>Usuário:</strong> João Silva</span>
                        </div>
                      </div>
                      <div class="tutorial-card-actions">
                        <button class="tutorial-open-button">
                          <i class="material-icons">visibility</i>
                          ABRIR
                        </button>
                        <button class="tutorial-edit-button">
                          <i class="material-icons">edit</i>
                          EDITAR
                        </button>
                        <button class="tutorial-complete-button">
                          <i class="material-icons">check_circle</i>
                          CONCLUIR
                        </button>
                      </div>
                    </div>
                    <div class="tutorial-card">
                      <div class="tutorial-card-header">
                        <span class="tutorial-order-id">#002</span>
                      </div>
                      <div class="tutorial-card-title">Compra de Insumos</div>
                      <div class="tutorial-card-details">
                        <div class="tutorial-card-detail">
                          <i class="material-icons">format_list_numbered</i>
                          <span><strong>Quantidade:</strong> 50</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">category</i>
                          <span><strong>Categoria:</strong> Matérias-primas</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">priority_high</i>
                          <span><strong>Urgência:</strong> Urgente</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">event</i>
                          <span><strong>Data do Pedido:</strong> 14/05/2025</span>
                        </div>
                        <div class="tutorial-card-detail">
                          <i class="material-icons">person</i>
                          <span><strong>Usuário:</strong> Maria Oliveira</span>
                        </div>
                      </div>
                      <div class="tutorial-card-actions">
                        <button class="tutorial-open-button">
                          <i class="material-icons">visibility</i>
                          ABRIR
                        </button>
                        <button class="tutorial-edit-button">
                          <i class="material-icons">edit</i>
                          EDITAR
                        </button>
                        <button class="tutorial-complete-button">
                          <i class="material-icons">check_circle</i>
                          CONCLUIR
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="tutorial-pagination">
                    <button class="tutorial-pagination-button">
                      <i class="material-icons">navigate_before</i>
                      Anterior
                    </button>
                    <span class="tutorial-pagination-info">Página 1 de 1</span>
                    <button class="tutorial-pagination-button">
                      Próximo
                      <i class="material-icons">navigate_next</i>
                    </button>
                  </div>
                  <button class="tutorial-close-button">
                    <i class="material-icons">close</i>
                    FECHAR
                  </button>
                </div>
                
                <div v-if="currentStep === 4" class="tutorial-edit-simulation">
                  <div class="tutorial-modal-header-sim">Editar Pedido #001</div>
                  <div class="tutorial-form">
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Produto</div>
                      <div class="tutorial-form-field filled"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Quantidade</div>
                      <div class="tutorial-form-field filled"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Data do Pedido</div>
                      <div class="tutorial-form-field filled"></div>
                    </div>
                    <div class="tutorial-form-row">
                      <div class="tutorial-form-label">Observações</div>
                      <div class="tutorial-form-textarea filled"></div>
                    </div>
                    <div class="tutorial-form-buttons">
                      <div class="tutorial-form-button cancel">Cancelar</div>
                      <div class="tutorial-form-button update">Atualizar</div>
                    </div>
                  </div>
                </div>
                
                <div v-if="currentStep === 5" class="tutorial-concluir-simulation">
                  <div class="tutorial-modal-header-sim">Visualizar Pedido #001</div>
                  <div class="tutorial-pedido-details">
                    <div class="tutorial-detail-row">
                      <div class="tutorial-detail-label">Produto:</div>
                      <div class="tutorial-detail-value">Produto A</div>
                    </div>
                    <div class="tutorial-detail-row">
                      <div class="tutorial-detail-label">Quantidade:</div>
                      <div class="tutorial-detail-value">10 unidades</div>
                    </div>
                    <div class="tutorial-detail-row">
                      <div class="tutorial-detail-label">Data do Pedido:</div>
                      <div class="tutorial-detail-value">15/05/2025</div>
                    </div>
                    <div class="tutorial-detail-row">
                      <div class="tutorial-detail-label">Status:</div>
                      <div class="tutorial-detail-value">
                        <span class="tutorial-status pending">Pendente</span>
                      </div>
                    </div>
                    <div class="tutorial-detail-row">
                      <div class="tutorial-detail-label">Observações:</div>
                      <div class="tutorial-detail-value">Entrega urgente</div>
                    </div>
                  </div>
                  <div class="tutorial-form-buttons">
                    <div class="tutorial-form-button cancel">Fechar</div>
                    <div class="tutorial-form-button complete">Concluir Pedido</div>
                  </div>
                </div>
                
                <div v-if="currentStep === 6" class="tutorial-permissions-simulation">
                  <div class="tutorial-modal-header-sim">Sistema de Permissões</div>
                  <div class="tutorial-permissions-content">
                    <div class="tutorial-permission-role">
                      <div class="tutorial-role-icon user">
                        <i class="material-icons">person</i>
                      </div>
                      <div class="tutorial-role-info">
                        <div class="tutorial-role-title">Usuário Comum</div>
                        <div class="tutorial-role-permissions">
                          <div class="tutorial-permission-item">✓ Criar pedidos</div>
                          <div class="tutorial-permission-item">✓ Ver pedidos do setor</div>
                          <div class="tutorial-permission-item">✓ Editar próprios pedidos</div>
                          <div class="tutorial-permission-item">✓ Concluir próprios pedidos</div>
                          <div class="tutorial-permission-item">✗ Editar pedidos de outros</div>
                          <div class="tutorial-permission-item">✗ Ver pedidos de outros setores</div>
                        </div>
                      </div>
                    </div>
                    <div class="tutorial-permission-role">
                      <div class="tutorial-role-icon manager">
                        <i class="material-icons">supervisor_account</i>
                      </div>
                      <div class="tutorial-role-info">
                        <div class="tutorial-role-title">Gestor</div>
                        <div class="tutorial-role-permissions">
                          <div class="tutorial-permission-item">✓ Todas as permissões de usuário comum</div>
                          <div class="tutorial-permission-item">✓ Editar pedidos do setor</div>
                          <div class="tutorial-permission-item">✓ Concluir pedidos do setor</div>
                          <div class="tutorial-permission-item">✓ Acessar relatórios</div>
                          <div class="tutorial-permission-item">✗ Ver pedidos de outros setores</div>
                        </div>
                      </div>
                    </div>
                    <div class="tutorial-permission-role">
                      <div class="tutorial-role-icon admin">
                        <i class="material-icons">admin_panel_settings</i>
                      </div>
                      <div class="tutorial-role-info">
                        <div class="tutorial-role-title">Administrador</div>
                        <div class="tutorial-role-permissions">
                          <div class="tutorial-permission-item">✓ Acesso completo ao sistema</div>
                          <div class="tutorial-permission-item">✓ Ver pedidos de todos os setores</div>
                          <div class="tutorial-permission-item">✓ Editar qualquer pedido</div>
                          <div class="tutorial-permission-item">✓ Gerenciar usuários</div>
                          <div class="tutorial-permission-item">✓ Gerar relatórios avançados</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div v-if="currentStep === 7" class="tutorial-resources-simulation">
                  <div class="tutorial-modal-header-sim">Recursos Adicionais</div>
                  <div class="tutorial-resources-grid">
                    <div class="tutorial-resource-card">
                      <div class="tutorial-resource-icon history">
                        <i class="material-icons">history</i>
                      </div>
                      <div class="tutorial-resource-title">Histórico de Alterações</div>
                      <div class="tutorial-resource-desc">Todas as mudanças são registradas</div>
                    </div>
                    <div class="tutorial-resource-card">
                      <div class="tutorial-resource-icon budget">
                        <i class="material-icons">account_balance</i>
                      </div>
                      <div class="tutorial-resource-title">Orçamentos e Custos</div>
                      <div class="tutorial-resource-desc">Controle financeiro dos pedidos</div>
                    </div>
                    <div class="tutorial-resource-card">
                      <div class="tutorial-resource-icon report">
                        <i class="material-icons">assessment</i>
                      </div>
                      <div class="tutorial-resource-title">Relatórios Gerenciais</div>
                      <div class="tutorial-resource-desc">Dados para tomada de decisão</div>
                    </div>
                    <div class="tutorial-resource-card">
                      <div class="tutorial-resource-icon security">
                        <i class="material-icons">security</i>
                      </div>
                      <div class="tutorial-resource-title">Segurança Avançada</div>
                      <div class="tutorial-resource-desc">Proteção em todos os níveis</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="tutorial-info">
              <h3>{{ tutorialSteps[currentStep - 1].title }}</h3>
              <p>{{ tutorialSteps[currentStep - 1].description }}</p>
              <div class="tutorial-tip" v-if="tutorialSteps[currentStep - 1].tip">
                <span class="tip-icon">💡</span>
                <span class="tip-text">{{ tutorialSteps[currentStep - 1].tip }}</span>
              </div>
              
              <div class="tutorial-navigation">
                <button 
                  @click="goToPrevious" 
                  class="tutorial-prev-btn"
                  :disabled="currentStep === 1"
                >
                  <i class="material-icons">arrow_back</i>
                  Anterior
                </button>
                <button 
                  v-if="!isLastStep" 
                  @click="goToNext" 
                  class="tutorial-next-btn"
                >
                  Próximo
                  <i class="material-icons">arrow_forward</i>
                </button>
                <button 
                  v-else 
                  @click="finishTutorial" 
                  class="tutorial-finish-btn"
                >
                  Finalizar
                  <i class="material-icons">check_circle</i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
export default {
  name: 'TutorialModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentStep: 1,
      tutorialSteps: [
        {
          title: 'Bem-vindo ao Sistema de Pedidos',
          description: 'Este tutorial rápido vai te mostrar como utilizar o sistema. A navegação principal fica no menu lateral, de onde você pode acessar todas as funcionalidades. O sistema foi projetado para gerenciar pedidos de diferentes setores da empresa com segurança e eficiência.',
          tip: 'Você pode acessar este tutorial novamente a qualquer momento pelo menu de Ajuda. Seu perfil de usuário determina quais ações você pode realizar no sistema.'
        },
        {
          title: 'Criando um Pedido',
          description: 'Para criar um pedido, clique no botão "Criar Pedido" no menu. Preencha o formulário com os dados necessários, como descrição, quantidade, categoria, urgência e observações. Os pedidos são automaticamente vinculados ao seu setor e ficam visíveis para todos os usuários do mesmo setor.',
          tip: 'Todos os campos marcados com * são obrigatórios. Você pode anexar arquivos ao pedido para fornecer informações adicionais.'
        },
        {
          title: 'Consultando Pedidos',
          description: 'Para visualizar os pedidos existentes, clique em "Consultar Pedidos" no menu. Aqui você pode ver todos os pedidos do seu setor organizados em cards com suas principais informações. É possível filtrar por status (Pendente, Concluído ou Cancelado) para facilitar a visualização.',
          tip: 'Apenas usuários administradores podem ver pedidos de todos os setores. Usuários comuns visualizam apenas os pedidos do seu próprio setor, garantindo a segurança das informações.'
        },
        {
          title: 'Editando um Pedido',
          description: 'Na lista de pedidos, você pode clicar no botão EDITAR para modificar um pedido existente. Note que você só poderá editar pedidos que você mesmo criou, a menos que seja um gestor ou administrador. Todas as alterações são registradas no histórico do pedido para auditoria.',
          tip: 'Administradores e gestores podem editar qualquer pedido. Usuários comuns podem editar apenas os pedidos que eles mesmos criaram, garantindo a integridade dos dados.'
        },
        {
          title: 'Concluindo um Pedido',
          description: 'Quando um pedido for finalizado, você pode marcá-lo como concluído clicando no botão CONCLUIR. Esta ação só está disponível para o criador do pedido, gestores ou administradores. Ao concluir um pedido, você pode informar a data exata da conclusão.',
          tip: 'Pedidos concluídos não podem mais ser editados. O sistema mantém um registro completo de quem concluiu cada pedido e quando, garantindo total rastreabilidade.'
        },
        {
          title: 'Sistema de Permissões',
          description: 'O sistema possui três níveis de acesso: Usuário Comum, Gestor e Administrador. Usuários comuns podem criar e gerenciar seus próprios pedidos. Gestores podem gerenciar todos os pedidos do seu setor. Administradores têm acesso completo a todos os pedidos e usuários do sistema.',
          tip: 'As permissões são verificadas no servidor a cada operação, garantindo a segurança mesmo que alguém tente burlar as restrições da interface.'
        },
        {
          title: 'Recursos Adicionais',
          description: 'O sistema oferece outros recursos como: histórico detalhado de alterações em pedidos, registro de atividades, orçamentos e custos para cada pedido, filtros avançados de pesquisa e relatórios gerenciais para acompanhamento de desempenho.',
          tip: 'Gestores e administradores têm acesso a relatórios e estatísticas que ajudam na tomada de decisões estratégicas para a empresa.'
        }
      ]
    };
  },
  computed: {
    isLastStep() {
      return this.currentStep === this.tutorialSteps.length;
    }
  },
  methods: {
    goToNext() {
      if (this.currentStep < this.tutorialSteps.length) {
        this.currentStep++;
      }
    },
    goToPrevious() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },
    skipTutorial() {
      this.$emit('close');
    },
    finishTutorial() {
      this.$emit('close');
    },
    handleOverlayClick(event) {
      // Não permite fechar o tutorial clicando fora, apenas com os botões
      event.stopPropagation();
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');

.tutorial-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.tutorial-modal {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: 12px;
  width: 95%;
  max-width: 900px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
  color: white;
  overflow: hidden;
  max-height: 95vh;
  display: flex;
  flex-direction: column;
}

.tutorial-modal-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
}

.tutorial-modal-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
}

.tutorial-actions {
  display: flex;
  gap: 10px;
}

.tutorial-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tutorial-skip-btn {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ccc;
}

.tutorial-skip-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.tutorial-navigation {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: flex-end;
}

.tutorial-prev-btn,
.tutorial-next-btn, 
.tutorial-finish-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tutorial-prev-btn {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ccc;
}

.tutorial-prev-btn:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.2);
}

.tutorial-prev-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tutorial-next-btn, .tutorial-finish-btn {
  background-color: #ff6f61;
  color: #fff;
}

.tutorial-next-btn:hover, .tutorial-finish-btn:hover {
  background-color: #ff8577;
  transform: translateY(-2px);
}

.tutorial-content {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
  max-height: none;
}

.tutorial-progress {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #66ccff;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 14px;
  color: #bbb;
}

.tutorial-step {
  display: flex;
  gap: 30px;
  flex-direction: column;
}

.tutorial-illustration {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 20px;
  overflow: hidden;
  min-height: 350px;
  max-height: 450px;
}

.tutorial-image {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

/* Estilos para simulações realistas */
.tutorial-menu-simulation,
.tutorial-pedido-simulation,
.tutorial-consulta-simulation,
.tutorial-edit-simulation,
.tutorial-concluir-simulation,
.tutorial-permissions-simulation,
.tutorial-resources-simulation {
  display: flex;
  flex-direction: column;
  height: auto;
  width: 100%;
  max-height: 100%;
  overflow: hidden;
}

/* Menu Simulação */
.tutorial-sidebar {
  width: 200px;
  background-color: #2e2e2e;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
}

.tutorial-logo {
  width: 80px;
  height: 80px;
  background-color: #66ccff;
  border-radius: 50%;
  margin-bottom: 20px;
}

.tutorial-menu-button {
  width: 80%;
  padding: 10px 15px;
  background-color: #424242;
  color: #fff;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 10px;
  font-weight: 500;
  cursor: pointer;
}

.tutorial-menu-button.active {
  background-color: #66ccff;
  color: #000;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.tutorial-menu-button.logout {
  background-color: #ff5252;
  margin-top: auto;
}

.tutorial-menu-simulation {
  display: flex;
  flex-direction: row;
}

.tutorial-content-area {
  flex: 1;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tutorial-welcome {
  text-align: center;
}

.tutorial-welcome-icon {
  width: 80px;
  height: 80px;
  background-color: #66ccff;
  border-radius: 50%;
  margin: 0 auto 20px;
}

.tutorial-welcome-text {
  font-size: 24px;
  color: #fff;
  font-weight: 600;
}

/* Form Simulação */
.tutorial-modal-header-sim {
  background-color: #ff6f61;
  color: white;
  padding: 15px 20px;
  font-weight: 600;
  font-size: 18px;
  text-align: center;
}

.tutorial-form {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tutorial-form-row {
  display: flex;
  gap: 10px;
  align-items: center;
}

.tutorial-form-label {
  width: 120px;
  color: #bbb;
  font-size: 14px;
}

.tutorial-form-field {
  flex: 1;
  height: 40px;
  background-color: #444;
  border-radius: 6px;
  position: relative;
}

.tutorial-form-field.filled::after {
  content: '';
  position: absolute;
  left: 15px;
  top: 12px;
  width: 70%;
  height: 16px;
  background-color: #666;
  border-radius: 4px;
}

.tutorial-form-textarea {
  flex: 1;
  height: 80px;
  background-color: #444;
  border-radius: 6px;
  position: relative;
}

.tutorial-form-textarea.filled::after {
  content: '';
  position: absolute;
  left: 15px;
  top: 15px;
  width: 80%;
  height: 50px;
  background-color: #666;
  border-radius: 4px;
}

.tutorial-form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 15px;
}

.tutorial-form-button {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  text-align: center;
}

.tutorial-form-button.cancel {
  background-color: #555;
  color: #fff;
}

.tutorial-form-button.save,
.tutorial-form-button.update {
  background-color: #66ccff;
  color: #000;
}

.tutorial-form-button.complete {
  background-color: #5cb85c;
  color: #fff;
}

/* Lista de Pedidos Simulação */
.tutorial-search-bar {
  padding: 15px 20px;
  display: flex;
  gap: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tutorial-search-field {
  flex: 1;
  height: 40px;
  background-color: #444;
  border-radius: 6px;
}

.tutorial-search-button {
  width: 40px;
  height: 40px;
  background-color: #66ccff;
  border-radius: 6px;
}

.tutorial-table {
  width: 100%;
  padding: 0 20px;
  margin-top: 15px;
}

.tutorial-table-header {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr 1fr 1fr;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tutorial-th {
  font-weight: 600;
  color: #ccc;
  font-size: 14px;
}

.tutorial-table-row {
  display: grid;
  grid-template-columns: 0.5fr 2fr 1fr 1fr 1fr;
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tutorial-td {
  color: #fff;
  font-size: 14px;
  display: flex;
  align-items: center;
}

.tutorial-status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.tutorial-status.pending {
  background-color: #ffc107;
  color: #000;
}

.tutorial-status.complete {
  background-color: #5cb85c;
  color: #fff;
}

.tutorial-action-buttons {
  display: flex;
  gap: 8px;
}

.tutorial-action-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  position: relative;
}

.tutorial-action-btn.view {
  background-color: #666;
}

.tutorial-action-btn.edit {
  background-color: #2196F3;
}

/* Detalhe do Pedido Simulação */
.tutorial-pedido-details {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tutorial-detail-row {
  display: flex;
  gap: 10px;
}

.tutorial-detail-label {
  width: 120px;
  color: #bbb;
  font-size: 14px;
  font-weight: 600;
}

.tutorial-detail-value {
  flex: 1;
  color: #fff;
  font-size: 14px;
}

.tutorial-info {
  flex: 1;
  padding: 15px 0;
}

.tutorial-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 20px;
  color: #fff;
}

.tutorial-info p {
  margin-bottom: 20px;
  color: #ccc;
  line-height: 1.6;
}

.tutorial-tip {
  background: linear-gradient(145deg, #3a3a3a, #333);
  padding: 15px;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 20px;
  border-left: 3px solid #ff6f61;
}

.tip-icon {
  font-size: 20px;
}

.tip-text {
  color: #ddd;
  font-size: 14px;
  line-height: 1.5;
}

@media (min-width: 768px) {
  .tutorial-step {
    flex-direction: row;
  }
  
  .tutorial-illustration {
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .tutorial-modal {
    width: 95%;
    max-height: 95vh;
  }
  
  .tutorial-illustration {
    min-height: 350px;
  }
  
  .tutorial-menu-simulation,
  .tutorial-pedido-simulation,
  .tutorial-consulta-simulation,
  .tutorial-edit-simulation,
  .tutorial-concluir-simulation,
  .tutorial-permissions-simulation,
  .tutorial-resources-simulation {
    max-width: 100%;
    overflow-y: auto;
    max-height: 350px;
  }
  
  .tutorial-cards-container {
    grid-template-columns: 1fr;
  }
  
  .tutorial-resources-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .tutorial-permissions-content {
    padding: 10px;
  }
  
  .tutorial-permission-role {
    flex-direction: column;
    align-items: center;
  }
  
  .tutorial-role-permissions {
    grid-template-columns: 1fr;
  }
  
  .tutorial-navigation {
    justify-content: space-between;
  }
}

.tutorial-role-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  font-size: 28px;
}

.tutorial-role-icon.user {
  background-color: #3498db;
}

.tutorial-role-icon.manager {
  background-color: #f39c12;
}

.tutorial-role-icon.admin {
  background-color: #ff6f61;
}

.tutorial-resource-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  color: white;
  font-size: 28px;
}

.tutorial-resource-icon.history {
  background-color: #3498db;
}

.tutorial-resource-icon.budget {
  background-color: #2ecc71;
}

.tutorial-resource-icon.report {
  background-color: #f39c12;
}

.tutorial-resource-icon.security {
  background-color: #e74c3c;
}

.tutorial-detail-icon {
  width: 24px;
  height: 24px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tutorial-detail-icon i {
  font-size: 14px;
  color: #ff6f61;
}

.tutorial-card-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 6px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  font-weight: 500;
}

.tutorial-card-button.view {
  background-color: #555;
  color: #fff;
}

.tutorial-card-button.edit {
  background-color: #3498db;
  color: #fff;
}

.tutorial-card-button.complete {
  background-color: #5cb85c;
  color: #fff;
}

.tutorial-permission-item {
  font-size: 0.9rem;
  color: #ddd;
  padding: 7px;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Ajustar o estilo dos cards */
.tutorial-cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  padding: 15px;
  overflow-y: auto;
  max-height: 250px;
}

/* Ajustes para os passos 6 e 7 */
.tutorial-permissions-content,
.tutorial-resources-grid {
  padding: 15px;
  overflow-y: auto;
  max-height: 280px;
}

/* Consulta de Pedidos - Passo 3 (estilo atualizado) */
.tutorial-consulta-simulation {
  background-color: #1f1f1f;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
}

.tutorial-modal-header-sim {
  background-color: #1f1f1f;
  color: #ff6f61;
  padding: 15px 20px;
  font-weight: 600;
  font-size: 18px;
  text-align: left;
  border-bottom: 1px solid #333;
  margin-bottom: 0;
}

.tutorial-filter-container {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #1f1f1f;
  border-bottom: 1px solid #333;
}

.tutorial-filter-label {
  display: flex;
  align-items: center;
  color: #999;
  margin-right: 10px;
}

.tutorial-filter-label i {
  margin-right: 5px;
  color: #ff6f61;
  font-size: 18px;
}

.tutorial-filter-select {
  background-color: #333;
  color: #f5f5f5;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 0.9rem;
}

.tutorial-card {
  background-color: #2a2a2a;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  border: 1px solid #333;
}

.tutorial-card:hover {
  transform: translateY(-3px);
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.2);
}

.tutorial-order-id {
  font-size: 1.5em;
  color: #ff6f61;
  font-weight: bold;
}

.tutorial-card-title {
  font-size: 1.2rem;
  color: #f5f5f5;
  text-align: center;
  margin: 5px 0 10px;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}

.tutorial-card-details {
  width: 100%;
}

.tutorial-card-detail {
  margin: 8px 0;
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #dfe6e9;
}

.tutorial-card-detail i {
  margin-right: 8px;
  color: #ff6f61;
  font-size: 16px;
}

.tutorial-card-detail strong {
  margin-right: 5px;
}

.tutorial-card-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  gap: 10px;
}

.tutorial-open-button,
.tutorial-edit-button,
.tutorial-complete-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 11px;
  font-weight: bold;
  gap: 5px;
}

.tutorial-open-button {
  background-color: #444;
  color: white;
}

.tutorial-edit-button {
  background-color: #3498db;
  color: white;
}

.tutorial-complete-button {
  background-color: #5cb85c;
  color: white;
}

.tutorial-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-top: 1px solid #333;
  margin-top: auto;
}

.tutorial-pagination-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #333;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.tutorial-close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin: 15px 20px;
  padding: 10px;
  background-color: #444;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
}
</style> 