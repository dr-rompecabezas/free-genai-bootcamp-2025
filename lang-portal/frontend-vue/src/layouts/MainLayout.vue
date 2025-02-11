<template>
  <div class="min-h-screen">
    <main class="pl-72">
      <Breadcrumbs />
      <div class="container mx-auto px-4 py-8">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import Breadcrumbs from '@/components/Breadcrumbs.vue'
// Layout component that provides spacing for the sidebar
</script>
