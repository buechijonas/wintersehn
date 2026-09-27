<template>
  <BaseButton variant="neutral" shape="square" size="sm" class="text-error" title="Löschen">
    <AppIcon name="trash" class="size-4 icon-tint-error" alt="Löschen" />
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'DeleteButton',
  components: { BaseButton, AppIcon },
}
</script>
