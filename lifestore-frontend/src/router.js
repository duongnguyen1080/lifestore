import { createRouter, createWebHistory } from 'vue-router'
import LearnMore from './components/LearnMore.vue'
import AppHome from './components/AppHome.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: AppHome
  },
  {
    path: '/learn-more/:authorInfo/:userQuestion/:quote',
    name: 'LearnMore',
    component: LearnMore,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router