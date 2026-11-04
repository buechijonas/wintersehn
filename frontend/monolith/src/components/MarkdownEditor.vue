<template>
  <div class="flex flex-col rounded-box border border-wntrs-border">
    <div
      class="flex flex-wrap items-center justify-between gap-2 border-b border-wntrs-border px-2 py-1.5"
    >
      <div class="join">
        <BaseButton
          v-for="tab in tabs"
          :key="tab.key"
          size="xs"
          class="join-item"
          :variant="mode === tab.key ? 'primary' : 'neutral'"
          @click="mode = tab.key"
        >
          {{ tab.label }}
        </BaseButton>
      </div>
      <div v-if="mode === 'write'" class="flex flex-wrap gap-0.5">
        <BaseButton
          v-for="tool in tools"
          :key="tool.label"
          variant="ghost"
          size="xs"
          class="font-mono min-w-7"
          :title="tool.title"
          @click="tool.apply()"
        >
          {{ tool.label }}
        </BaseButton>
      </div>
    </div>

    <textarea
      v-show="mode === 'write'"
      :id="id"
      ref="textarea"
      :value="modelValue"
      class="textarea w-full min-h-96 border-0 rounded-t-none font-mono text-sm leading-relaxed [field-sizing:content] focus:outline-none"
      placeholder="Text in Markdown schreiben …"
      @input="$emit('update:modelValue', $event.target.value)"
    ></textarea>

    <MarkdownContent v-if="mode === 'preview'" :text="modelValue" class="min-h-96 px-4 py-3" />
  </div>
</template>

<script>
import BaseButton from '@core/components/common/BaseButton.vue'
import MarkdownContent from '@/components/MarkdownContent.vue'

export default {
  name: 'MarkdownEditor',
  components: { BaseButton, MarkdownContent },
  props: {
    modelValue: { type: String, default: '' },
    id: { type: String, default: undefined },
  },
  emits: ['update:modelValue'],
  data() {
    return {
      mode: 'write',
      tabs: [
        { key: 'write', label: 'Schreiben' },
        { key: 'preview', label: 'Vorschau' },
      ],
      tools: [
        { label: 'B', title: 'Fett', apply: () => this.wrap('**', '**', 'fett') },
        { label: 'I', title: 'Kursiv', apply: () => this.wrap('_', '_', 'kursiv') },
        { label: 'H', title: 'Überschrift', apply: () => this.prefix('## ') },
        { label: '•', title: 'Liste', apply: () => this.prefix('- ') },
        { label: '1.', title: 'Nummerierte Liste', apply: () => this.prefix('1. ') },
        { label: '❝', title: 'Zitat', apply: () => this.prefix('> ') },
        { label: '</>', title: 'Code', apply: () => this.wrap('`', '`', 'code') },
        { label: '🔗', title: 'Link', apply: () => this.wrap('[', '](https://)', 'Linktext') },
      ],
    }
  },
  methods: {
    replace(start, end, text, selectFrom, selectTo) {
      const value = this.modelValue
      this.$emit('update:modelValue', value.slice(0, start) + text + value.slice(end))
      this.$nextTick(() => {
        this.$refs.textarea.focus()
        this.$refs.textarea.setSelectionRange(start + selectFrom, start + selectTo)
      })
    },
    wrap(before, after, fallback) {
      const { selectionStart: start, selectionEnd: end } = this.$refs.textarea
      const selected = this.modelValue.slice(start, end) || fallback
      this.replace(
        start,
        end,
        before + selected + after,
        before.length,
        before.length + selected.length,
      )
    },
    prefix(marker) {
      const { selectionStart, selectionEnd } = this.$refs.textarea
      const start = this.modelValue.lastIndexOf('\n', selectionStart - 1) + 1
      const lines = this.modelValue.slice(start, selectionEnd).split('\n')
      const text = lines.map((line) => marker + line).join('\n')
      this.replace(start, selectionEnd, text, text.length, text.length)
    },
  },
}
</script>
