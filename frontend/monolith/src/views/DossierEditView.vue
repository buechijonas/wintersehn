<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div
    class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1"
  >
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Meta bearbeiten</h2>

      <div v-if="!draft && !error" class="skeleton h-96 w-full"></div>

      <BaseCard v-else-if="draft" class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <template v-for="field in fields" :key="field.key">
            <label class="label not-first:mt-4" :for="`dossier-${field.key}`">{{
              field.label
            }}</label>
            <select
              v-if="field.options"
              :id="`dossier-${field.key}`"
              v-model="draft[field.key]"
              class="select w-full"
            >
              <option value="">–</option>
              <option v-for="option in field.options" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
            <input
              v-else
              :id="`dossier-${field.key}`"
              v-model.trim="draft[field.key]"
              :type="field.type"
              v-bind="field.attrs"
              class="input w-full"
            />
          </template>

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex justify-end gap-4 mt-4">
            <CancelButton :to="detailRoute" />
            <BaseButton type="submit" variant="primary" :disabled="saving">
              <AppIcon name="disk" />
              Speichern
            </BaseButton>
          </div>
        </form>
      </BaseCard>
    </div>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { metaFields } from '@/data/dossierFields.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'DossierEditView',
  components: { AppIcon, BaseBreadcrumbs, BaseButton, BaseCard, CancelButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      fields: metaFields,
      draft: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    uuid() {
      return this.$route.params.uuid
    },
    detailRoute() {
      return { name: 'dossier', params: { uuid: this.uuid } }
    },
    breadcrumbs() {
      return [
        { label: 'Personalakten', to: '/' },
        { label: this.draft?.title || '…', to: this.detailRoute },
        { label: 'Meta bearbeiten' },
      ]
    },
  },
  async mounted() {
    await this.runAction(() => this.dossiersStore.fetchDossier(this.uuid))
    const dossier = this.dossiersStore.current
    this.draft = dossier && { ...dossier, birthdate: dossier.birthdate ?? '' }
  },
  methods: {
    save() {
      const data = { ...this.draft, birthdate: this.draft.birthdate || null }
      return this.runAction(async () => {
        await this.dossiersStore.updateDossier(this.uuid, data)
        this.$router.push(this.detailRoute)
      })
    },
  },
}
</script>
