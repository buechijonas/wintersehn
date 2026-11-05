<template>
  <section>
    <div class="flex items-center justify-between gap-4 my-4">
      <h3 class="text-xl">{{ title }}</h3>
      <input
        type="checkbox"
        class="toggle toggle-primary"
        :aria-label="`${title} aktivieren`"
        :checked="enabled"
        :disabled="locked"
        @change="$emit('update:enabled', $event.target.checked)"
      />
    </div>
    <BaseCard class="p-6 flex flex-col gap-4" :class="{ 'opacity-60': !enabled }">
      <p class="text-wntrs-muted">{{ description }}</p>
      <slot name="notice" />
      <form v-if="!locked" class="flex gap-2" @submit.prevent="add">
        <input
          v-model="input"
          type="text"
          inputmode="url"
          autocomplete="off"
          placeholder="Link oder Domain einfügen"
          :aria-label="`${title}: Link oder Domain`"
          class="input w-full rounded-full border-wntrs-field focus:border-primary focus:outline-none"
        />
        <BaseButton type="submit" variant="primary" shape="circle" :disabled="!input.trim()">
          <AppIcon name="plus" alt="Hinzufügen" />
        </BaseButton>
      </form>
      <p v-if="invalid" class="text-error text-sm">Das ist kein gültiger Link.</p>
      <ul v-if="domains.length" class="flex max-h-64 flex-wrap gap-2 overflow-y-auto">
        <li
          v-for="domain in domains"
          :key="domain"
          class="flex items-center gap-1 rounded-full border border-wntrs-border pl-3 text-sm"
          :class="locked ? 'pr-3' : 'pr-1'"
        >
          {{ domain }}
          <BaseButton
            v-if="!locked"
            variant="ghost"
            size="xs"
            shape="circle"
            @click="
              $emit(
                'update:domains',
                domains.filter((item) => item !== domain),
              )
            "
          >
            <AppIcon name="cross" size="sm" :alt="`${domain} entfernen`" />
          </BaseButton>
        </li>
      </ul>
      <div v-if="domains.length" class="flex items-center justify-between gap-4">
        <span class="text-sm text-wntrs-muted">{{ domains.length }} Einträge</span>
        <BaseButton
          v-if="!locked"
          size="sm"
          variant="error"
          outline
          @click="$emit('update:domains', [])"
        >
          <AppIcon name="trash" />
          Liste leeren
        </BaseButton>
      </div>
    </BaseCard>
  </section>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { toDomain } from '@/lib/domains.js'

export default {
  name: 'DomainListSettings',
  components: { AppIcon, BaseButton, BaseCard },
  props: {
    title: { type: String, required: true },
    description: { type: String, required: true },
    enabled: { type: Boolean, required: true },
    domains: { type: Array, required: true },
    locked: { type: Boolean, default: false },
  },
  emits: ['update:enabled', 'update:domains'],
  data() {
    return {
      input: '',
      invalid: false,
    }
  },
  methods: {
    add() {
      const domain = toDomain(this.input)
      this.invalid = !domain
      if (!domain) return
      this.input = ''
      if (this.domains.includes(domain)) return
      this.$emit('update:domains', [...this.domains, domain])
    },
  },
}
</script>
