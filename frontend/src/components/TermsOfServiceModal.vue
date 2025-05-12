<template>
  <div class="terms-modal-overlay" v-if="show">
    <div class="terms-modal">
      <div class="terms-modal-header">
        <h2>Termos de Serviço</h2>
      </div>
      <div class="terms-modal-body" ref="termsContent" @scroll="checkScroll">
        <div class="scroll-info" v-if="!hasScrolledToBottom">
          <div class="scroll-icon">
            <i class="fas fa-arrow-down"></i>
          </div>
          <p>Role até o final para aceitar os termos</p>
        </div>
        
        <h3>1. Termos e Condições de Uso do Sistema AraldiTech Pedidos</h3>
        <p>Ao se cadastrar e utilizar o sistema AraldiTech Pedidos ("Sistema"), você concorda integralmente com estes Termos de Serviço. Leia atentamente antes de prosseguir com seu cadastro.</p>
        
        <h3>2. Descrição do Serviço</h3>
        <p>O Sistema AraldiTech Pedidos é uma plataforma desenvolvida para gerenciamento de pedidos, controle de inventário, e monitoramento de atividades operacionais. O sistema é fornecido no estado em que se encontra, sujeito a modificações e melhorias periódicas.</p>
        
        <h3>3. Registro e Segurança da Conta</h3>
        <p>Para utilizar o Sistema, você deve criar uma conta com informações precisas e completas. Você é responsável por:</p>
        <ul>
          <li>Manter a confidencialidade de sua senha</li>
          <li>Restringir o acesso ao seu computador e dispositivos</li>
          <li>Assumir total responsabilidade por todas as atividades realizadas com sua conta</li>
          <li>Notificar imediatamente a AraldiTech sobre qualquer uso não autorizado de sua conta</li>
        </ul>
        <p>A AraldiTech não será responsável por perdas ou danos decorrentes do não cumprimento dessas responsabilidades.</p>
        
        <h3>4. Dados do Usuário e Privacidade</h3>
        <p>Ao utilizar o Sistema, você concorda que a AraldiTech poderá:</p>
        <ul>
          <li>Coletar e armazenar informações pessoais conforme detalhado em nossa Política de Privacidade</li>
          <li>Registrar data, hora e IP do aceite destes termos para fins legais e de auditoria</li>
          <li>Armazenar registros de atividades (logs) de sua utilização do sistema</li>
          <li>Utilizar cookies e tecnologias semelhantes para melhorar a experiência do usuário</li>
        </ul>
        
        <h3>5. Uso Apropriado do Sistema</h3>
        <p>Você concorda em utilizar o Sistema apenas para fins legítimos e de acordo com estes termos. Você não deve:</p>
        <ul>
          <li>Usar o Sistema para atividades ilegais ou não autorizadas</li>
          <li>Tentar obter acesso não autorizado ao Sistema ou a contas de outros usuários</li>
          <li>Compartilhar suas credenciais de acesso com terceiros</li>
          <li>Introduzir malware, vírus ou qualquer código prejudicial ao Sistema</li>
          <li>Interferir ou interromper a integridade ou o desempenho do Sistema</li>
          <li>Coletar ou armazenar informações pessoais de outros usuários do Sistema</li>
        </ul>
        
        <h3>6. Disponibilidade e Atualizações</h3>
        <p>A AraldiTech se esforçará para manter o Sistema disponível, mas não garante que:</p>
        <ul>
          <li>O Sistema estará disponível ininterruptamente</li>
          <li>O Sistema estará livre de erros ou problemas técnicos</li>
          <li>As funcionalidades atenderão a todos os requisitos específicos dos usuários</li>
        </ul>
        <p>A AraldiTech reserva-se o direito de modificar, atualizar ou descontinuar recursos do Sistema a qualquer momento, sem aviso prévio.</p>
        
        <h3>7. Propriedade Intelectual</h3>
        <p>Todo o conteúdo e código do Sistema, incluindo mas não limitado a textos, gráficos, logos, ícones, imagens, clipes de áudio, downloads digitais e compilações de dados, são propriedade exclusiva da AraldiTech ou de seus fornecedores de conteúdo e estão protegidos por leis nacionais e internacionais de direitos autorais.</p>
        
        <h3>8. Limitação de Responsabilidade</h3>
        <p>Em nenhuma circunstância a AraldiTech, seus diretores, funcionários, agentes ou parceiros serão responsáveis por quaisquer danos diretos, indiretos, incidentais, especiais, exemplares ou consequenciais, incluindo, entre outros, perda de lucros, dados, uso, boa vontade ou outras perdas intangíveis, resultantes de:</p>
        <ul>
          <li>Uso ou incapacidade de uso do Sistema</li>
          <li>Acesso não autorizado ou alteração de suas transmissões ou dados</li>
          <li>Declarações ou conduta de terceiros no Sistema</li>
          <li>Perda de dados ou interrupções de negócios decorrentes do uso do Sistema</li>
        </ul>
        
        <h3>9. Indemnização</h3>
        <p>Você concorda em defender, indenizar e isentar a AraldiTech, seus diretores, funcionários e agentes de e contra quaisquer reclamações, danos, obrigações, perdas, responsabilidades, custos ou dívidas e despesas (incluindo, mas não se limitando a honorários advocatícios) decorrentes de:</p>
        <ul>
          <li>Seu uso e acesso ao Sistema</li>
          <li>Violação por parte do usuário de qualquer termo deste acordo</li>
          <li>Violação por parte do usuário de qualquer direito de terceiros, incluindo, sem limitação, qualquer direito autoral, propriedade ou direito de privacidade</li>
        </ul>
        
        <h3>10. Rescisão</h3>
        <p>A AraldiTech pode, a seu exclusivo critério, suspender ou encerrar seu acesso ao Sistema por qualquer motivo, incluindo, sem limitação, violação destes Termos de Serviço. Após o término, seu direito de utilizar o Sistema cessará imediatamente.</p>
        
        <h3>11. Conformidade com Leis</h3>
        <p>Você deve cumprir todas as leis locais, estaduais, nacionais e internacionais aplicáveis ao uso do Sistema, incluindo, sem limitação, as leis de proteção de dados como a Lei Geral de Proteção de Dados (LGPD) do Brasil.</p>
        
        <h3>12. Modificações dos Termos</h3>
        <p>A AraldiTech reserva-se o direito de revisar estes termos a qualquer momento, sem aviso prévio. Ao continuar a usar o Sistema após tais alterações, você concorda em ficar vinculado aos termos revisados.</p>
        
        <h3>13. Lei Aplicável</h3>
        <p>Estes termos e condições são regidos e interpretados de acordo com as leis do Brasil, e você se submete irrevogavelmente à jurisdição exclusiva dos tribunais brasileiros para a resolução de quaisquer disputas.</p>
        
        <h3>14. Contato</h3>
        <p>Se você tiver dúvidas sobre estes Termos de Serviço, entre em contato conosco pelo e-mail: contato@aralditech.com</p>
      </div>
      <div class="terms-modal-footer">
        <div class="terms-acceptance">
          <label class="checkbox-container">
            <input type="checkbox" v-model="termsAccepted" :disabled="!hasScrolledToBottom">
            <span class="checkmark"></span>
            <span class="acceptance-text">Li e aceito os termos de serviço</span>
          </label>
        </div>
        <div class="terms-actions">
          <button 
            type="button" 
            class="btn-decline" 
            @click="declineTerms">
            Não Aceito
          </button>
          <button 
            type="button" 
            class="btn-accept" 
            :disabled="!termsAccepted" 
            @click="acceptTerms">
            Aceito e Concordo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'TermsOfServiceModal',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['accept-terms', 'decline-terms'],
  setup(props, { emit }) {
    const termsContent = ref(null);
    const termsAccepted = ref(false);
    const hasScrolledToBottom = ref(false);
    
    // Verificar se o usuário rolou até o final dos termos
    const checkScroll = () => {
      if (!termsContent.value) return;
      
      const { scrollTop, scrollHeight, clientHeight } = termsContent.value;
      // Consideramos "rolado até o final" quando estiver a menos de 30px do fim
      const isAtBottom = scrollTop + clientHeight >= scrollHeight - 30;
      
      if (isAtBottom && !hasScrolledToBottom.value) {
        hasScrolledToBottom.value = true;
      }
    };
    
    // Aceitar os termos e emitir evento com timestamp
    const acceptTerms = () => {
      if (!termsAccepted.value || !hasScrolledToBottom.value) return;
      
      const acceptanceTimestamp = new Date().toISOString();
      emit('accept-terms', { 
        accepted: true, 
        timestamp: acceptanceTimestamp,
        userAgent: navigator.userAgent,
        // Incluímos informações adicionais para registro
        termsVersion: '1.0',
        acceptanceMethod: 'checkbox-confirmation'
      });
    };
    
    // Recusar os termos
    const declineTerms = () => {
      emit('decline-terms');
    };
    
    onMounted(() => {
      // Resetar estado quando o modal for aberto
      termsAccepted.value = false;
      hasScrolledToBottom.value = false;
    });
    
    return {
      termsContent,
      termsAccepted,
      hasScrolledToBottom,
      checkScroll,
      acceptTerms,
      declineTerms
    };
  }
}
</script>

<style scoped>
.terms-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.terms-modal {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: 12px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  animation: modalFadeIn 0.3s ease;
}

.terms-modal-header {
  padding: 20px;
  border-bottom: 1px solid #444;
  display: flex;
  justify-content: center;
  align-items: center;
}

.terms-modal-header h2 {
  margin: 0;
  font-size: 24px;
  color: #fff;
  text-align: center;
}

.terms-modal-body {
  padding: 20px;
  overflow-y: auto;
  max-height: 50vh;
  position: relative;
  scroll-behavior: smooth;
}

.scroll-info {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.8);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  z-index: 10;
  animation: pulse 2s infinite;
}

.scroll-icon {
  font-size: 24px;
  color: #66ccff;
  margin-bottom: 10px;
}

.scroll-info p {
  margin: 0;
  color: #fff;
  font-size: 16px;
}

.terms-modal-body h3 {
  font-size: 18px;
  margin: 25px 0 10px;
  color: #eee;
}

.terms-modal-body h3:first-child {
  margin-top: 0;
}

.terms-modal-body p {
  font-size: 15px;
  line-height: 1.6;
  color: #ccc;
  margin-bottom: 16px;
}

.terms-modal-body ul {
  padding-left: 20px;
  margin-bottom: 16px;
}

.terms-modal-body li {
  margin-bottom: 8px;
  color: #ccc;
  line-height: 1.5;
}

.terms-modal-footer {
  padding: 20px;
  border-top: 1px solid #444;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.terms-acceptance {
  display: flex;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 35px;
  cursor: pointer;
  font-size: 16px;
  user-select: none;
  color: #eee;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 24px;
  width: 24px;
  background-color: #444;
  border-radius: 4px;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #555;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: #66ccff;
}

.checkbox-container input:disabled ~ .checkmark {
  background-color: #444;
  opacity: 0.5;
  cursor: not-allowed;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container .acceptance-text {
  margin-left: 5px;
}

.terms-actions {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.btn-accept, .btn-decline {
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.btn-accept {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #fff;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.btn-accept:not(:disabled):hover {
  background: linear-gradient(145deg, #444, #333);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}

.btn-accept:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-decline {
  background: transparent;
  color: #ccc;
  border: 1px solid #444;
}

.btn-decline:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(102, 204, 255, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(102, 204, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(102, 204, 255, 0);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .terms-modal {
    max-width: 95%;
  }
  
  .terms-modal-header h2 {
    font-size: 20px;
  }
  
  .terms-modal-body {
    max-height: 40vh;
    padding: 15px;
  }
  
  .terms-modal-body h3 {
    font-size: 16px;
  }
  
  .terms-modal-body p, 
  .terms-modal-body li {
    font-size: 14px;
  }
  
  .checkbox-container {
    font-size: 14px;
  }
  
  .terms-actions {
    flex-direction: column;
  }
  
  .btn-accept, .btn-decline {
    padding: 12px 15px;
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .terms-modal-header h2 {
    font-size: 18px;
  }
  
  .terms-modal-body {
    padding: 12px;
  }
  
  .terms-modal-body h3 {
    font-size: 15px;
  }
  
  .terms-modal-body p, 
  .terms-modal-body li {
    font-size: 13px;
  }
  
  .checkbox-container {
    font-size: 13px;
    padding-left: 30px;
  }
  
  .checkmark {
    height: 20px;
    width: 20px;
  }
  
  .checkbox-container .checkmark:after {
    left: 7px;
    top: 4px;
    width: 5px;
    height: 10px;
  }
  
  .btn-accept, .btn-decline {
    padding: 10px 15px;
    font-size: 14px;
  }
}
</style> 