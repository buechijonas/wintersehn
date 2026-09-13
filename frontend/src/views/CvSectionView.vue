<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { flats } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

const route = useRoute()
const contentStore = useContentStore()

onMounted(() => contentStore.fetchContent('cv'))

const cvCategories = computed(() => contentStore.items.cv?.data ?? [])
const section = computed(() =>
  cvCategories.value.flatMap((category) => category.items).find((item) => item.key === route.params.key),
)

const breadcrumbs = computed(() => [
  { label: 'Lebenslauf', to: '/cv' },
  { label: section.value?.label ?? '' },
])
</script>

<template>
  <Page active-navigation="cv">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">{{ section?.label }}</h2>

        <p v-if="!section?.timeline?.length" class="text-wntrs-muted font-light">
          Inhalt folgt in Kürze.
        </p>

        <ul v-else class="timeline timeline-snap-icon max-md:timeline-compact timeline-vertical">
          <li
            v-for="(entry, index) in section.timeline"
            :key="`${entry.year}-${entry.title}`"
          >
            <hr :class="{ invisible: index === 0 }" />
            <div class="timeline-middle font-mono italic text-wntrs-muted">{{ entry.year }}</div>
            <div
              :class="
                entry.side === 'start'
                  ? 'timeline-start mb-10 flex justify-end'
                  : 'timeline-end mb-10 flex justify-start'
              "
            >
              <div class="flex flex-col items-center gap-1">
                <Card
                  class="size-40 flex flex-col items-center justify-center text-center gap-4 p-2"
                >
                  <img
                    class="size-16"
                    :alt="entry.title"
                    :src="flats[entry.icon ?? section.icon]"
                  />
                  <div>
                    <div class="text-wntrs-slate text-xs font-bold">{{ entry.title }}</div>
                    <p class="text-wntrs-slate font-light text-xs">{{ entry.description }}</p>
                  </div>
                </Card>
                <a
                  v-for="link in entry.links ?? []"
                  :key="link.url"
                  :href="link.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn btn-primary btn-sm w-40 shadow-none"
                >
                  {{ link.label }}
                </a>
              </div>
            </div>
            <hr :class="{ invisible: index === section.timeline.length - 1 }" />
          </li>
        </ul>
      </div>
    </div>
  </Page>
</template>
