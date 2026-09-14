<template>
  <v-app>
    <RouterView />
  </v-app>
</template>

<script>
import { RouterView } from 'vue-router'

export default {
  name: 'App',
  components: { RouterView },
}
</script>
