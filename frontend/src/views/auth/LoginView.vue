<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

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

      <button type="submit" class="btn btn-primary w-full mt-6 shadow-none" :disabled="loading">
        Anmelden
      </button>
    </form>
    <p class="text-sm mt-4 text-center color-gray">
      Noch kein Konto?
      <RouterLink to="/signup" class="link link-primary">Registrieren</RouterLink>
    </p>
  </AuthPage>
</template>
