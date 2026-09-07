<script setup>
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Footer from '@/components/common/Footer.vue'

const breadcrumbs = [
  {
    label: 'Home',
    to: '/',
  },
]
</script>

<template>
  <Page active-navigation="dashboard">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex" style="height: calc(100vh - 192px)">
      <div class="flex flex-col mx-auto my-32">
        <h1 class="title my-8 font-light">Herzlich Willkommen</h1>
        <p class="subtitle mx-auto color-gray font-light">wintersehn.ch</p>
      </div>
    </div>
    <Footer />
  </Page>
</template>
