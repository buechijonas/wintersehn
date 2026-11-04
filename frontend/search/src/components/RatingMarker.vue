<template>
  <span class="relative z-10 flex focus-within:z-40">
    <template v-if="report">
      <div class="group dropdown hidden sm:flex" @keydown.esc="closeMenu">
        <div
          tabindex="0"
          role="button"
          :aria-label="icon.label"
          :title="icon.label"
          class="flex size-4 cursor-pointer rounded-sm focus:outline-none focus-visible:outline-1 focus-visible:outline-offset-1"
        >
          <AppIcon :name="icon.name" :class="icon.class" />
        </div>
        <div
          tabindex="0"
          class="dropdown-content invisible group-focus-within:visible z-30 mt-2 w-72 rounded-box border border-wntrs-border bg-base-100 p-4"
        >
          <RatingReport :report="report" />
        </div>
      </div>
      <button
        type="button"
        :aria-label="icon.label"
        class="active:scale-95 sm:hidden"
        :class="[mobileClass, icon.tone]"
        @click="$refs.dialog.open()"
      >
        <AppIcon :name="icon.name" :class="icon.class" />
      </button>
      <BaseDialog ref="dialog" :title="host">
        <RatingReport :report="report" />
      </BaseDialog>
    </template>
    <span v-else :title="icon.label" class="sm:flex sm:size-4" :class="[mobileClass, icon.tone]">
      <AppIcon :name="icon.name" :alt="icon.label" :class="icon.class" />
    </span>
  </span>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseDialog from '@core/components/common/BaseDialog.vue'
import RatingReport from '@/components/RatingReport.vue'
import { ratingIcons } from '@/data/ratings.js'
import { closeMenu } from '@/lib/menu.js'

export default {
  name: 'RatingMarker',
  components: { AppIcon, BaseDialog, RatingReport },
  props: {
    rating: { type: String, required: true },
    report: { type: Object, default: null },
    host: { type: String, default: '' },
  },
  data() {
    return {
      mobileClass: 'flex shrink-0 items-center justify-center rounded-full max-sm:size-8',
    }
  },
  computed: {
    icon() {
      return ratingIcons[this.rating]
    },
  },
  methods: {
    closeMenu,
  },
}
</script>
