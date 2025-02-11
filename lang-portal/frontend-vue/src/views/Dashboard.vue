<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Dashboard</h1>
    </div>

    <div v-if="isLoading" data-test="loading" class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 3" :key="i" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 animate-pulse">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-4"></div>
        <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
      </div>
    </div>

    <div v-else-if="error" data-test="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-600 dark:text-red-400">
      {{ error }}
    </div>

    <template v-else>
      <div class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        <!-- Total Vocabulary -->
        <DashboardCard title="Total Vocabulary" :icon="BookOpen">
          <div class="text-3xl font-bold">{{ stats?.total_vocabulary || 0 }}</div>
          <div class="text-sm text-gray-500">words in your collection</div>
        </DashboardCard>

        <!-- Mastered Words -->
        <DashboardCard title="Mastered Words" :icon="Trophy">
          <div class="text-3xl font-bold">{{ stats?.mastered_words || 0 }}</div>
          <div class="text-sm text-gray-500">words mastered</div>
        </DashboardCard>

        <!-- Success Rate -->
        <DashboardCard title="Success Rate" :icon="Activity">
          <div class="text-3xl font-bold">{{ (stats?.success_rate || 0) * 100 }}%</div>
          <div class="text-sm text-gray-500">correct answers</div>
        </DashboardCard>
      </div>

      <!-- Recent Session -->
      <DashboardCard v-if="recentSession" title="Recent Study Session" :icon="Clock">
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <div>
              <div class="font-medium">{{ recentSession.activity_name }}</div>
              <div class="text-sm text-gray-500">
                {{ new Date(recentSession.created_at).toLocaleDateString() }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-green-600">{{ recentSession.correct_count }} correct</div>
              <div class="text-red-600">{{ recentSession.wrong_count }} wrong</div>
            </div>
          </div>
          <RouterLink
            :to="{ name: 'study-session', params: { id: recentSession.id }}"
            class="inline-flex items-center text-blue-600 hover:text-blue-800"
          >
            View Details
            <ArrowRight class="w-4 h-4 ml-1" />
          </RouterLink>
        </div>
      </DashboardCard>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { BookOpen, Trophy, Clock, ArrowRight, Activity } from 'lucide-vue-next'
import { useStatsStore } from '@/stores/stats'
import DashboardCard from './DashboardCard.vue'

const store = useStatsStore()
const { recentSession, stats, isLoading, error } = store

onMounted(() => {
  store.loadDashboardData()
})
</script>
