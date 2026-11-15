<template>
  <AuthPage title="Kein Zugriff" breadcrumb-label="Kein Zugriff">
    <p class="font-light">
      Dieser Bereich ist nur für freigeschaltete Konten sichtbar. Kontaktiere
      <a href="mailto:contact@wintersehn.ch" class="link link-primary">contact@wintersehn.ch</a>, um
      ihn freischalten zu lassen und mehr über wintersehn zu erfahren.
    </p>
    <BaseButton variant="primary" block class="mt-6" to="/">Zur Startseite</BaseButton>
  </AuthPage>
</template>

<script>
import AuthPage from '@core/components/layout/AuthPage.vue'
import BaseButton from '@core/components/common/BaseButton.vue'

export default {
  name: 'LockedView',
  components: { AuthPage, BaseButton },
}
</script>
