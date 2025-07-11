<template>
  <footer class="app-footer">
    <div class="container">
      <p>&copy; 2025 AraldiTech. Todos os direitos reservados.</p>
      <ul class="footer-links">
        <li><router-link to="/politica-privacidade" @click.prevent="showModal('privacy')">Política de Privacidade</router-link></li>
        <li><router-link to="/termos-uso" @click.prevent="showModal('terms')">Termos de Uso</router-link></li>
      </ul>
    </div>
    
    <!-- Modal Política de Privacidade -->
    <div class="policy-modal" v-if="activeModal === 'privacy'">
      <div class="policy-modal-content">
        <div class="policy-modal-header">
          <h2>Política de Privacidade</h2>
          <button class="close-modal" @click="closeModal">&times;</button>
        </div>
        <div class="policy-modal-body">
          <h3>1. Informações que coletamos</h3>
          <p>A AraldiTech coleta informações quando você se registra em nosso sistema, faz login e utiliza o aplicativo. As informações coletadas incluem seu nome, e-mail, dados de pedidos, setor e outras informações necessárias para o funcionamento do sistema.</p>
          
          <h3>2. Como usamos suas informações</h3>
          <p>Suas informações são utilizadas para:</p>
          <ul>
            <li>Gerenciar sua conta e fornecer o serviço solicitado</li>
            <li>Melhorar o sistema e a experiência do usuário</li>
            <li>Enviar comunicações relacionadas ao serviço</li>
            <li>Gerar relatórios e estatísticas internas</li>
          </ul>
          
          <h3>3. Proteção de dados</h3>
          <p>Implementamos medidas de segurança para proteger suas informações pessoais. Seus dados são armazenados em servidores seguros e protegidos contra acesso não autorizado.</p>
          
          <h3>4. Compartilhamento de informações</h3>
          <p>Não vendemos, trocamos ou transferimos suas informações pessoais para terceiros. Isso não inclui parceiros confiáveis que nos auxiliam na operação do nosso sistema, desde que concordem em manter essas informações confidenciais.</p>
          
          <h3>5. Seus direitos</h3>
          <p>Você tem o direito de acessar, corrigir ou excluir suas informações pessoais a qualquer momento. Para exercer esses direitos, entre em contato com nosso suporte.</p>
          
          <h3>6. Alterações na política de privacidade</h3>
          <p>Qualquer alteração em nossa política de privacidade será publicada nesta página. Recomendamos que você consulte regularmente nossa política de privacidade.</p>
          
          <h3>7. Contato</h3>
          <p>Se você tiver dúvidas sobre esta política de privacidade, entre em contato conosco através do email: contato@aralditech.com</p>
        </div>
        <div class="policy-modal-footer">
          <button class="btn-accept" @click="closeModal">Entendi</button>
        </div>
      </div>
    </div>
    
    <!-- Modal Termos de Uso -->
    <div class="policy-modal" v-if="activeModal === 'terms'">
      <div class="policy-modal-content">
        <div class="policy-modal-header">
          <h2>Termos de Uso</h2>
          <button class="close-modal" @click="closeModal">&times;</button>
        </div>
        <div class="policy-modal-body">
          <h3>1. Aceitação dos Termos</h3>
          <p>Ao acessar e utilizar o sistema AraldiTech Pedidos, você concorda em cumprir estes Termos de Uso. Se você não concordar com algum dos termos, não deverá utilizar o sistema.</p>
          
          <h3>2. Contas de Usuário</h3>
          <p>Para utilizar o sistema, você precisará criar uma conta. Você é responsável por manter a confidencialidade de sua senha e é totalmente responsável por todas as atividades realizadas com sua conta.</p>
          
          <h3>3. Uso Adequado</h3>
          <p>Você concorda em utilizar o sistema apenas para fins legítimos e de acordo com estes termos. Você não deve:</p>
          <ul>
            <li>Violar leis ou regulamentos aplicáveis</li>
            <li>Compartilhar sua conta com terceiros</li>
            <li>Tentar acessar áreas restritas do sistema</li>
            <li>Introduzir vírus, malware ou outros códigos maliciosos</li>
          </ul>
          
          <h3>4. Propriedade Intelectual</h3>
          <p>Todo o conteúdo, recursos e funcionalidades do sistema AraldiTech Pedidos são de propriedade da AraldiTech e estão protegidos por leis de propriedade intelectual.</p>
          
          <h3>5. Limitação de Responsabilidade</h3>
          <p>A AraldiTech não será responsável por danos indiretos, consequenciais, especiais, punitivos ou exemplares, incluindo perda de dados, interrupção de negócios ou perda de lucros.</p>
          
          <h3>6. Suspensão e Término</h3>
          <p>A AraldiTech reserva-se o direito de suspender ou encerrar sua conta a qualquer momento, por qualquer motivo, sem aviso prévio, incluindo por violação destes Termos de Uso.</p>
          
          <h3>7. Modificações</h3>
          <p>A AraldiTech pode modificar estes Termos de Uso a qualquer momento. As alterações entram em vigor imediatamente após sua publicação. Seu uso continuado do sistema após tais alterações constitui sua aceitação dos novos termos.</p>
          
          <h3>8. Lei Aplicável</h3>
          <p>Estes Termos de Uso são regidos pelas leis do Brasil. Qualquer disputa relacionada a estes termos será resolvida nos tribunais competentes do Brasil.</p>
        </div>
        <div class="policy-modal-footer">
          <button class="btn-accept" @click="closeModal">Aceito os Termos</button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'AppFooter',
  setup() {
    const activeModal = ref(null);
    
    const showModal = (modalType) => {
      activeModal.value = modalType;
      document.body.style.overflow = 'hidden';
    };
    
    const closeModal = () => {
      activeModal.value = null;
      document.body.style.overflow = '';
    };
    
    // Handler para os eventos globais
    const handleShowPrivacyPolicy = () => showModal('privacy');
    const handleShowTerms = () => showModal('terms');
    
    onMounted(() => {
      // Registrar os listeners de eventos globais
      window.addEventListener('show-privacy-policy', handleShowPrivacyPolicy);
      window.addEventListener('show-terms', handleShowTerms);
      
      // Listener para fechamento com ESC
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && activeModal.value) {
          closeModal();
        }
      });
    });
    
    onUnmounted(() => {
      // Remover os listeners ao desmontar o componente
      window.removeEventListener('show-privacy-policy', handleShowPrivacyPolicy);
      window.removeEventListener('show-terms', handleShowTerms);
    });
    
    return {
      activeModal,
      showModal,
      closeModal
    };
  }
};
</script>

<style scoped>
/* Estilos do rodapé fixo */
.app-footer {
  background-color: #2c2c2c;
  border-top: 1px solid #444;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: var(--z-index-footer);
}

.container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  max-width: 75rem; /* Convertido de 1200px para rem */
  margin: 0 auto;
  padding: var(--spacing-sm) var(--spacing-md);
}

.app-footer p {
  margin: 0;
  font-size: var(--font-size-sm);
  color: #aaa;
}

.footer-links {
  list-style: none;
  display: flex;
  gap: var(--spacing-md);
  margin: 0;
  padding: 0;
}

.footer-links li a {
  color: #ccc;
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: color 0.3s ease;
}

.footer-links li a:hover {
  color: #fff;
}

/* Estilos do Modal - mantendo padrão do AppLogin */
.policy-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-index-modal);
  padding: var(--spacing-md);
}

.policy-modal-content {
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  border-radius: var(--border-radius-lg);
  max-width: 50rem; /* Convertido de 800px para rem */
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 0.625rem 1.875rem rgba(0, 0, 0, 0.5);
  animation: modalFadeIn 0.3s ease;
}

.policy-modal-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid #444;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.policy-modal-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  color: #fff;
}

.close-modal {
  background: none;
  border: none;
  color: #ccc;
  font-size: var(--font-size-xxl);
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-modal:hover {
  color: #fff;
}

.policy-modal-body {
  padding: var(--spacing-md);
  overflow-y: auto;
  flex: 1;
}

.policy-modal-body h3 {
  font-size: var(--font-size-lg);
  margin: var(--spacing-md) 0 var(--spacing-xs);
  color: #eee;
}

.policy-modal-body h3:first-child {
  margin-top: 0;
}

.policy-modal-body p {
  font-size: var(--font-size-md);
  line-height: 1.6;
  color: #ccc;
  margin-bottom: var(--spacing-md);
}

.policy-modal-body ul {
  padding-left: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.policy-modal-body li {
  margin-bottom: var(--spacing-xs);
  color: #ccc;
}

.policy-modal-footer {
  padding: var(--spacing-sm) var(--spacing-md);
  border-top: 1px solid #444;
  display: flex;
  justify-content: flex-end;
}

.btn-accept {
  padding: var(--spacing-xs) var(--spacing-md);
  background: linear-gradient(145deg, #3b3b3b, #2c2c2c);
  color: #fff;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-md);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-accept:hover {
  background: linear-gradient(145deg, #444, #333);
  transform: translateY(-0.125rem); /* Convertido de -2px para rem */
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-1.25rem); /* Convertido de -20px para rem */
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsividade */
@media (max-width: 1024px) {
  .container {
    padding: 0.75rem var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .policy-modal-content {
    max-width: 95%;
  }
  
  .policy-modal-header h2 {
    font-size: var(--font-size-lg);
  }
  
  .policy-modal-body h3 {
    font-size: var(--font-size-md);
  }
  
  .policy-modal-body p, 
  .policy-modal-body li {
    font-size: var(--font-size-sm);
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0.5rem var(--spacing-xs);
  }
  
  .app-footer p, 
  .footer-links li a {
    font-size: var(--font-size-xs);
  }
  
  .footer-links {
    gap: 0.9375rem; /* Convertido de 15px para rem */
  }
  
  .policy-modal-header {
    padding: var(--spacing-sm);
  }
  
  .policy-modal-body {
    padding: var(--spacing-sm);
  }
  
  .policy-modal-header h2 {
    font-size: var(--font-size-md);
  }
  
  .policy-modal-body h3 {
    font-size: var(--font-size-sm);
  }
  
  .policy-modal-body p, 
  .policy-modal-body li {
    font-size: var(--font-size-xs);
  }
  
  .btn-accept {
    padding: 0.5rem 1rem;
    font-size: var(--font-size-sm);
  }
}
</style>
