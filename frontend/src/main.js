import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';  
import 'vue-toastification/dist/index.css';  


// Configuração do Axios de forma global (importação simplificada)
import axios from 'axios';

// Configuração global do axios
axios.defaults.baseURL = 'http://localhost:8000/api';

const app = createApp(App);

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
