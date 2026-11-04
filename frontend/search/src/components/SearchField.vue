<template>
  <form role="search" @submit.prevent="submit">
    <label
      class="input input-lg h-14 w-full rounded-full border-2 border-wntrs-field pl-7 pr-2 focus-within:border-primary focus-within:outline-none"
    >
      <input
        v-model.trim="query"
        type="search"
        placeholder="Wonach suchst du?"
        aria-label="Suchen"
        autocomplete="off"
      />
      <button type="submit" aria-label="Suchen" class="btn btn-ghost btn-circle text-primary">
        <AppIcon name="search" class="size-5!" />
      </button>
    </label>
  </form>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'

export default {
  name: 'SearchField',
  components: { AppIcon },
  props: {
    modelValue: { type: String, default: '' },
  },
  emits: ['submit'],
  data() {
    return {
      query: this.modelValue,
    }
  },
  watch: {
    modelValue(value) {
      this.query = value
    },
  },
  methods: {
    submit() {
      if (!this.query) return
      this.$emit('submit', this.query)
    },
  },
}
</script>
