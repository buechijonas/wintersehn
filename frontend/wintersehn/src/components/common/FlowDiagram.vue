<template>
  <BaseCard class="flex flex-col gap-2 p-4">
    <button
      type="button"
      class="cursor-zoom-in overflow-x-auto text-left"
      :aria-label="`${title} vergrössern`"
      @click="$refs.dialog.open()"
    >
      <DiagramCanvas :title="title" :columns="columns" :edges="edges" class="min-w-160" />
    </button>
    <span class="flex items-center gap-1 self-end text-xs text-wntrs-muted">
      <AppIcon name="expand" />
      Zum Vergrössern anklicken
    </span>
    <BaseDialog
      ref="dialog"
      :title="title"
      box-class="h-[100dvh] max-h-none w-screen max-w-none rounded-none"
    >
      <DiagramCanvas
        :title="title"
        :columns="columns"
        :edges="edges"
        variant="dialog"
        class="m-auto max-h-full"
      />
    </BaseDialog>
  </BaseCard>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import DiagramCanvas from '@/components/common/DiagramCanvas.vue'

export default {
  name: 'FlowDiagram',
  components: { AppIcon, BaseCard, BaseDialog, DiagramCanvas },
  props: {
    title: { type: String, required: true },
    columns: { type: Array, required: true },
    edges: { type: Array, default: () => [] },
  },
}
</script>
