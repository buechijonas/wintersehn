<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="cpnt-breadcrumbs py-2 px-6">
    <div class="breadcrumbs text-sm">
      <ul>
        <li class="item" v-for="(item, index) in items" :key="index">
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
<style>
.cpnt-breadcrumbs {
  border-bottom-width: 1px;
  border-bottom-style: solid;
  border-bottom-color: #e3e5e8;
}

.cpnt-breadcrumbs .item {
  color: #a8b3bf;
}
</style>
