<template>
  <div>
    <label v-if="label" class="label">{{ label }}</label>
    <div class="flex items-center gap-4">
      <BaseCard class="size-16 shrink-0 flex items-center justify-center p-2">
        <img
          v-if="previewIcon"
          class="size-11"
          :class="{ 'opacity-40': !modelValue }"
          :src="icons[previewIcon]"
          alt=""
        />
      </BaseCard>

      <BaseButton
        type="button"
        class="flex-1 min-w-0 justify-start gap-2"
        @click="openDialog"
      >
        <img v-if="modelValue" class="size-5 shrink-0" :src="icons[modelValue]" alt="" />
        <span class="truncate">{{ currentLabel }}</span>
      </BaseButton>
    </div>

    <BaseDialog ref="dialog" title="Icon wählen">
      <input
        v-model="search"
        type="text"
        placeholder="Icon suchen…"
        class="input w-full mb-4"
        autofocus
      />
      <div class="grid grid-cols-4 gap-2 max-h-80 overflow-y-auto">
        <button
          v-if="allowEmpty"
          type="button"
          class="flex flex-col items-center gap-1 p-2 rounded hover:bg-base-200"
          :class="{ 'bg-base-200': !modelValue }"
          @click="choose('')"
        >
          <img class="size-8" :src="icons[emptyIcon]" alt="" />
          <span class="text-xs text-center">{{ emptyLabel }}</span>
        </button>
        <button
          v-for="key in filteredKeys"
          :key="key"
          type="button"
          class="flex flex-col items-center gap-1 p-2 rounded hover:bg-base-200"
          :class="{ 'bg-base-200': modelValue === key }"
          @click="choose(key)"
        >
          <img class="size-8" :src="icons[key]" alt="" />
          <span class="text-xs text-center">{{ iconLabel(key) }}</span>
        </button>
        <p
          v-if="!filteredKeys.length"
          class="col-span-full text-wntrs-muted text-sm text-center py-4"
        >
          Keine Icons gefunden.
        </p>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'

export default {
  name: 'IconPickerField',
  components: { BaseCard, BaseButton, BaseDialog },
  props: {
    modelValue: { type: String, default: '' },
    icons: { type: Object, required: true },
    label: { type: String, default: 'Icon' },
    allowEmpty: { type: Boolean, default: false },
    emptyIcon: { type: String, default: '' },
    emptyLabel: { type: String, default: 'Kein Icon' },
  },
  emits: ['update:modelValue'],
  data() {
    return { search: '' }
  },
  computed: {
    iconKeys() {
      return Object.keys(this.icons).sort((a, b) => a.localeCompare(b, 'de'))
    },
    filteredKeys() {
      const query = this.search.trim().toLowerCase()
      if (!query) return this.iconKeys
      return this.iconKeys.filter(
        (key) =>
          key.replace(/[-_]/g, ' ').includes(query) ||
          this.iconLabel(key).toLowerCase().includes(query),
      )
    },
    previewIcon() {
      return this.modelValue || this.emptyIcon
    },
    currentLabel() {
      if (this.modelValue) return this.iconLabel(this.modelValue)
      return this.allowEmpty ? this.emptyLabel : 'Icon wählen'
    },
  },
  methods: {
    iconLabel(key) {
      if (!key) return 'Icon wählen'
      return key
        .split(/[-_]/)
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    openDialog() {
      this.search = ''
      this.$refs.dialog?.open()
    },
    choose(key) {
      this.$emit('update:modelValue', key)
      this.$refs.dialog?.close()
    },
  },
}
</script>
