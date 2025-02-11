<template>
  <Table>
    <thead class="bg-gray-50 dark:bg-gray-900">
      <tr>
        <TableHeader
          v-for="key in sortableColumns"
          :key="key"
          :sort-key="key"
          :current-sort-key="sortKey"
          :sort-direction="sortDirection"
          :onClick="() => onSort(key)"
        >
          {{ formatColumnName(key) }}
        </TableHeader>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:divide-gray-700">
      <TableRow v-for="word in words" :key="word.id">
        <TableCell>
          <RouterLink
            :to="`/words/${word.id}`"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            {{ word.kanji }}
          </RouterLink>
        </TableCell>
        <TableCell>{{ word.romaji }}</TableCell>
        <TableCell>{{ word.english }}</TableCell>
        <TableCell class="text-green-500 dark:text-green-400">
          {{ word.correct_count }}
        </TableCell>
        <TableCell class="text-red-500 dark:text-red-400">
          {{ word.wrong_count }}
        </TableCell>
      </TableRow>
    </tbody>
  </Table>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Table from './Table.vue'
import TableHeader from './TableHeader.vue'
import TableRow from './TableRow.vue'
import TableCell from './TableCell.vue'

export type WordSortKey = 'kanji' | 'romaji' | 'english' | 'correct_count' | 'wrong_count'

interface Word {
  id: number
  kanji: string
  romaji: string
  english: string
  correct_count: number
  wrong_count: number
}

const props = defineProps<{
  words: Word[]
  sortKey: WordSortKey
  sortDirection: 'asc' | 'desc'
  onSort: (key: WordSortKey) => void
}>()

const sortableColumns = ['kanji', 'romaji', 'english', 'correct_count', 'wrong_count'] as const

function formatColumnName(key: string): string {
  switch (key) {
    case 'correct_count':
      return 'Correct'
    case 'wrong_count':
      return 'Wrong'
    default:
      return key.charAt(0).toUpperCase() + key.slice(1)
  }
}
</script>
