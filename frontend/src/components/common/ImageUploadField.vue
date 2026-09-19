<template>
  <div>
    <input ref="input" type="file" accept="image/*" multiple class="hidden" @change="onChange" />
    <BaseButton type="button" :disabled="uploading" @click="$refs.input.click()">
      {{ uploading ? 'Lädt hoch…' : label }}
    </BaseButton>
    <p v-if="error" class="text-error text-sm mt-2">{{ error }}</p>
  </div>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'ImageUploadField',
  components: { BaseButton },
  props: {
    label: { type: String, default: 'Bilder hochladen' },
  },
  emits: ['uploaded'],
  data() {
    return {
      uploading: false,
      error: '',
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
  },
  methods: {
    async onChange(event) {
      const files = [...event.target.files]
      event.target.value = ''
      if (!files.length) return

      this.error = ''
      this.uploading = true
      try {
        // Uploaded as one batch (not per-file) so the parent does a single
        // save - emitting per file would let concurrent saves race and
        // silently drop each other's images.
        const urls = await Promise.all(files.map((file) => this.contentStore.uploadImage(file)))
        this.$emit('uploaded', urls)
      } catch (e) {
        this.error = e.message
      } finally {
        this.uploading = false
      }
    },
  },
}
</script>
