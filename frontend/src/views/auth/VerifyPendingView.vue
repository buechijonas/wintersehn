<script setup>
import { RouterLink } from 'vue-router'
import AuthPage from '@/components/layout/AuthPage.vue'
</script>

<template>
  <AuthPage title="Verifizierung ausstehend" breadcrumb-label="Verifizierung">
    <p class="font-light">
      Lass dein Konto verifizieren, indem du uns kontaktierst:
      <a href="mailto:contact@wintersehn.ch" class="link link-primary">contact@wintersehn.ch</a>
      und wartet nun auf die Bestätigung durch den Inhaber. Sie erhalten Zugriff, sobald die
      Verifizierung abgeschlossen ist.
    </p>
    <RouterLink to="/logout" class="btn btn-primary w-full mt-6 shadow-none">Abmelden</RouterLink>
  </AuthPage>
</template>
