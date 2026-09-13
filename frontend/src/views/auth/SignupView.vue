<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''

  if (password.value !== passwordConfirm.value) {
    error.value = 'Die Passwörter stimmen nicht überein.'
    return
  }

  loading.value = true
  try {
    await authStore.signup({
      username: username.value,
      email: email.value,
      password: password.value,
    })
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

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

      <button type="submit" class="btn btn-primary w-full mt-6 shadow-none" :disabled="loading">
        Registrieren
      </button>
    </form>
    <p class="text-sm mt-4 text-center text-wntrs-muted">
      Bereits ein Konto?
      <RouterLink to="/login" class="link link-primary">Anmelden</RouterLink>
    </p>
  </AuthPage>
</template>
