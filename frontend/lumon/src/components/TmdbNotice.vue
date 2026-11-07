<template>
  <p class="text-xs text-wntrs-muted">
    Daten und Bilder von TMDB. LUMON nutzt die TMDB-API, ist aber nicht von TMDB unterstützt oder
    zertifiziert.<template v-if="providers"> Anbieterdaten von JustWatch.</template>
  </p>
</template>

<script>
export default {
  name: 'TmdbNotice',
  props: {
    providers: { type: Boolean, default: false },
  },
}
</script>
