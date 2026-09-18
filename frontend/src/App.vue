<template>
  <v-app>
    <BasePage :active-navigation="$route.meta.activeNavigation">
      <RouterView />
    </BasePage>
  </v-app>
</template>

<script>
import { RouterView } from 'vue-router'
import BasePage from '@/components/layout/BasePage.vue'

export default {
  name: 'App',
  components: { RouterView, BasePage },
}
</script>
