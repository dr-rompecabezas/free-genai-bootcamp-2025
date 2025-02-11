<template>
  <aside class="fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r bg-background">
    <!-- Header -->
    <header class="border-b px-6 py-3">
      <h1 class="text-xl font-semibold">LangPortal</h1>
    </header>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto p-4">
      <ul class="space-y-1">
        <li v-for="item in navItems" :key="item.name">
          <RouterLink
            :to="item.path"
            :data-testid="'nav-item-' + item.name.toLowerCase().replace(' ', '-')"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
            :class="{
              'bg-primary/10 text-primary': isActive(item.path),
              'hover:bg-muted': !isActive(item.path)
            }"
          >
            <component :is="item.icon" class="h-4 w-4" />
            <span>{{ item.name }}</span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- Rail -->
    <div class="border-t" />
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { Home, BookOpen, WholeWord, Group, Clock, Settings } from 'lucide-vue-next'

const route = useRoute()

const navItems = [
  { icon: Home, name: 'Dashboard', path: '/dashboard' },
  { icon: BookOpen, name: 'Study Activities', path: '/study-activities' },
  { icon: WholeWord, name: 'Words', path: '/words' },
  { icon: Group, name: 'Word Groups', path: '/groups' },
  { icon: Clock, name: 'Sessions', path: '/sessions' },
  { icon: Settings, name: 'Settings', path: '/settings' },
]

const isActive = (path: string) => {
  // Handle root path
  if (path === '/dashboard' && route.path === '/') return true
  // Handle nested routes
  return route.path.startsWith(path)
}
</script>
