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
      <TableRow v-for="session in sessions" :key="session.id">
        <TableCell>
          <RouterLink
            :to="`/sessions/${session.id}`"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            {{ session.id }}
          </RouterLink>
        </TableCell>
        <TableCell>
          <RouterLink
            :to="`/study-activities/${session.activity_id}`"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            {{ session.activity_name }}
          </RouterLink>
        </TableCell>
        <TableCell>
          <RouterLink
            :to="`/groups/${session.group_id}`"
            class="text-blue-600 dark:text-blue-400 hover:underline"
          >
            {{ session.group_name }}
          </RouterLink>
        </TableCell>
        <TableCell>{{ session.start_time }}</TableCell>
        <TableCell>{{ session.end_time }}</TableCell>
        <TableCell>{{ session.review_items_count }}</TableCell>
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

export type StudySessionSortKey = 'id' | 'activity_name' | 'group_name' | 'start_time' | 'end_time' | 'review_items_count'

interface StudySession {
  id: number
  activity_id: number
  activity_name: string
  group_id: number
  group_name: string
  start_time: string
  end_time: string
  review_items_count: number
}

const props = defineProps<{
  sessions: StudySession[]
  sortKey: StudySessionSortKey
  sortDirection: 'asc' | 'desc'
  onSort: (key: StudySessionSortKey) => void
}>()

const sortableColumns = ['id', 'activity_name', 'group_name', 'start_time', 'end_time', 'review_items_count'] as const

function formatColumnName(key: string): string {
  if (key === 'review_items_count') {
    return '# Review Items'
  }
  return key.replace(/_([a-z])/g, ' $1').trim()
}
</script>
