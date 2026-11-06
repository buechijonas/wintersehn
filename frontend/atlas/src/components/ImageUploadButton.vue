<template>
  <label class="btn btn-sm shadow-none gap-2" :class="{ 'btn-disabled': uploading }">
    <span v-if="uploading" class="loading loading-spinner size-4"></span>
    <AppIcon v-else name="picture" />
    {{ label }}
    <input type="file" accept="image/*" class="hidden" @change="upload" />
  </label>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'ImageUploadButton',
  components: { AppIcon },
  props: {
    label: { type: String, default: 'Bild hochladen' },
  },
  emits: ['uploaded', 'error'],
  data() {
    return {
      uploading: false,
    }
  },
  methods: {
    async upload(event) {
      const [file] = event.target.files
      event.target.value = ''
      if (!file) return
      this.uploading = true
      try {
        this.$emit('uploaded', await useAtlasStore().uploadImage(file))
      } catch (e) {
        this.$emit('error', e.message)
      } finally {
        this.uploading = false
      }
    },
  },
}
</script>
