<template>
  <p v-for="line in lines" :key="line" class="font-light">{{ line }}</p>
</template>

<script>
export default {
  name: 'LegalAddress',
  data() {
    return {
      lines: ['Jonas S. Büchi', 'Eichmatt 1', 'CH-3324 Hindelbank', 'Kanton Bern'],
    }
  },
}
</script>
