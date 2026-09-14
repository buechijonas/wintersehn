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

<script>
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'LogoutView',
  components: { RouterLink, AuthPage },
  data() {
    return { done: false }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  async mounted() {
    try {
      await this.authStore.logout()
    } catch {
      // nothing more useful to do on this page
    }
    this.done = true
  },
}
</script>
