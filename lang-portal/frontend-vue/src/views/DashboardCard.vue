<template>
  <div :class="['bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6', className]">
    <div class="flex items-center gap-2 mb-4">
      <component :is="icon" class="w-5 h-5 text-blue-500" />
      <h2 class="text-lg font-semibold">{{ title }}</h2>
    </div>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import type { Component } from 'vue'

interface Props {
  title: string
  icon: Component
  className?: string
}

defineProps<Props>()</script>
