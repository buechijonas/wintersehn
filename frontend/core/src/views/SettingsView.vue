<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Einstellungen</h2>

      <div class="mb-10">
        <h3 class="text-xl my-4">Konto</h3>
        <AccountCard />
      </div>

      <AppearanceSettings />
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import AccountCard from '@core/components/common/AccountCard.vue'
import AppearanceSettings from '@core/components/common/AppearanceSettings.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@core/components/common/BaseFooter.vue'

export default {
  name: 'SettingsView',
  components: { AccountCard, AppearanceSettings, BaseBreadcrumbs, BaseFooter },
  data() {
    return {
      breadcrumbs: [{ label: 'Einstellungen', to: '/' }],
    }
  },
}
</script>
