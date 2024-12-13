import { createRouter, createWebHistory } from 'vue-router'
import LearnMore from './components/LearnMore.vue'
import AppHome from './components/AppHome.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: AppHome,
    meta: { preserveState: true }
  },
  {
    path: '/learn-more',
    name: 'LearnMore',
    component: LearnMore,
    meta: { preserveState: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

let savedState = null;

router.beforeEach((to, from, next) => {
  console.log('Router guard triggered:', {
    to: to.name,
    from: from.name,
    homeComponent: from.matched[0]?.instances?.default,
    savedState: router._savedState
  });

  if (from.name === 'Home' && to.name === 'LearnMore') {
    const homeComponent = from.matched[0].instances.default;
    if (homeComponent) {
      router._savedState = {
        quotes: homeComponent.quotes,
        question: homeComponent.question
      };
      console.log('State saved:', router._savedState);
    }
  }
  next();
});

export default router 