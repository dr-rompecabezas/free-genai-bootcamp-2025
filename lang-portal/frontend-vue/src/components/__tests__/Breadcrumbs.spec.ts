import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { router } from '@/router'
import Breadcrumbs from '../Breadcrumbs.vue'
import { useNavigationStore } from '@/stores/navigation'

describe('Breadcrumbs', () => {
  beforeEach(() => {
    const pinia = createPinia()
    const navigationStore = useNavigationStore(pinia)
    navigationStore.$reset()
  })

  it('renders dashboard breadcrumb for root path', async () => {
    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router, createPinia()]
      }
    })

    await router.push('/')
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Dashboard')
    expect(wrapper.find('[data-testid="breadcrumb-page"]').text()).toBe('Dashboard')
  })

  it('renders multiple levels of breadcrumbs', async () => {
    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router, createPinia()]
      }
    })

    await router.push('/study-activities')
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Study Activities')
    expect(wrapper.findAll('[data-testid="breadcrumb-page"]')).toHaveLength(1)
  })

  it('shows entity name when available', async () => {
    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router, createPinia()]
      }
    })

    const navigationStore = useNavigationStore()
    navigationStore.setCurrentGroup({
      id: 1,
      group_name: 'JLPT N5 Kanji'
    })

    await router.push('/groups/1')
    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('JLPT N5 Kanji')
    expect(wrapper.find('[data-testid="breadcrumb-page"]').text()).toBe('JLPT N5 Kanji')
  })
})
