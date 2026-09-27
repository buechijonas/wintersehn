<template>
  <BaseButton variant="neutral" shape="square" size="sm" title="Bearbeiten">
    <AppIcon name="pencil" alt="Bearbeiten" />
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'EditButton',
  components: { BaseButton, AppIcon },
}
</script>
