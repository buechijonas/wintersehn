<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="border-b border-wntrs-border py-2 px-6">
    <div class="breadcrumbs text-sm">
      <ul>
        <li class="text-wntrs-muted" v-for="(item, index) in items" :key="index">
          <RouterLink v-if="item.to" :to="item.to">
            {{ item.label }}
          </RouterLink>

          <span v-else>
            {{ item.label }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>
