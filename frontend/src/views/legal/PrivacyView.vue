<script setup>
import LegalContent from '@/components/legal/LegalContent.vue'
import { legalPages } from '@/data/legal.js'
</script>

<template>
  <LegalContent :page="legalPages.privacy" />
</template>
