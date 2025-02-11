<template>
  <header class="flex h-16 shrink-0 items-center gap-2 border-b px-4">
    <!-- Sidebar trigger button -->
    <button class="-ml-1 p-2 hover:bg-muted rounded-lg">
      <Menu class="h-4 w-4" />
    </button>

    <!-- Separator -->
    <div class="mr-2 h-4 w-px bg-border" />

    <!-- Breadcrumbs -->
    <nav aria-label="Breadcrumb">
      <ol class="flex items-center gap-1.5">
        <template v-for="(item, index) in breadcrumbItems" :key="item.path">
          <li class="flex items-center gap-1.5">
            <template v-if="index === breadcrumbItems.length - 1">
              <span
                class="text-sm font-medium text-muted-foreground"
                data-testid="breadcrumb-page"
              >{{ item.name }}</span>
            </template>
            <template v-else>
              <RouterLink
                :to="item.path"
                class="text-sm font-medium text-foreground hover:text-primary"
              >{{ item.name }}</RouterLink>
              <ChevronRight class="h-4 w-4 text-muted-foreground" />
            </template>
          </li>
        </template>
      </ol>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Menu, ChevronRight } from 'lucide-vue-next'
import { useNavigationStore } from '@/stores/navigation'

// Define route mappings for breadcrumbs
const routeMappings: { [key: string]: string } = {
  '': 'Dashboard',
  'dashboard': 'Dashboard',
  'study-activities': 'Study Activities',
  'words': 'Words',
  'groups': 'Word Groups',
  'sessions': 'Study Sessions',
  'settings': 'Settings',
  'launch': 'Launch'
}

const route = useRoute()
const navigationStore = useNavigationStore()

const breadcrumbItems = computed(() => {
  const pathnames = route.path.split('/').filter(x => x)
  
  // If we're at root, show dashboard
  if (pathnames.length === 0) {
    pathnames.push('')
  }

  return pathnames.map((name, index) => {
    let displayName = routeMappings[name] || name
    const path = '/' + pathnames.slice(0, index + 1).join('/')
    
    // Use group, word, or activity name for the last item if available
    if (index === pathnames.length - 1 || (name !== 'launch' && index === pathnames.length - 2)) {
      if (navigationStore.currentGroup && name === navigationStore.currentGroup.id.toString()) {
        displayName = navigationStore.currentGroup.group_name
      } else if (navigationStore.currentWord && name === navigationStore.currentWord.id.toString()) {
        displayName = navigationStore.currentWord.kanji
      } else if (navigationStore.currentStudyActivity && name === navigationStore.currentStudyActivity.id.toString()) {
        displayName = navigationStore.currentStudyActivity.title
      }
    }

    return {
      name: displayName,
      path
    }
  })
})
</script>
