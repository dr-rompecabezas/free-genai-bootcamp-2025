import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import Sidebar from '../Sidebar.vue'
import { router } from '@/router'

describe('Sidebar', () => {
  it('renders all navigation items', () => {
    const wrapper = mount(Sidebar, {
      global: {
        plugins: [router]
      }
    })

    const navItems = [
      'Dashboard',
      'Study Activities',
      'Words',
      'Word Groups',
      'Sessions',
      'Settings'
    ]

    navItems.forEach(item => {
      expect(wrapper.text()).toContain(item)
    })
  })

  it('marks the current route as active', async () => {
    const wrapper = mount(Sidebar, {
      global: {
        plugins: [router]
      }
    })

    await router.push('/dashboard')
    await wrapper.vm.$nextTick()

    const dashboardLink = wrapper.find('[data-testid="nav-item-dashboard"]')
    expect(dashboardLink.classes()).toContain('bg-primary/10')
  })

  it('handles nested routes correctly', async () => {
    const wrapper = mount(Sidebar, {
      global: {
        plugins: [router]
      }
    })

    await router.push('/study-activities/1')
    await wrapper.vm.$nextTick()

    const studyActivitiesLink = wrapper.find('[data-testid="nav-item-study-activities"]')
    expect(studyActivitiesLink.classes()).toContain('bg-primary/10')
  })
})
