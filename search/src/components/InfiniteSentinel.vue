<template>
  <div ref="sentinel" class="h-px"></div>
</template>

<script>
export default {
  name: 'InfiniteSentinel',
  emits: ['visible'],
  mounted() {
    this.observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) this.$emit('visible')
    })
    this.observer.observe(this.$refs.sentinel)
  },
  beforeUnmount() {
    this.observer.disconnect()
  },
}
</script>
