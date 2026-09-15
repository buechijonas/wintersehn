<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
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

            <label class="label mt-4">Icon</label>
            <div class="flex items-center gap-4">
              <BaseCard class="size-16 shrink-0 flex items-center justify-center p-2">
                <img v-if="selectedIcon" class="size-11" :src="countryIcons[selectedIcon]" alt="" />
              </BaseCard>

              <div class="w-full">
                <button
                  type="button"
                  popovertarget="icon-menu"
                  style="anchor-name: --icon-menu-anchor"
                  class="select w-full flex items-center gap-2"
                >
                  <img v-if="selectedIcon" class="size-5" :src="countryIcons[selectedIcon]" alt="" />
                  <span>{{ iconLabel(selectedIcon) }}</span>
                </button>

                <ul
                  id="icon-menu"
                  ref="iconMenu"
                  popover
                  class="dropdown menu rounded-box bg-base-100 shadow-sm max-h-72 overflow-y-auto flex-nowrap"
                  style="position-anchor: --icon-menu-anchor; width: anchor-size(width)"
                >
                  <li v-for="key in iconKeys" :key="key">
                    <a :class="{ active: selectedIcon === key }" @click="chooseIcon(key)">
                      <img class="size-6" :src="countryIcons[key]" alt="" />
                      {{ iconLabel(key) }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>

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
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import CancelButton from '@/components/common/CancelButton.vue'
import { countries } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCountriesItemCreateView',
  components: { BasePage, BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, CancelButton },
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
    iconKeys() {
      return Object.keys(countries).sort((a, b) => a.localeCompare(b, 'de'))
    },
  },
  mounted() {
    this.contentStore.fetchContent('countries')
  },
  methods: {
    iconLabel(key) {
      if (!key) return 'Icon wählen'
      return key
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    chooseIcon(key) {
      this.selectedIcon = key
      this.$refs.iconMenu?.hidePopover()
    },
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
