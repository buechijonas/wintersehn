<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">{{ label }}</h2>

        <textarea
          v-model="text"
          rows="24"
          spellcheck="false"
          :readonly="!authStore.user?.can_edit_content"
          class="textarea w-full font-mono text-xs"
        ></textarea>

        <p v-if="error" class="text-error text-sm mt-2">{{ error }}</p>
        <p v-if="saved" class="text-success text-sm mt-2">Gespeichert.</p>

        <div v-if="authStore.user?.can_edit_content" class="flex gap-4 mt-4">
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
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

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

export default {
  name: 'AdminContentView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter, BaseButton },
  data() {
    return {
      text: '',
      error: '',
      saved: false,
      saving: false,
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
      this.error = ''
      this.saved = false

      let data
      try {
        data = JSON.parse(this.text)
      } catch {
        this.error = 'Ungültiges JSON.'
        return
      }

      this.saving = true
      try {
        await this.contentStore.saveContent(this.key, data)
        this.saved = true
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
  },
}
</script>
