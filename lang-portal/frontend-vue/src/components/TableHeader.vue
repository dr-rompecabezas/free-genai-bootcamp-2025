<template>
  <th
    class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800"
    @click="onClick"
  >
    <div class="flex items-center space-x-1">
      <span><slot></slot></span>
      <template v-if="currentSortKey === sortKey">
        <ChevronUp v-if="sortDirection === 'asc'" class="w-4 h-4" />
        <ChevronDown v-else class="w-4 h-4" />
      </template>
    </div>
  </th>
</template>

<script setup lang="ts">
import { ChevronUp, ChevronDown } from 'lucide-vue-next'

defineProps<{
  sortKey: string
  currentSortKey: string
  sortDirection: 'asc' | 'desc'
  onClick: () => void
}>()
</script>
