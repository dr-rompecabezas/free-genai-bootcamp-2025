<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Study Sessions</h1>

    <div v-if="isLoading" class="text-center py-4">Loading...</div>
    
    <div v-else-if="error" class="text-red-500 text-center py-4">{{ error }}</div>
    
    <template v-else>
      <StudySessionsTable
        :sessions="sortedSessions"
        :sort-key="sortKey"
        :sort-direction="sortDirection"
        :onSort="handleSort"
      />

      <div class="flex justify-center space-x-2">
        <button
          v-for="page in totalPages"
          :key="page"
          class="px-3 py-1 rounded"
          :class="{
            'bg-blue-500 text-white': page === currentPage,
            'bg-gray-200 text-gray-700 hover:bg-gray-300': page !== currentPage
          }"
          @click="currentPage = page"
        >
          {{ page }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import StudySessionsTable, { type StudySessionSortKey } from '@/components/StudySessionsTable.vue'
import { fetchStudySessions } from '@/services/api'

const sessions = ref([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const sortKey = ref<StudySessionSortKey>('start_time')
const sortDirection = ref<'asc' | 'desc'>('desc')
const currentPage = ref(1)
const totalPages = ref(1)
const itemsPerPage = 10

const sortedSessions = computed(() => {
  return [...sessions.value].sort((a, b) => {
    const aValue = a[sortKey.value.toLowerCase()]
    const bValue = b[sortKey.value.toLowerCase()]
    if (aValue < bValue) return sortDirection.value === 'asc' ? -1 : 1
    if (aValue > bValue) return sortDirection.value === 'asc' ? 1 : -1
    return 0
  })
})

async function loadSessions() {
  isLoading.value = true
  error.value = null
  try {
    const response = await fetchStudySessions(currentPage.value, itemsPerPage)
    sessions.value = response.items
    totalPages.value = response.total_pages
  } catch (err) {
    error.value = 'Failed to load sessions'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function handleSort(key: StudySessionSortKey) {
  if (key === sortKey.value) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDirection.value = 'asc'
  }
}

watch([currentPage], () => {
  loadSessions()
})

onMounted(() => {
  loadSessions()
})
</script>
