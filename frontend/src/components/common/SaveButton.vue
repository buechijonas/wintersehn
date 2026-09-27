<template>
  <BaseButton variant="neutral" shape="square" size="sm" title="Speichern">
    <AppIcon name="disk" alt="Speichern" />
  </BaseButton>
</template>

<script>
import BaseButton from '@/components/common/BaseButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

export default {
  name: 'SaveButton',
  components: { BaseButton, AppIcon },
}
</script>
