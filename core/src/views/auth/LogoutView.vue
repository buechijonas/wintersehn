<template>
  <AuthPage title="Abmelden" breadcrumb-label="Abmelden">
    <p class="font-light">
      {{ done ? 'Sie wurden erfolgreich abgemeldet.' : 'Sie werden abgemeldet …' }}
    </p>
    <BaseButton variant="primary" block class="mt-6" to="/">Zurück zur Startseite</BaseButton>
  </AuthPage>
</template>

<script>
import AuthPage from '@core/components/layout/AuthPage.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import { useAuthStore } from '@core/stores/auth.js'

export default {
  name: 'LogoutView',
  components: { AuthPage, BaseButton },
  data() {
    return { done: false }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  async mounted() {
    await this.authStore.logout().catch(() => {})
    this.done = true
  },
}
</script>
