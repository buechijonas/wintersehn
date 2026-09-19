<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Einstellungen</h2>

      <template v-if="authStore.isAuthenticated">
        <div class="flex flex-col items-center gap-4 mb-10 sm:flex-row sm:items-start">
          <div class="flex flex-col items-center shrink-0">
            <h3 class="text-xl my-4">Profilbild</h3>
            <BaseCard class="size-24 shrink-0 flex items-center justify-center p-2">
              <img class="size-14" :src="avatarSrc" alt="" />
            </BaseCard>
          </div>

          <div class="flex-1 flex flex-col min-w-0 w-full sm:w-auto">
            <h3 class="text-xl my-4">Konto</h3>
            <BaseCard class="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div class="flex flex-col gap-1 min-w-0">
                <p class="flex flex-wrap gap-1 min-w-0">
                  <span class="text-wntrs-muted shrink-0">Benutzername:</span>
                  <span class="truncate min-w-0">{{ authStore.user.username }}</span>
                </p>
                <p class="flex flex-wrap gap-1 min-w-0">
                  <span class="text-wntrs-muted shrink-0">E-Mail:</span>
                  <span class="truncate min-w-0">{{ authStore.user.email }}</span>
                </p>
              </div>
              <BaseButton to="/settings/account" class="shrink-0">Bearbeiten</BaseButton>
            </BaseCard>
          </div>
        </div>

        <div class="mb-10">
          <h3 class="text-xl my-4">Passwort</h3>
          <BaseCard class="p-6 flex items-center justify-between gap-4">
            <p class="text-wntrs-muted">Passwort ändern oder zurücksetzen.</p>
            <BaseButton to="/settings/password">Ändern</BaseButton>
          </BaseCard>
        </div>
      </template>

      <div class="mb-10">
        <h3 class="text-xl my-4">Darstellung</h3>
        <BaseCard
          class="p-6 flex flex-col items-center text-center gap-4"
          :class="{ 'sm:flex-row sm:items-center sm:text-left sm:justify-between': !dyslexiaFont }"
        >
          <p class="text-wntrs-muted min-w-0">Erscheinungsbild der Oberfläche.</p>
          <div class="flex flex-wrap justify-center gap-2">
            <BaseButton
              v-for="option in themeOptions"
              :key="option.value"
              type="button"
              size="sm"
              :variant="themeMode === option.value ? 'primary' : 'neutral'"
              @click="themeMode = option.value"
            >
              <AppIcon
                :name="option.icon"
                class="size-4"
                :class="{ invert: themeMode === option.value }"
                alt=""
              />
              {{ option.label }}
            </BaseButton>
          </div>
        </BaseCard>
      </div>

      <div class="mb-10">
        <h3 class="text-xl my-4">Barrierefreiheit</h3>
        <BaseCard
          class="p-6 flex flex-col items-center text-center gap-4"
          :class="{ 'sm:flex-row sm:items-center sm:text-left sm:justify-between': !dyslexiaFont }"
        >
          <p class="text-wntrs-muted min-w-0">Legasthenie</p>
          <div class="flex flex-wrap justify-center gap-2">
            <BaseButton
              v-for="option in dyslexiaOptions"
              :key="option.value"
              type="button"
              size="sm"
              :variant="dyslexiaFont === option.value ? 'primary' : 'neutral'"
              @click="dyslexiaFont = option.value"
            >
              {{ option.label }}
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { themeMode } from '@/lib/theme.js'
import { dyslexiaFont } from '@/lib/dyslexia.js'

export default {
  name: 'SettingsView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, AppIcon },
  data() {
    return {
      icons,
      breadcrumbs: [{ label: 'Einstellungen', to: '/' }],
      themeOptions: [
        { value: 'auto', icon: 'laptop', label: 'Auto' },
        { value: 'light', icon: 'brightness', label: 'Hell' },
        { value: 'dark', icon: 'moon-stars', label: 'Dunkel' },
      ],
      dyslexiaOptions: [
        { value: true, label: 'An' },
        { value: false, label: 'Aus' },
      ],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    avatarSrc() {
      return profiles[this.authStore.user?.avatar] ?? icons.user
    },
    themeMode: {
      get() {
        return themeMode.value
      },
      set(value) {
        themeMode.value = value
      },
    },
    dyslexiaFont: {
      get() {
        return dyslexiaFont.value
      },
      set(value) {
        dyslexiaFont.value = value
      },
    },
  },
}
</script>
