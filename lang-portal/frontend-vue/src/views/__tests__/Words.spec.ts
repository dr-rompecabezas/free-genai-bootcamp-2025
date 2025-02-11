import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { nextTick } from 'vue'
import Words from '../Words.vue'
import { router } from '@/router'
import { fetchWords } from '@/services/api'

vi.mock('@/services/api', () => ({
  fetchWords: vi.fn().mockResolvedValue({
    words: [
      {
        id: 1,
        kanji: '日',
        romaji: 'hi',
        english: 'sun',
        correct_count: 5,
        wrong_count: 2
      }
    ],
    total_pages: 1
  })
}))

describe('Words', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders words table with data', async () => {
    const wrapper = mount(Words, {
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

    expect(wrapper.text()).toContain('Words')
    expect(wrapper.find('table').exists()).toBe(true)
    expect(wrapper.text()).toContain('日')
    expect(wrapper.text()).toContain('hi')
    expect(wrapper.text()).toContain('sun')
  })

  it('handles sorting', async () => {
    const wrapper = mount(Words, {
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

    // Click on kanji header to sort
    await wrapper.find('th').trigger('click')

    // Verify sort state changed
    expect(wrapper.vm.sortDirection).toBe('desc')
  })

  it('shows loading state', async () => {
    vi.mocked(fetchWords).mockImplementationOnce(() => new Promise(() => {}))

    const wrapper = mount(Words, {
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
    vi.mocked(fetchWords).mockRejectedValueOnce(new Error('API Error'))

    const wrapper = mount(Words, {
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

    expect(wrapper.text()).toContain('Failed to load words')
  })
})
