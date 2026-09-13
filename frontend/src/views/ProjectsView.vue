<script setup>
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Footer from '@/components/common/Footer.vue'

const breadcrumbs = [{ label: 'Projekte', to: '/' }]
</script>

<template>
  <Page active-navigation="projects">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex h-[calc(100dvh-192px)]">
      <div class="flex flex-col mx-auto my-32">
        <h1 class="text-title my-8 font-light">Projekte</h1>
        <p class="subtitle mx-auto text-wntrs-muted font-light">Inhalt folgt in Kürze.</p>
      </div>
    </div>
    <Footer />
  </Page>
</template>
