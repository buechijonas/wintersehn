<template>
  <AuthPage title="Registrieren" breadcrumb-label="Registrieren">
    <form class="fieldset" @submit.prevent="onSubmit">
      <label class="label" for="signup-username">Benutzername</label>
      <input
        id="signup-username"
        v-model="username"
        type="text"
        autocomplete="username"
        class="input w-full"
        required
      />

      <label class="label mt-2" for="signup-email">E-Mail</label>
      <input
        id="signup-email"
        v-model="email"
        type="email"
        autocomplete="email"
        class="input w-full"
        required
      />

      <label class="label mt-2" for="signup-password">Passwort</label>
      <input
        id="signup-password"
        v-model="password"
        type="password"
        autocomplete="new-password"
        class="input w-full"
        required
      />

      <label class="label mt-2" for="signup-password-confirm">Passwort bestätigen</label>
      <input
        id="signup-password-confirm"
        v-model="passwordConfirm"
        type="password"
        autocomplete="new-password"
        class="input w-full"
        required
      />

      <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

      <BaseButton type="submit" variant="primary" block class="mt-6" :disabled="loading">
        Registrieren
      </BaseButton>
    </form>
    <p class="text-sm mt-4 text-center text-wntrs-muted">
      Bereits ein Konto?
      <RouterLink to="/login" class="link link-primary">Anmelden</RouterLink>
    </p>
  </AuthPage>
</template>

<script>
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'SignupView',
  components: { RouterLink, AuthPage, BaseButton },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      passwordConfirm: '',
      error: '',
      loading: false,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    async onSubmit() {
      this.error = ''

      if (this.password !== this.passwordConfirm) {
        this.error = 'Die Passwörter stimmen nicht überein.'
        return
      }

      this.loading = true
      try {
        await this.authStore.signup({
          username: this.username,
          email: this.email,
          password: this.password,
        })
        this.$router.push('/')
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
