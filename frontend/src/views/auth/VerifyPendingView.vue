<template>
  <AuthPage title="Verifizierung ausstehend" breadcrumb-label="Verifizierung">
    <p class="font-light">
      Lass dein Konto verifizieren, indem du uns kontaktierst:
      <a href="mailto:contact@wintersehn.ch" class="link link-primary">contact@wintersehn.ch</a>
      und wartet nun auf die Bestätigung durch den Inhaber. Sie erhalten Zugriff, sobald die
      Verifizierung abgeschlossen ist.
    </p>
    <BaseButton variant="primary" block class="mt-6" to="/logout">Abmelden</BaseButton>
  </AuthPage>
</template>

<script>
import AuthPage from '@/components/layout/AuthPage.vue'
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'VerifyPendingView',
  components: { AuthPage, BaseButton },
}
</script>
