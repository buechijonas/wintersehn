<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Neuer Eintrag</h2>

        <BaseCard v-if="section" class="p-6">
          <form class="fieldset" @submit.prevent="save">
            <label class="label" for="media-item-name">Name</label>
            <input
              id="media-item-name"
              v-model="name"
              type="text"
              class="input w-full"
              required
            />

            <label class="label mt-4" for="media-item-platform">Plattform</label>
            <input
              id="media-item-platform"
              v-model="platform"
              type="text"
              class="input w-full"
              required
            />

            <label class="label mt-4" for="media-item-url">Link</label>
            <input id="media-item-url" v-model="url" type="url" class="input w-full" required />

            <IconPickerField v-model="selectedIcon" :icons="mediaIcons" class="mt-4" />

            <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

            <div class="flex gap-4 mt-4">
              <CancelButton to="/admin/media" />
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
import IconPickerField from '@/components/common/IconPickerField.vue'
import { social } from '@/assets/images.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminMediaItemCreateView',
  components: {
    BasePage,
    BaseBreadcrumbs,
    BaseCard,
    BaseFooter,
    BaseButton,
    CancelButton,
    IconPickerField,
  },
  data() {
    return {
      name: '',
      platform: '',
      url: '',
      selectedIcon: '',
      error: '',
      saving: false,
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    mediaIcons() {
      return social
    },
    sectionIndex() {
      return Number(this.$route.params.section)
    },
    sections() {
      return this.contentStore.items.media?.data ?? []
    },
    section() {
      return this.sections[this.sectionIndex] ?? null
    },
    breadcrumbs() {
      return [
        { label: 'Admin', to: '/admin' },
        { label: 'Medien', to: '/admin/media' },
        { label: this.section?.title ?? '…' },
      ]
    },
  },
  mounted() {
    this.contentStore.fetchContent('media')
  },
  methods: {
    async save() {
      this.error = ''
      if (!this.name.trim() || !this.platform.trim() || !this.url.trim() || !this.selectedIcon) {
        this.error = 'Name, Plattform, Link und Icon sind erforderlich.'
        return
      }

      this.saving = true
      try {
        const item = {
          icon: this.selectedIcon,
          name: this.name.trim(),
          platform: this.platform.trim(),
          url: this.url.trim(),
        }
        const data = this.sections.map((s, i) =>
          i === this.sectionIndex ? { ...s, items: [...s.items, item] } : s,
        )
        await this.contentStore.saveContent('media', data)
        this.$router.push('/admin/media')
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
