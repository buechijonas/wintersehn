<template>
  <div>
    <input ref="input" type="file" accept="image/*" class="hidden" @change="pick" />
    <BaseButton
      type="button"
      variant="neutral"
      size="sm"
      class="w-full"
      :disabled="disabled"
      @click="$refs.input.click()"
    >
      <AppIcon name="picture" />
      {{ label }}
    </BaseButton>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'

export default {
  name: 'ImagePickButton',
  components: { AppIcon, BaseButton },
  props: {
    label: { type: String, default: 'Bild' },
    disabled: { type: Boolean, default: false },
  },
  emits: ['pick'],
  methods: {
    pick(event) {
      const [file] = event.target.files
      event.target.value = ''
      if (file) this.$emit('pick', file)
    },
  },
}
</script>
