<template>
  <div class="space-y-4">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Words</h1>

    <div v-if="isLoading" class="text-center py-4">Loading...</div>
    
    <div v-else-if="error" class="text-red-500 text-center py-4">{{ error }}</div>
    
    <template v-else>
      <WordsTable
        :words="words"
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
import { ref, onMounted, watch } from 'vue'
import WordsTable, { type WordSortKey } from '@/components/WordsTable.vue'
import { fetchWords } from '@/services/api'

const words = ref([])
const isLoading = ref(false)
const error = ref<string | null>(null)
const sortKey = ref<WordSortKey>('kanji')
const sortDirection = ref<'asc' | 'desc'>('asc')
const currentPage = ref(1)
const totalPages = ref(1)

async function loadWords() {
  isLoading.value = true
  error.value = null
  try {
    const response = await fetchWords(currentPage.value, sortKey.value, sortDirection.value)
    words.value = response.words
    totalPages.value = response.total_pages
  } catch (err) {
    error.value = 'Failed to load words'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function handleSort(key: WordSortKey) {
  if (key === sortKey.value) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDirection.value = 'asc'
  }
}

watch([currentPage, sortKey, sortDirection], () => {
  loadWords()
})

onMounted(() => {
  loadWords()
})
</script>
