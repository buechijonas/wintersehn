<template>
  <div class="group dropdown dropdown-end" @keydown.esc="closeMenu">
    <div tabindex="0" role="button" class="btn shadow-none gap-2">
      <AppIcon name="menu-dots" />
      Aktionen
    </div>
    <ul
      tabindex="0"
      class="dropdown-content menu invisible group-focus-within:visible z-30 mt-2 w-52 rounded-box border border-wntrs-border bg-base-100 p-1"
    >
      <li v-for="link in links" :key="link.to">
        <RouterLink :to="link.to" class="flex h-10 items-center gap-3" @click="closeMenu">
          <AppIcon :name="link.icon" />
          {{ link.label }}
        </RouterLink>
      </li>
      <li>
        <RouterLink :to="editTo" class="flex h-10 items-center gap-3" @click="closeMenu">
          <AppIcon name="pencil" />
          Bearbeiten
        </RouterLink>
      </li>
      <li>
        <button type="button" class="flex h-10 items-center gap-3 text-error" @click="remove">
          <AppIcon name="trash" />
          Löschen
        </button>
      </li>
    </ul>
    <ConfirmDialog ref="confirm" :message="deleteMessage" @confirm="$emit('delete')" />
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import AppIcon from '@core/components/common/AppIcon.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import { closeMenu } from '@core/lib/menu.js'

export default {
  name: 'ActionsMenu',
  components: { AppIcon, ConfirmDialog, RouterLink },
  props: {
    links: { type: Array, default: () => [] },
    editTo: { type: String, required: true },
    deleteMessage: { type: String, required: true },
  },
  emits: ['delete'],
  methods: {
    closeMenu,
    remove() {
      closeMenu()
      this.$refs.confirm.open()
    },
  },
}
</script>
