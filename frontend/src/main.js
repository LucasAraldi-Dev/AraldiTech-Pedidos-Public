import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';  
import 'vue-toastification/dist/index.css';  
import { inicializarProtecoesSeguranca, sanitizeHtml } from './utils/securityService';
// Importando estilos de responsividade globais
import './assets/responsive.css';

// Configuração do Axios de forma global (importação simplificada)
import axios from 'axios';

// Configuração global do axios
axios.defaults.baseURL = 'http://localhost:8000/api';

const app = createApp(App);

// Diretiva global para sanitização de XSS
app.directive('sanitize', {
  mounted(el, binding) {
    // Aplicar sanitização ao conteúdo do elemento
    const value = binding.value !== undefined ? binding.value : el.innerText;
    el.innerText = sanitizeHtml(value);
  },
  updated(el, binding) {
    // Atualizar a sanitização quando o valor mudar
    const value = binding.value !== undefined ? binding.value : el.innerText;
    el.innerText = sanitizeHtml(value);
  }
});

// Criando propriedade global para sanitização
app.config.globalProperties.$sanitize = sanitizeHtml;

// Configuração global do Vue Toastification
const options = {
  position: 'top-center',  // Colocando as notificações no topo e centralizadas
  timeout: 2500,  // Duração da notificação em ms
  // closeButton: true, // Removido para evitar erro de VNode
  pauseOnFocusLoss: true,  // Pausa a notificação quando a página perde foco
  pauseOnHover: true,  // Pausa a notificação ao passar o mouse sobre ela
};

app.use(Toast, options);  // Usando o Toast no Vue

app.use(router);
app.mount('#app');

// Inicializar proteções de segurança
inicializarProtecoesSeguranca().catch(error => {
  // Silenciar erros de inicialização em produção
  if (process.env.NODE_ENV === 'development') {
    console.error('Erro na inicialização de proteções de segurança:', error);
  }
});
