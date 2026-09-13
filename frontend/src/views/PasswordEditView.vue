<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

const breadcrumbs = [
  { label: 'Einstellungen', to: '/settings' },
  { label: 'Passwort ändern' },
]

const currentPassword = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const error = ref('')
const saving = ref(false)

async function save() {
  error.value = ''

  if (newPassword.value !== newPasswordConfirm.value) {
    error.value = 'Die Passwörter stimmen nicht überein.'
    return
  }

  saving.value = true
  try {
    await authStore.changePassword(currentPassword.value, newPassword.value)
    router.push('/settings')
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <Page>
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Passwort ändern</h2>

        <Card class="p-6">
          <form class="fieldset" @submit.prevent="save">
            <label class="label" for="password-current">Aktuelles Passwort</label>
            <input
              id="password-current"
              v-model="currentPassword"
              type="password"
              autocomplete="current-password"
              class="input w-full"
              required
            />

            <label class="label mt-2" for="password-new">Neues Passwort</label>
            <input
              id="password-new"
              v-model="newPassword"
              type="password"
              autocomplete="new-password"
              class="input w-full"
              required
            />

            <label class="label mt-2" for="password-new-confirm">Neues Passwort bestätigen</label>
            <input
              id="password-new-confirm"
              v-model="newPasswordConfirm"
              type="password"
              autocomplete="new-password"
              class="input w-full"
              required
            />

            <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

            <div class="flex gap-4 mt-4">
              <RouterLink to="/settings" class="btn shadow-none">Abbrechen</RouterLink>
              <button type="submit" class="btn btn-primary shadow-none" :disabled="saving">
                Passwort ändern
              </button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  </Page>
</template>
