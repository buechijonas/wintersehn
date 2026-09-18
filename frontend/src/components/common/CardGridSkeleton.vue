<template>
  <div class="flex flex-col gap-4">
    <div v-for="row in rows" :key="row" class="mx-auto w-full max-w-200">
      <div class="skeleton mt-4 mb-4 h-6 w-32"></div>
      <div class="flex flex-wrap justify-center gap-2 lg:justify-start">
        <div v-for="col in cols" :key="col" class="skeleton size-40 shrink-0 rounded-box"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardGridSkeleton',
  props: {
    rows: { type: Number, default: 2 },
    cols: { type: Number, default: 4 },
  },
}
</script>
