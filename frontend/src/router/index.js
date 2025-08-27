import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HRPanel from '../views/HRPanel.vue'
import CandidateInterview from '../views/CandidateInterview.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/hr',
      name: 'hr-panel',
      component: HRPanel
    },
    {
      path: '/interview/:sessionId?',
      name: 'candidate-interview',
      component: CandidateInterview
    }
  ]
})

export default router
