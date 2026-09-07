<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()

onMounted(() => {
  authStore.fetchMe()
})
</script>

<template>
  <v-app>
    <RouterView />
  </v-app>
</template>
