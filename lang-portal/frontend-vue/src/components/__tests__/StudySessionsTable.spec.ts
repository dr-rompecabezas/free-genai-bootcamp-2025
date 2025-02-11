import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import StudySessionsTable from '../StudySessionsTable.vue'
import { router } from '@/router'

const testSessions = [
  {
    id: 1,
    activity_id: 1,
    activity_name: 'JLPT N5 Review',
    group_id: 1,
    group_name: 'JLPT N5 Kanji',
    start_time: '2025-02-11T09:00:00Z',
    end_time: '2025-02-11T09:30:00Z',
    review_items_count: 20
  },
  {
    id: 2,
    activity_id: 2,
    activity_name: 'Daily Kanji',
    group_id: 2,
    group_name: 'Common Use Kanji',
    start_time: '2025-02-11T10:00:00Z',
    end_time: '2025-02-11T10:15:00Z',
    review_items_count: 15
  }
]

describe('StudySessionsTable', () => {
  it('renders all sessions with correct data', () => {
    const wrapper = mount(StudySessionsTable, {
      props: {
        sessions: testSessions,
        sortKey: 'id',
        sortDirection: 'asc',
        onSort: () => {}
      },
      global: {
        plugins: [router]
      }
    })

    // Check if all session data is rendered
    testSessions.forEach(session => {
      expect(wrapper.text()).toContain(session.id.toString())
      expect(wrapper.text()).toContain(session.activity_name)
      expect(wrapper.text()).toContain(session.group_name)
      expect(wrapper.text()).toContain(session.review_items_count.toString())
    })
  })

  it('calls onSort when header is clicked', async () => {
    const onSort = vi.fn()
    const wrapper = mount(StudySessionsTable, {
      props: {
        sessions: testSessions,
        sortKey: 'id',
        sortDirection: 'asc',
        onSort
      },
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('th').trigger('click')
    expect(onSort).toHaveBeenCalledWith('id')
  })

  it('shows sort direction indicator', () => {
    const wrapper = mount(StudySessionsTable, {
      props: {
        sessions: testSessions,
        sortKey: 'id',
        sortDirection: 'asc',
        onSort: () => {}
      },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.find('svg').exists()).toBe(true)
  })

  it('renders links to related entities', () => {
    const wrapper = mount(StudySessionsTable, {
      props: {
        sessions: testSessions,
        sortKey: 'id',
        sortDirection: 'asc',
        onSort: () => {}
      },
      global: {
        plugins: [router]
      }
    })

    const session = testSessions[0]
    
    // Check session link
    const sessionLink = wrapper.find(`a[href="/sessions/${session.id}"]`)
    expect(sessionLink.exists()).toBe(true)
    expect(sessionLink.text()).toBe(session.id.toString())

    // Check activity link
    const activityLink = wrapper.find(`a[href="/study-activities/${session.activity_id}"]`)
    expect(activityLink.exists()).toBe(true)
    expect(activityLink.text()).toBe(session.activity_name)

    // Check group link
    const groupLink = wrapper.find(`a[href="/groups/${session.group_id}"]`)
    expect(groupLink.exists()).toBe(true)
    expect(groupLink.text()).toBe(session.group_name)
  })
})
