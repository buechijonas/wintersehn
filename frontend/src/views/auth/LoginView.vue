<template>
  <AuthPage title="Anmelden" breadcrumb-label="Anmelden">
    <form class="fieldset" @submit.prevent="onSubmit">
      <label class="label" for="login-username">Benutzername</label>
      <input
        id="login-username"
        v-model="username"
        type="text"
        autocomplete="username"
        class="input w-full"
        required
      />

      <label class="label mt-2" for="login-password">Passwort</label>
      <input
        id="login-password"
        v-model="password"
        type="password"
        autocomplete="current-password"
        class="input w-full"
        required
      />

      <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

      <BaseButton type="submit" variant="primary" block class="mt-6" :disabled="saving">
        Anmelden
      </BaseButton>
    </form>
    <p class="text-sm mt-4 text-center text-wntrs-muted">
      Noch kein Konto?
      <RouterLink to="/signup" class="link link-primary">Registrieren</RouterLink>
    </p>
  </AuthPage>
</template>

<script>
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useAuthStore } from '@/stores/auth.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'LoginView',
  components: { RouterLink, AuthPage, BaseButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      username: '',
      password: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    async onSubmit() {
      await this.runAction(() => this.authStore.login(this.username, this.password))
      if (!this.error) this.$router.push('/')
    },
  },
}
</script>
