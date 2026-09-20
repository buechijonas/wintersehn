<template>
  <AuthPage title="Registrieren" breadcrumb-label="Registrieren">
    <form ref="form" class="fieldset" @submit.prevent="onSubmit">
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

      <altcha-widget
        class="mt-4"
        challenge="/api/auth/altcha-challenge/"
        auto="onload"
        name="altcha"
      ></altcha-widget>

      <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

      <BaseButton type="submit" variant="primary" block class="mt-6" :disabled="saving">
        Registrieren
      </BaseButton>
    </form>
    <p class="text-sm mt-4 text-center text-wntrs-muted">
      Bereits ein Konto?
      <RouterLink to="/login" class="link link-primary">Anmelden</RouterLink>
    </p>
  </AuthPage>
</template>

<style scoped>
altcha-widget {
  display: block;
  --altcha-max-width: 100%;
  --altcha-color-base: var(--color-base-100);
  --altcha-border-color: color-mix(in oklab, var(--color-base-content) 20%, transparent);
  --altcha-border-width: var(--border, 1px);
  --altcha-border-radius: var(--radius-field, 0.25rem);
}
</style>

<script>
import 'altcha'
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useAuthStore } from '@/stores/auth.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'SignupView',
  components: { RouterLink, AuthPage, BaseButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      username: '',
      email: '',
      password: '',
      passwordConfirm: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    async onSubmit() {
      if (this.password !== this.passwordConfirm) {
        this.error = 'Die Passwörter stimmen nicht überein.'
        return
      }

      const altcha = new FormData(this.$refs.form).get('altcha')
      if (!altcha) {
        this.error = 'Bitte warte, bis die Bot-Verifizierung abgeschlossen ist.'
        return
      }

      await this.runAction(() =>
        this.authStore.signup({
          username: this.username,
          email: this.email,
          password: this.password,
          altcha,
        }),
      )
      if (!this.error) this.$router.push('/')
    },
  },
}
</script>
