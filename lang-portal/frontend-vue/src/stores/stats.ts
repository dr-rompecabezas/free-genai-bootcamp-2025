import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchRecentStudySession, fetchStudyStats } from '@/services/api'
import type { RecentSession, StudyStats } from '@/types'

export const useStatsStore = defineStore('stats', () => {
  const recentSession = ref<RecentSession | null>(null)
  const stats = ref<StudyStats | null>(null)
  const isLoading = ref(true)
  const error = ref<string | null>(null)

  async function loadDashboardData() {
    isLoading.value = true
    error.value = null
    
    try {
      const [sessionData, statsData] = await Promise.all([
        fetchRecentStudySession(),
        fetchStudyStats()
      ])
      recentSession.value = sessionData
      stats.value = statsData
    } catch (err) {
      error.value = 'Failed to load dashboard data'
      console.error('Failed to load dashboard data:', err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    recentSession,
    stats,
    isLoading,
    error,
    loadDashboardData
  }
})
