<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
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

const route = useRoute()
const authStore = useAuthStore()
const contentStore = useContentStore()

const key = computed(() => route.params.key)
const label = computed(() => SECTION_LABELS[key.value] ?? key.value)
const breadcrumbs = computed(() => [
  { label: 'Admin', to: '/admin' },
  { label: label.value },
])

const text = ref('')
const error = ref('')
const saved = ref(false)
const saving = ref(false)

async function load() {
  error.value = ''
  saved.value = false
  const data = await contentStore.fetchContent(key.value)
  text.value = JSON.stringify(data, null, 2)
}

onMounted(load)
watch(key, load)

function downloadBackup() {
  const blob = new Blob([text.value], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${key.value}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const fileInput = ref(null)

function pickFile() {
  fileInput.value?.click()
}

async function onFileSelected(event) {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return

  error.value = ''
  saved.value = false
  const content = await file.text()
  try {
    JSON.parse(content)
  } catch {
    error.value = 'Datei enthält kein gültiges JSON.'
    return
  }
  text.value = content
}

async function save() {
  error.value = ''
  saved.value = false

  let data
  try {
    data = JSON.parse(text.value)
  } catch {
    error.value = 'Ungültiges JSON.'
    return
  }

  saving.value = true
  try {
    await contentStore.saveContent(key.value, data)
    saved.value = true
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <Page active-navigation="admin">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 max-h-[calc(100vh-101px)] overflow-y-auto">
      <div class="mx-auto w-200">
        <h2 class="title-category my-4">{{ label }}</h2>

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
          <button type="button" class="btn shadow-none" @click="pickFile">Datei hochladen</button>
          <button type="button" class="btn shadow-none" @click="downloadBackup">
            Als Datei sichern
          </button>
          <button
            type="button"
            class="btn btn-primary shadow-none"
            :disabled="saving"
            @click="save"
          >
            Speichern
          </button>
        </div>
      </div>
    </div>
  </Page>
</template>
