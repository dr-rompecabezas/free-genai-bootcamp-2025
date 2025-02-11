import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { path: '/dashboard', replace: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/study-activities',
      name: 'study-activities',
      component: () => import('@/views/StudyActivities.vue')
    },
    {
      path: '/study-activities/:id',
      name: 'study-activity',
      component: () => import('@/views/StudyActivityShow.vue')
    },
    {
      path: '/study-activities/:id/launch',
      name: 'study-activity-launch',
      component: () => import('@/views/StudyActivityLaunch.vue')
    },
    {
      path: '/words',
      name: 'words',
      component: () => import('@/views/Words.vue')
    },
    {
      path: '/words/:id',
      name: 'word',
      component: () => import('@/views/WordShow.vue')
    },
    {
      path: '/groups',
      name: 'groups',
      component: () => import('@/views/Groups.vue')
    },
    {
      path: '/groups/:id',
      name: 'group',
      component: () => import('@/views/GroupShow.vue')
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('@/views/Sessions.vue')
    },
    {
      path: '/sessions/:id',
      name: 'session',
      component: () => import('@/views/StudySessionShow.vue')
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings.vue')
    }
  ]
})
