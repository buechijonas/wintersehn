<script setup>
import { computed, onMounted } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { countries } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

const contentStore = useContentStore()
const breadcrumbs = [{ label: 'Über mich', to: '/' }]

onMounted(() => contentStore.fetchContent('about'))

const aboutRows = computed(() => contentStore.items.about?.data ?? [])
</script>

<template>
  <Page active-navigation="about">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-12 pb-12 px-6 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl my-4">Über mich</h2>
        <Card class="overflow-x-auto">
          <table class="table">
            <tbody>
              <tr v-for="row in aboutRows" :key="row.label">
                <td class="text-wntrs-muted font-medium">{{ row.label }}</td>
                <td>
                  <span class="flex items-center gap-2">
                    <img v-if="row.icon" class="size-5" :src="countries[row.icon]" alt="" />
                    {{ row.value }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </Card>
      </div>
    </div>
  </Page>
</template>
