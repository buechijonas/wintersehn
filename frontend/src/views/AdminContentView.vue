<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ label }}</h2>

      <textarea
        v-model="text"
        rows="24"
        spellcheck="false"
        :readonly="!canEdit"
        class="textarea w-full font-mono text-xs"
      ></textarea>

      <p v-if="error" class="text-error text-sm mt-2">{{ error }}</p>
      <p v-if="saved" class="text-success text-sm mt-2">Gespeichert.</p>

      <div v-if="canEdit" class="flex gap-4 mt-4">
        <input
          ref="fileInput"
          type="file"
          accept="application/json"
          class="hidden"
          @change="onFileSelected"
        />
        <BaseButton @click="pickFile">Datei hochladen</BaseButton>
        <BaseButton @click="downloadBackup">Als Datei sichern</BaseButton>
        <BaseButton variant="primary" :disabled="saving" @click="save">Speichern</BaseButton>
      </div>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

const SECTION_LABELS = {
  about: 'Über mich',
  ethos: 'Ethos',
  cv: 'Lebenslauf',
  countries: 'Länder',
  media: 'Medien',
  impressum: 'Impressum',
  privacy: 'Datenschutzerklärung',
  cookies: 'Cookierichtlinien',
  terms: 'Nutzungsrichtlinien',
  disclaimer: 'Haftungsausschluss',
}

const CHANGE_PERMISSION_BY_KEY = {
  about: 'can_change_about',
  ethos: 'can_change_ethos',
  cv: 'can_change_cv',
  countries: 'can_change_countries',
  media: 'can_change_media',
}

export default {
  name: 'AdminContentView',
  components: { BaseBreadcrumbs, BaseFooter, BaseButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      text: '',
      saved: false,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    key() {
      return this.$route.params.key
    },
    label() {
      return SECTION_LABELS[this.key] ?? this.key
    },
    canEdit() {
      const flag = CHANGE_PERMISSION_BY_KEY[this.key]
      return flag ? !!this.authStore.user?.[flag] : !!this.authStore.user?.can_edit_content
    },
    breadcrumbs() {
      return [{ label: 'Admin', to: '/admin' }, { label: this.label }]
    },
  },
  watch: {
    key: 'load',
  },
  mounted() {
    this.load()
  },
  methods: {
    async load() {
      this.error = ''
      this.saved = false
      const data = await this.contentStore.fetchContent(this.key)
      this.text = JSON.stringify(data, null, 2)
    },
    downloadBackup() {
      const blob = new Blob([this.text], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${this.key}.json`
      link.click()
      URL.revokeObjectURL(url)
    },
    pickFile() {
      this.$refs.fileInput?.click()
    },
    async onFileSelected(event) {
      const file = event.target.files?.[0]
      event.target.value = ''
      if (!file) return

      this.error = ''
      this.saved = false
      const content = await file.text()
      try {
        JSON.parse(content)
      } catch {
        this.error = 'Datei enthält kein gültiges JSON.'
        return
      }
      this.text = content
    },
    async save() {
      this.saved = false

      let data
      try {
        data = JSON.parse(this.text)
      } catch {
        this.error = 'Ungültiges JSON.'
        return
      }

      await this.runAction(() => this.contentStore.saveContent(this.key, data))
      if (!this.error) this.saved = true
    },
  },
}
</script>
