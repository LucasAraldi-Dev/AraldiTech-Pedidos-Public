import { createRouter, createWebHashHistory } from 'vue-router';
import AppHome from '@/views/AppHome.vue';
import AppLogin from '@/views/AppLogin.vue';
import AppContato from '@/views/AppContato.vue';
import AppAjuda from '@/views/AppAjuda.vue';
import AppMenu from '@/views/AppMenu.vue';
import AppMenuLayout from '@/views/AppMenuLayout.vue';
import AppLoading from '@/views/AppLoading.vue';
import { isTokenValid } from '@/utils/isTokenValid';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: AppHome,
  },
  {
    path: '/login',
    name: 'Login',
    component: AppLogin,
    beforeEnter: async (to, from, next) => {
      console.log("Navegando para login, verificando token...");
      const token = localStorage.getItem('access_token');
      if (token && (await isTokenValid())) {
        console.log("Token válido encontrado, redirecionando para Menu");
        next({ name: 'Menu' });
      } else {
        console.log("Nenhum token válido, continuando para login");
        next();
      }
    },
  },
  {
    path: '/contato',
    name: 'Contato',
    component: AppContato,
  },
  {
    path: '/ajuda',
    name: 'Ajuda',
    component: AppAjuda,
  },
  {
    path: '/politica-privacidade',
    name: 'PoliticaPrivacidade',
    component: AppHome,
    beforeEnter: (to, from, next) => {
      // Abrir modal de política de privacidade via evento global
      next(false); // Impede a navegação
      // Uso de setTimeout para garantir que a emissão do evento aconteça após o cancelamento da navegação
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('show-privacy-policy'));
      }, 100);
    }
  },
  {
    path: '/termos-uso',
    name: 'TermosUso',
    component: AppHome,
    beforeEnter: (to, from, next) => {
      // Abrir modal de termos de uso via evento global
      next(false); // Impede a navegação
      // Uso de setTimeout para garantir que a emissão do evento aconteça após o cancelamento da navegação
      setTimeout(() => {
        window.dispatchEvent(new CustomEvent('show-terms'));
      }, 100);
    }
  },
  {
    path: '/loading',
    name: 'Loading',
    component: AppLoading,
    beforeEnter: (to, from, next) => {
      // Permitir acesso da página de login ou após uma autenticação bem-sucedida
      const token = localStorage.getItem('access_token');
      if (from.name === 'Login' || token) {
        next();
      } else {
        next({ name: 'Login' });
      }
    }
  },
  {
    path: '/menu',
    component: AppMenuLayout,
    children: [
      {
        path: '',
        name: 'Menu',
        component: AppMenu,
      },
    ],
    beforeEnter: async (to, from, next) => {
      console.log("Navegando para menu, verificando autenticação...");
      const token = localStorage.getItem('access_token');
      console.log("Token encontrado:", token ? "Sim" : "Não");
      
      if (!token) {
        console.log("Token não encontrado, redirecionando para login");
        next({ name: 'Login' });
        return;
      }
      
      const isValid = await isTokenValid();
      console.log("Token é válido:", isValid ? "Sim" : "Não");
      
      if (!isValid) {
        console.log("Token inválido, redirecionando para login");
        next({ name: 'Login' });
        return;
      }
      
      const user = JSON.parse(localStorage.getItem('user'));
      console.log("Usuário recuperado do localStorage:", user);
      
      if (user) {
        console.log("Usuário encontrado, permitindo acesso ao menu");
        next();
      } else {
        console.warn("Dados de usuário não encontrados no localStorage");
        next({ name: 'Login' }); // Redirecione para login se o usuário não for válido
      }
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
