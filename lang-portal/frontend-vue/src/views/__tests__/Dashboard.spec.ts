import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import { useStatsStore } from '@/stores/stats'

// Mock API responses
const mockRecentSession = {
  id: 1,
  group_id: 1,
  activity_name: 'Vocabulary Review',
  created_at: '2025-02-10T22:00:00Z',
  correct_count: 8,
  wrong_count: 2
}

const mockStats = {
  total_vocabulary: 1000,
  total_words_studied: 500,
  mastered_words: 200,
  success_rate: 0.8,
  total_sessions: 50,
  active_groups: 5,
  current_streak: 7
}

// Create a mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/study-session/:id',
      name: 'study-session',
      component: { template: '<div>Study Session</div>' }
    }
  ]
})

describe('Dashboard', () => {
  beforeEach(() => {
    vi.mock('@/services/api', () => ({
      fetchRecentStudySession: vi.fn().mockResolvedValue(mockRecentSession),
      fetchStudyStats: vi.fn().mockResolvedValue(mockStats)
    }))
  })

  it('renders dashboard stats correctly', async () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              stats: {
                recentSession: mockRecentSession,
                stats: mockStats,
                isLoading: false
              }
            }
          }),
          router
        ]
      }
    })

    // Wait for component to load data
    await wrapper.vm.$nextTick()

    // Verify stats are displayed
    expect(wrapper.text()).toContain('Total Vocabulary')
    expect(wrapper.text()).toContain('1000')
    expect(wrapper.text()).toContain('Mastered Words')
    expect(wrapper.text()).toContain('200')
    expect(wrapper.text()).toContain('Success Rate')
    expect(wrapper.text()).toContain('80%')

    // Verify recent session is displayed
    expect(wrapper.text()).toContain('Vocabulary Review')
    expect(wrapper.text()).toContain('8 correct')
    expect(wrapper.text()).toContain('2 wrong')
  })

  it('shows loading state', () => {
    const wrapper = mount(Dashboard, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              stats: {
                recentSession: null,
                stats: null,
                isLoading: true
              }
            }
          }),
          router
        ]
      }
    })

    expect(wrapper.find('[data-test="loading"]').exists()).toBe(true)
  })

  it('shows error state when API fails', async () => {
    vi.mock('@/services/api', () => ({
      fetchRecentStudySession: vi.fn().mockRejectedValue(new Error('API Error')),
      fetchStudyStats: vi.fn().mockRejectedValue(new Error('API Error'))
    }))

    const wrapper = mount(Dashboard, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              stats: {
                recentSession: null,
                stats: null,
                isLoading: false,
                error: 'Failed to load dashboard data'
              }
            }
          }),
          router
        ]
      }
    })

    await wrapper.vm.$nextTick()
    expect(wrapper.find('[data-test="error"]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Failed to load dashboard data')
  })
})
