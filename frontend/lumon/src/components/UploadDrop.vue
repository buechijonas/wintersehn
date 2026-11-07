<template>
  <label
    class="flex cursor-pointer flex-col gap-2 rounded-box border border-dashed text-sm transition-colors"
    :class="[
      dragging ? 'border-primary bg-primary/5' : 'border-wntrs-border hover:bg-base-200',
      compact ? 'px-3 py-2' : 'items-center p-6 text-center',
      { 'pointer-events-none': saving },
    ]"
    @dragover.prevent="dragging = true"
    @dragleave="dragging = false"
    @drop.prevent="drop"
  >
    <input type="file" :accept="accept" class="hidden" @change="pick" />
    <span class="flex items-center gap-2" :class="{ 'justify-center': !compact }">
      <AppIcon name="upload" />
      {{ saving ? `Wird hochgeladen · ${Math.round(progress * 100)} %` : label }}
    </span>
    <progress
      v-if="saving"
      class="progress progress-primary h-1 w-full"
      :value="progress"
      max="1"
    ></progress>
    <span v-else-if="!compact" class="text-xs text-wntrs-muted">MP4, M4V, WebM, MKV oder MOV</span>
    <span v-if="error" class="text-xs text-error">{{ error }}</span>
  </label>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useLumonStore } from '@/stores/lumon.js'

export default {
  name: 'UploadDrop',
  components: { AppIcon },
  mixins: [asyncActionMixin],
  props: {
    target: { type: Object, required: true },
    label: { type: String, default: 'Video hierher ziehen oder auswählen' },
    compact: { type: Boolean, default: false },
  },
  emits: ['uploaded'],
  data() {
    return {
      accept: '.mp4,.m4v,.webm,.mkv,.mov,video/*',
      dragging: false,
      progress: 0,
    }
  },
  methods: {
    drop(event) {
      this.dragging = false
      this.send(event.dataTransfer.files[0])
    },
    pick(event) {
      this.send(event.target.files[0])
      event.target.value = ''
    },
    send(file) {
      if (!file) return
      this.progress = 0
      this.runAction(async () => {
        await useLumonStore().upload(this.target, file, (progress) => {
          this.progress = progress
        })
        this.$emit('uploaded')
      })
    },
  },
}
</script>
