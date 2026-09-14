<template>
  <Page active-navigation="admin">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Neuer Eintrag</h2>

        <Card v-if="section" class="p-6">
          <form class="fieldset" @submit.prevent="save">
            <label class="label" for="ethos-item-title">Titel</label>
            <input
              id="ethos-item-title"
              v-model="title"
              type="text"
              class="input w-full"
              required
            />

            <label class="label mt-4">Icon</label>
            <div class="flex items-center gap-4">
              <Card class="size-16 shrink-0 flex items-center justify-center p-2">
                <img v-if="selectedIcon" class="size-11" :src="flatIcons[selectedIcon]" alt="" />
              </Card>

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
                  <li v-for="key in iconKeys" :key="key">
                    <a :class="{ active: selectedIcon === key }" @click="chooseIcon(key)">
                      <img class="size-6" :src="flatIcons[key]" alt="" />
                      {{ iconLabel(key) }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>

            <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

            <div class="flex gap-4 mt-4">
              <RouterLink to="/admin/ethos" class="btn shadow-none">Abbrechen</RouterLink>
              <button type="submit" class="btn btn-primary shadow-none" :disabled="saving">
                Speichern
              </button>
            </div>
          </form>
        </Card>
      </div>
    </div>
    <Footer />
  </Page>
</template>

<script>
import { RouterLink } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import Footer from '@/components/common/Footer.vue'
import { flats } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminEthosItemCreateView',
  components: { RouterLink, Page, Breadcrumbs, Card, Footer },
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
    flatIcons() {
      return flats
    },
    sectionIndex() {
      return Number(this.$route.params.section)
    },
    sections() {
      return this.contentStore.items.ethos?.data ?? []
    },
    section() {
      return this.sections[this.sectionIndex] ?? null
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Ethos', to: '/admin/ethos' },
        { label: this.section?.title ?? '…' },
      ]
    },
    iconKeys() {
      return Object.keys(flats).sort((a, b) => a.localeCompare(b, 'de'))
    },
  },
  mounted() {
    this.contentStore.fetchContent('ethos')
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
            ? { ...s, items: [...s.items, { icon: this.selectedIcon, label: this.title.trim() }] }
            : s,
        )
        await this.contentStore.saveContent('ethos', data)
        this.$router.push('/admin/ethos')
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
