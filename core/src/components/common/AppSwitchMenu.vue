<template>
  <ul tabindex="0" class="dropdown-content menu left-0 z-40 rounded-none bg-base-100 p-0 shadow-sm">
    <li v-for="target in targets" :key="target.url">
      <a :href="target.url" class="flex items-center gap-3 rounded-none" :class="itemClass">
        <img :src="`${target.url}/icons/maskable-512.png`" alt="" class="size-6" />
        <span>{{ target.label }}</span>
      </a>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'AppSwitchMenu',
  props: {
    targets: {
      type: Array,
      required: true,
    },
    itemClass: {
      type: String,
      default: '',
    },
  },
}
</script>
