import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HRPanel from '../views/HRPanel.vue'
import CandidateInterview from '../views/CandidateInterview.vue'
import VacanciesList from '../views/VacanciesList.vue'
import VacancyForm from '../views/VacancyForm.vue'
import VacancyDetail from '../views/VacancyDetail.vue'
import ModelStatus from '../views/ModelStatus.vue'

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
      path: '/vacancies',
      name: 'vacancies-list',
      component: VacanciesList
    },
    {
      path: '/vacancies/create',
      name: 'vacancy-create',
      component: VacancyForm
    },
    {
      path: '/vacancies/:id',
      name: 'vacancy-detail',
      component: VacancyDetail
    },
    {
      path: '/vacancies/:id/edit',
      name: 'vacancy-edit',
      component: VacancyForm
    },
    {
      path: '/interview/:sessionId?',
      name: 'candidate-interview',
      component: CandidateInterview
    },
    {
      path: '/model-status',
      name: 'model-status',
      component: ModelStatus
    }
  ]
})

export default router
