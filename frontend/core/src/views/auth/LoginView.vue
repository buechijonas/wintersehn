<template>
  <AuthPage title="Anmelden" breadcrumb-label="Anmelden">
    <p class="font-light mb-6">
      wintersehn nutzt govex für die Anmeldung. Benutzername und Passwort verwaltest du dort.
    </p>
    <p v-if="locked" class="mb-6 rounded-box bg-base-200 p-4 text-sm">
      Dieser Bereich ist gesperrt. Melde dich an und kontaktiere
      <a href="mailto:contact@wintersehn.ch" class="link link-primary">contact@wintersehn.ch</a>, um
      ihn freischalten zu lassen und mehr über wintersehn zu erfahren.
    </p>
    <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>
    <BaseButton variant="primary" block @click="authStore.startGovexLogin()">
      Mit govex anmelden
    </BaseButton>
  </AuthPage>
</template>

<script>
import AuthPage from '@core/components/layout/AuthPage.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import { useAuthStore } from '@core/stores/auth.js'

const ERROR_MESSAGES = {
  oidc_failed: 'Die Anmeldung über govex ist fehlgeschlagen. Bitte versuche es erneut.',
}

export default {
  name: 'LoginView',
  components: { AuthPage, BaseButton },
  data() {
    return {
      error: ERROR_MESSAGES[this.$route.query.error] ?? '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    locked() {
      return this.$route.query.reason === 'locked'
    },
  },
}
</script>
