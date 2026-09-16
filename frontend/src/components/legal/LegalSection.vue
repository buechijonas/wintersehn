<template>
  <section class="my-6">
    <h3 v-if="title" class="font-medium">{{ title }}</h3>
    <p v-if="subtitle" class="font-light text-wntrs-slate">{{ subtitle }}</p>
    <p v-if="text" class="font-light">{{ text }}</p>
    <ul v-if="items.length" class="ps-6 mt-4">
      <li v-for="item in items" :key="item.listtitle" class="mb-3">
        <span class="font-medium">{{ item.listtitle }}</span>
        <ul v-if="item.texttitle" class="ps-6">
          <li class="font-light">{{ item.texttitle }}</li>
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
