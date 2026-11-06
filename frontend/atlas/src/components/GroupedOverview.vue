<template>
  <p v-if="!groups.length" class="text-wntrs-muted">{{ empty }}</p>
  <section v-for="institution in groups" :key="institution.uuid" class="flex flex-col gap-4">
    <h2 class="text-xl font-light">{{ institution.name }}</h2>
    <div v-for="subject in institution.subjects" :key="subject.uuid" class="flex flex-col gap-2">
      <RouterLink
        :to="`/subjects/${subject.uuid}`"
        class="text-sm text-wntrs-muted hover:text-base-content"
      >
        {{ subject.name }}
      </RouterLink>
      <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <li v-for="item in subject.items" :key="item.uuid">
          <ItemCard
            :title="item.title"
            :to="`${base}/${item.uuid}`"
            :icon="icon"
            :meta="meta(item)"
          />
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
import { RouterLink } from 'vue-router'
import ItemCard from '@/components/ItemCard.vue'

export default {
  name: 'GroupedOverview',
  components: { ItemCard, RouterLink },
  props: {
    groups: { type: Array, required: true },
    base: { type: String, required: true },
    icon: { type: String, required: true },
    empty: { type: String, required: true },
    meta: { type: Function, default: () => '' },
  },
}
</script>
