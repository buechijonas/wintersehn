<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const done = ref(false)

onMounted(async () => {
  try {
    await authStore.logout()
  } catch {
    // nothing more useful to do on this page
  }
  done.value = true
})
</script>

<template>
  <AuthPage title="Abmelden" breadcrumb-label="Abmelden">
    <p class="font-light">
      {{ done ? 'Sie wurden erfolgreich abgemeldet.' : 'Sie werden abgemeldet …' }}
    </p>
    <RouterLink to="/" class="btn btn-primary w-full mt-6 shadow-none">
      Zurück zur Startseite
    </RouterLink>
  </AuthPage>
</template>
