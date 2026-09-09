<script setup>
import { computed, onMounted } from 'vue'
import LegalContent from '@/components/legal/LegalContent.vue'
import { useContentStore } from '@/stores/content.js'

const props = defineProps({
  contentKey: { type: String, required: true },
})

const contentStore = useContentStore()

onMounted(() => contentStore.fetchContent(props.contentKey))

const page = computed(() => contentStore.items[props.contentKey]?.data)
</script>

<template>
  <LegalContent v-if="page" :page="page" />
</template>
