import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../modules/dashboard/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/models',
      name: 'models',
      component: () => import('../modules/models/views/ModelsView.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../modules/settings/views/SettingsView.vue')
    }
  ]
})

export default router
