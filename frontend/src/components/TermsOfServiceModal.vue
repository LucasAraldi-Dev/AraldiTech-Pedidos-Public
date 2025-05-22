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
        
        <h3>1. Termos de Uso do Sistema AraldiTech Pedidos</h3>
        <p>O AraldiTech Pedidos é uma plataforma corporativa para gestão de pedidos, controle de estoque e rastreabilidade de operações. Seu uso é restrito a colaboradores e parceiros autorizados da AraldiTech.</p>
        <h3>2. Compromisso do Usuário</h3>
        <p>Ao se cadastrar, você se compromete a:</p>
        <ul>
          <li>Fornecer informações verdadeiras e atualizadas;</li>
          <li>Utilizar o sistema apenas para fins profissionais e autorizados pela empresa;</li>
          <li>Manter a confidencialidade de suas credenciais de acesso;</li>
          <li>Notificar imediatamente a equipe AraldiTech sobre qualquer uso não autorizado de sua conta;</li>
          <li>Respeitar as regras internas de segurança e compliance da empresa.</li>
        </ul>
        <h3>3. Política de Privacidade</h3>
        <p>A AraldiTech valoriza a privacidade dos seus dados. Ao utilizar o sistema, você concorda com a coleta e uso das seguintes informações:</p>
        <ul>
          <li>Dados cadastrais: nome, e-mail, setor, nome de usuário;</li>
          <li>Registros de acesso: datas, horários, IPs e logs de operações realizadas;</li>
          <li>Dados de navegação para melhoria contínua da plataforma.</li>
        </ul>
        <p>Esses dados são utilizados exclusivamente para:</p>
        <ul>
          <li>Garantir a segurança e rastreabilidade das operações;</li>
          <li>Auditoria interna e atendimento a obrigações legais;</li>
          <li>Melhorias de usabilidade e suporte técnico;</li>
          <li>Contato em caso de incidentes ou atualizações importantes.</li>
        </ul>
        <p>Seus dados não serão compartilhados com terceiros, exceto por obrigação legal ou ordem judicial. Você pode solicitar a revisão, atualização ou exclusão dos seus dados a qualquer momento, conforme a LGPD.</p>
        <h3>4. Responsabilidades e Boas Práticas</h3>
        <ul>
          <li>Não compartilhe sua senha ou acesso com terceiros;</li>
          <li>Não utilize o sistema para fins ilícitos ou fora do escopo corporativo;</li>
          <li>Respeite a integridade dos dados e das operações;</li>
          <li>Em caso de dúvidas, entre em contato com o suporte AraldiTech.</li>
        </ul>
        <h3>5. Atualizações e Suporte</h3>
        <p>A AraldiTech pode atualizar estes termos e a plataforma a qualquer momento para garantir segurança, conformidade e melhorias. O uso contínuo do sistema implica concordância com as versões mais recentes dos termos.</p>
        <h3>6. Contato</h3>
        <p>Para dúvidas sobre privacidade, uso do sistema ou solicitações relacionadas aos seus dados, entre em contato pelo e-mail: contato@aralditech.com</p>
      </div>
      <div class="terms-modal-footer">
        <div class="terms-acceptance">
          <label class="checkbox-container">
            <input type="checkbox" v-model="termsAccepted" :disabled="!hasScrolledToBottom">
            <span class="checkmark"></span>
            <span class="acceptance-text">Li e aceito os Termos de Uso e a Política de Privacidade do AraldiTech Pedidos</span>
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