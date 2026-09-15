<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Neuer Eintrag</h2>

        <BaseCard v-if="section" class="p-6">
          <form class="fieldset" @submit.prevent="save">
            <label class="label" for="cv-entry-year">Jahr</label>
            <input id="cv-entry-year" v-model="year" type="text" class="input w-full" required />

            <label class="label mt-4" for="cv-entry-title">Titel</label>
            <input id="cv-entry-title" v-model="title" type="text" class="input w-full" required />

            <label class="label mt-4" for="cv-entry-description">Beschreibung</label>
            <input
              id="cv-entry-description"
              v-model="description"
              type="text"
              class="input w-full"
            />

            <label class="label mt-4">Icon</label>
            <div class="flex items-center gap-4">
              <BaseCard class="size-16 shrink-0 flex items-center justify-center p-2">
                <img
                  v-if="selectedIcon"
                  class="size-11"
                  :src="flatIcons[selectedIcon]"
                  alt=""
                />
                <img v-else class="size-11 opacity-40" :src="flatIcons[section.icon]" alt="" />
              </BaseCard>

              <div class="w-full">
                <button
                  type="button"
                  popovertarget="icon-menu"
                  style="anchor-name: --icon-menu-anchor"
                  class="select w-full flex items-center gap-2"
                >
                  <img v-if="selectedIcon" class="size-5" :src="flatIcons[selectedIcon]" alt="" />
                  <span>{{ iconLabel(selectedIcon) }}</span>
                </button>

                <ul
                  id="icon-menu"
                  ref="iconMenu"
                  popover
                  class="dropdown menu rounded-box bg-base-100 shadow-sm max-h-72 overflow-y-auto flex-nowrap"
                  style="position-anchor: --icon-menu-anchor; width: anchor-size(width)"
                >
                  <li>
                    <a :class="{ active: !selectedIcon }" @click="chooseIcon('')">
                      <img class="size-6" :src="flatIcons[section.icon]" alt="" />
                      Abschnitts-Icon (Standard)
                    </a>
                  </li>
                  <li v-for="key in iconKeys" :key="key">
                    <a :class="{ active: selectedIcon === key }" @click="chooseIcon(key)">
                      <img class="size-6" :src="flatIcons[key]" alt="" />
                      {{ iconLabel(key) }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>

            <label class="label mt-4">Links</label>
            <div class="flex flex-col gap-2">
              <div v-for="(link, linkIndex) in links" :key="linkIndex" class="flex gap-2">
                <input
                  v-model="link.label"
                  type="text"
                  placeholder="Beschriftung"
                  class="input w-full"
                />
                <input v-model="link.url" type="url" placeholder="URL" class="input w-full" />
                <DeleteButton @click="removeLink(linkIndex)" />
              </div>
              <BaseButton type="button" size="sm" @click="addLink">Link hinzufügen</BaseButton>
            </div>

            <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

            <div class="flex gap-4 mt-4">
              <CancelButton :to="`/admin/cv/${key}`" />
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
import DeleteButton from '@/components/common/DeleteButton.vue'
import { flats } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminCvEntryCreateView',
  components: {
    BasePage,
    BaseBreadcrumbs,
    BaseCard,
    BaseFooter,
    BaseButton,
    CancelButton,
    DeleteButton,
  },
  data() {
    return {
      year: '',
      title: '',
      description: '',
      selectedIcon: '',
      links: [],
      error: '',
      saving: false,
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    flatIcons() {
      return flats
    },
    key() {
      return this.$route.params.key
    },
    categories() {
      return this.contentStore.items.cv?.data ?? []
    },
    location() {
      for (let categoryIndex = 0; categoryIndex < this.categories.length; categoryIndex++) {
        const itemIndex = this.categories[categoryIndex].items.findIndex(
          (item) => item.key === this.key,
        )
        if (itemIndex !== -1) return { categoryIndex, itemIndex }
      }
      return null
    },
    section() {
      if (!this.location) return null
      return this.categories[this.location.categoryIndex].items[this.location.itemIndex]
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Lebenslauf', to: '/admin/cv' },
        { label: this.section?.label ?? '…', to: `/admin/cv/${this.key}` },
        { label: 'Neuer Eintrag' },
      ]
    },
    iconKeys() {
      return Object.keys(flats).sort((a, b) => a.localeCompare(b, 'de'))
    },
  },
  mounted() {
    this.contentStore.fetchContent('cv')
  },
  methods: {
    iconLabel(key) {
      if (!key) return 'Abschnitts-Icon (Standard)'
      return key
        .split('-')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    chooseIcon(key) {
      this.selectedIcon = key
      this.$refs.iconMenu?.hidePopover()
    },
    addLink() {
      this.links.push({ label: '', url: '' })
    },
    removeLink(index) {
      this.links.splice(index, 1)
    },
    async save() {
      this.error = ''
      if (!this.year.trim() || !this.title.trim()) {
        this.error = 'Jahr und Titel sind erforderlich.'
        return
      }

      this.saving = true
      try {
        const timeline = this.section.timeline ?? []
        const links = this.links.filter((link) => link.label.trim() && link.url.trim())
        const entry = {
          side: timeline.length % 2 === 0 ? 'start' : 'end',
          year: this.year.trim(),
          title: this.title.trim(),
          description: this.description.trim(),
          ...(this.selectedIcon ? { icon: this.selectedIcon } : {}),
          ...(links.length ? { links } : {}),
        }

        const { categoryIndex, itemIndex } = this.location
        const categories = this.categories.map((category, ci) =>
          ci !== categoryIndex
            ? category
            : {
                ...category,
                items: category.items.map((item, ii) =>
                  ii !== itemIndex ? item : { ...item, timeline: [...timeline, entry] },
                ),
              },
        )
        await this.contentStore.saveContent('cv', categories)
        this.$router.push(`/admin/cv/${this.key}`)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
