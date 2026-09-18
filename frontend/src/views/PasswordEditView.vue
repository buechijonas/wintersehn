<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Passwort ändern</h2>

      <BaseCard class="p-6">
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
            <CancelButton to="/settings" />
            <BaseButton type="submit" variant="primary" :disabled="saving">
              Passwort ändern
            </BaseButton>
          </div>
        </form>
      </BaseCard>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import CancelButton from '@/components/common/CancelButton.vue'
import { useAuthStore } from '@/stores/auth.js'

export default {
  name: 'PasswordEditView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, CancelButton },
  data() {
    return {
      breadcrumbs: [
        { label: 'Einstellungen', to: '/settings' },
        { label: 'Passwort ändern' },
      ],
      currentPassword: '',
      newPassword: '',
      newPasswordConfirm: '',
      error: '',
      saving: false,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
  },
  methods: {
    async save() {
      this.error = ''

      if (this.newPassword !== this.newPasswordConfirm) {
        this.error = 'Die Passwörter stimmen nicht überein.'
        return
      }

      this.saving = true
      try {
        await this.authStore.changePassword(this.currentPassword, this.newPassword)
        this.$router.push('/settings')
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
