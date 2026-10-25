<template>
  <BaseButton
    v-bind="$attrs"
    variant="neutral"
    :size="square ? undefined : 'sm'"
    :shape="square ? 'square' : undefined"
    :title="label"
    :disabled="disabled"
    @click="open"
  >
    <AppIcon name="picture" :alt="label" />
    <template v-if="!square">{{ label }}</template>
  </BaseButton>

  <BaseDialog
    ref="dialog"
    title="Bild wählen"
    box-class="w-full h-full max-w-full max-h-full rounded-none sm:rounded-box sm:h-[640px] sm:max-h-[85vh] sm:w-11/12 sm:max-w-3xl"
  >
    <ImageLibrary
      v-if="openings"
      :key="openings"
      selectable
      :selected="selected"
      @select="pick"
      @removed="removed"
    />
  </BaseDialog>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import ImageLibrary from '@/components/ImageLibrary.vue'

export default {
  name: 'ImagePickButton',
  components: { AppIcon, BaseButton, BaseDialog, ImageLibrary },
  props: {
    label: { type: String, default: 'Bild wählen' },
    selected: { type: String, default: null },
    square: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
  },
  inheritAttrs: false,
  emits: ['pick'],
  data() {
    return {
      openings: 0,
    }
  },
  methods: {
    open() {
      this.openings += 1
      this.$refs.dialog.open()
    },
    pick(image) {
      this.$refs.dialog.close()
      this.$emit('pick', image.uuid)
    },
    removed(image) {
      if (image === this.selected) this.$emit('pick', null)
    },
  },
}
</script>
