import { createRouter, createWebHistory } from 'vue-router';
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
      if (!token || !(await isTokenValid())) {
        next({ name: 'Login' });
      } else {
        
        next();
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;