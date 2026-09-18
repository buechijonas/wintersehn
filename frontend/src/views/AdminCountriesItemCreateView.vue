<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Neuer Eintrag</h2>

      <BaseCard v-if="section" class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <label class="label" for="country-item-title">Titel</label>
          <input
            id="country-item-title"
            v-model="title"
            type="text"
            class="input w-full"
            required
          />

          <IconPickerField v-model="selectedIcon" :icons="countryIcons" class="mt-4" />

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex gap-4 mt-4">
            <CancelButton to="/admin/countries" />
            <BaseButton type="submit" variant="primary" :disabled="saving">Speichern</BaseButton>
          </div>
        </form>
      </BaseCard>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import CancelButton from '@/components/common/CancelButton.vue'
import IconPickerField from '@/components/common/IconPickerField.vue'
import { countries } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCountriesItemCreateView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseFooter,
    BaseButton,
    CancelButton,
    IconPickerField,
  },
  data() {
    return {
      title: '',
      selectedIcon: '',
      error: '',
      saving: false,
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    countryIcons() {
      return countries
    },
    sectionIndex() {
      return Number(this.$route.params.section)
    },
    sections() {
      return this.contentStore.items.countries?.data ?? []
    },
    section() {
      return this.sections[this.sectionIndex] ?? null
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Länder', to: '/admin/countries' },
        { label: this.section?.title ?? '…' },
      ]
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
  methods: {
    async save() {
      this.error = ''
      if (!this.title.trim() || !this.selectedIcon) {
        this.error = 'Titel und Icon sind erforderlich.'
        return
      }

      this.saving = true
      try {
        const data = this.sections.map((s, i) =>
          i === this.sectionIndex
            ? {
                ...s,
                items: [
                  ...s.items,
                  { icon: this.selectedIcon, label: this.title.trim(), iconSet: 'countries' },
                ],
              }
            : s,
        )
        await this.contentStore.saveContent('countries', data)
        this.$router.push('/admin/countries')
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
