import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/room/:id',
    name: 'room',
    component: () => import('../views/RoomChatView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to) => {

  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const username = localStorage.getItem('username');

  if (authRequired && !username) {
      alert('User not authenticated!');
      return '/login';
  }
});

export default router
