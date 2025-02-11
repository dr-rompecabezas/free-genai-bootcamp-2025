import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { nextTick } from 'vue'
import Sessions from '../Sessions.vue'
import { router } from '@/router'
import { fetchStudySessions } from '@/services/api'

vi.mock('@/services/api', () => ({
  fetchStudySessions: vi.fn().mockResolvedValue({
    items: [
      {
        id: 1,
        activity_id: 1,
        activity_name: 'JLPT N5 Review',
        group_id: 1,
        group_name: 'JLPT N5 Kanji',
        start_time: '2025-02-11T09:00:00Z',
        end_time: '2025-02-11T09:30:00Z',
        review_items_count: 20
      }
    ],
    total_pages: 1
  })
}))

describe('Sessions', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders sessions table with data', async () => {
    const wrapper = mount(Sessions, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    await nextTick()
    await nextTick()

    expect(wrapper.text()).toContain('Study Sessions')
    expect(wrapper.find('table').exists()).toBe(true)
    expect(wrapper.text()).toContain('JLPT N5 Review')
    expect(wrapper.text()).toContain('JLPT N5 Kanji')
    expect(wrapper.text()).toContain('20')
  })

  it('handles sorting', async () => {
    const wrapper = mount(Sessions, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    await nextTick()
    await nextTick()

    // Click on activity name header twice to sort desc
    await wrapper.find('th:nth-child(2)').trigger('click')
    await wrapper.find('th:nth-child(2)').trigger('click')

    // Verify sort state changed
    expect(wrapper.vm.sortDirection).toBe('desc')
  })

  it('shows loading state', async () => {
    vi.mocked(fetchStudySessions).mockImplementationOnce(() => new Promise(() => {}))

    const wrapper = mount(Sessions, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    await nextTick()

    expect(wrapper.text()).toContain('Loading')
  })

  it('shows error state', async () => {
    vi.mocked(fetchStudySessions).mockRejectedValueOnce(new Error('API Error'))

    const wrapper = mount(Sessions, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    await nextTick()
    await nextTick()

    expect(wrapper.text()).toContain('Failed to load sessions')
  })

  it('handles pagination', async () => {
    const wrapper = mount(Sessions, {
      global: {
        plugins: [
          router,
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    await nextTick()
    await nextTick()

    // Set total pages to 2 to ensure pagination button exists
    wrapper.vm.totalPages = 2

    await nextTick()

    // Click on page 2
    await wrapper.find('button:nth-child(2)').trigger('click')

    expect(wrapper.vm.currentPage).toBe(2)
  })
})
