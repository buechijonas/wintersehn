<template>
  <article class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">{{ title }}</h1>
    <div class="flex max-w-150 flex-col gap-10">
      <slot />
    </div>
  </article>
</template>

<script>
export default {
  name: 'LegalPage',
  props: {
    title: { type: String, required: true },
  },
}
</script>
