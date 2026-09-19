<template>
  <dialog ref="dialog" class="modal" @keydown="onKeydown">
    <div
      class="modal-box relative flex items-center justify-center p-0 w-full h-full max-w-full max-h-full bg-black/90 rounded-none"
      @touchstart="onTouchStart"
      @touchend="onTouchEnd"
    >
      <form method="dialog" class="absolute right-2 top-2 z-10">
        <BaseButton type="submit" variant="ghost" shape="circle" size="sm" class="text-white text-xl">
          ✕
        </BaseButton>
      </form>

      <BaseButton
        v-if="images.length > 1"
        type="button"
        variant="ghost"
        shape="circle"
        class="absolute left-2 top-1/2 -translate-y-1/2 z-10 text-white text-2xl"
        @click="prev"
      >
        ‹
      </BaseButton>

      <img v-if="currentImage" :src="currentImage" alt="" class="max-w-full max-h-full object-contain" />

      <BaseButton
        v-if="images.length > 1"
        type="button"
        variant="ghost"
        shape="circle"
        class="absolute right-2 top-1/2 -translate-y-1/2 z-10 text-white text-2xl"
        @click="next"
      >
        ›
      </BaseButton>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'

export default {
  name: 'ImageLightbox',
  components: { BaseButton },
  props: {
    images: { type: Array, required: true },
  },
  data() {
    return {
      index: 0,
      touchStartX: 0,
    }
  },
  computed: {
    currentImage() {
      return this.images[this.index] ?? ''
    },
  },
  methods: {
    open(startIndex = 0) {
      this.index = startIndex
      this.$refs.dialog?.showModal()
    },
    close() {
      this.$refs.dialog?.close()
    },
    prev() {
      this.index = (this.index - 1 + this.images.length) % this.images.length
    },
    next() {
      this.index = (this.index + 1) % this.images.length
    },
    onKeydown(event) {
      if (event.key === 'ArrowLeft') this.prev()
      else if (event.key === 'ArrowRight') this.next()
    },
    onTouchStart(event) {
      this.touchStartX = event.changedTouches[0].clientX
    },
    onTouchEnd(event) {
      const dx = event.changedTouches[0].clientX - this.touchStartX
      if (Math.abs(dx) < 40) return
      if (dx > 0) this.prev()
      else this.next()
    },
  },
}
</script>
