<template>
  <div class="flex flex-1 flex-col pb-8">
    <div class="mx-auto w-full max-w-150 px-6 lg:flex-1">
      <h2 class="text-xl font-light my-4">{{ title }}</h2>
      <div
        class="list bg-base-100 rounded-box shadow-none border-wntrs-border border-solid border-1 p-8"
      >
        <div class="text-wntrs-slate">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LegalPage',
  props: {
    title: { type: String, required: true },
  },
}
</script>
