import { createRouter, createWebHashHistory } from 'vue-router';
import AppHome from '@/views/AppHome.vue';
import AppLogin from '@/views/AppLogin.vue';
import AppContato from '@/views/AppContato.vue';
import AppAjuda from '@/views/AppAjuda.vue';
import AppMenu from '@/views/AppMenu.vue';
import AppMenuLayout from '@/views/AppMenuLayout.vue';
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
      const token = localStorage.getItem('access_token');
      if (token && (await isTokenValid())) {
        next({ name: 'Menu' });
      } else {
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
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        next({ name: 'Login' });
        return;
      }
      
      const isValid = await isTokenValid();
      
      if (!isValid) {
        next({ name: 'Login' });
        return;
      }
      
      const user = JSON.parse(localStorage.getItem('user'));
      
      if (user) {
        next();
      } else {
        next({ name: 'Login' });
      }
    },
  },
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Comportamento de rolagem suave
    if (savedPosition) {
      return {
        ...savedPosition,
        behavior: 'smooth',
      }
    } else {
      return { 
        top: 0,
        behavior: 'smooth',
      }
    }
  }
});

export default router;
