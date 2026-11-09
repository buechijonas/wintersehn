<template>
  <section class="flex flex-col gap-3">
    <h2 v-if="title" class="text-xl">{{ title }}</h2>
    <p v-if="subtitle" class="text-wntrs-slate">{{ subtitle }}</p>
    <p v-if="text" class="text-wntrs-muted">{{ text }}</p>
    <ul v-if="items.length" class="flex flex-col gap-3 ps-6">
      <li v-for="item in items" :key="item.listtitle">
        <span class="font-medium">{{ item.listtitle }}</span>
        <ul v-if="item.texttitle" class="ps-6">
          <li class="text-wntrs-muted">{{ item.texttitle }}</li>
        </ul>
      </li>
    </ul>
    <slot />
  </section>
</template>

<script>
export default {
  name: 'LegalSection',
  props: {
    title: { type: String, default: '' },
    subtitle: { type: String, default: '' },
    text: { type: String, default: '' },
    items: { type: Array, default: () => [] },
  },
}
</script>

<style scoped>
ul {
  list-style-type: disc;
}

ul ul {
  list-style-type: circle;
}
</style>
