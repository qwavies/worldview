import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import CompareView from '../views/CompareView.vue'
import SubmissionView from '../views/SubmissionView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: LandingView
    },
    {
      path: '/compare',
      component: CompareView,
      meta: { transition: 'fade' }
    },
    {
      path: '/submission',
      component: SubmissionView
    }
  ]
})

export default router
