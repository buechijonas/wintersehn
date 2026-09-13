<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Card from '@/components/common/Card.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const router = useRouter()

const breadcrumbs = [
  { label: 'Einstellungen', to: '/settings' },
  { label: 'Konto bearbeiten' },
]

const AVATAR_LABELS = {
  bee: 'Biene',
  bison: 'Bison',
  camel: 'Kamel',
  cat: 'Katze',
  chameleon: 'Chamäleon',
  crab: 'Krabbe',
  deer: 'Hirsch',
  dog: 'Hund',
  dolphin: 'Delfin',
  duck: 'Ente',
  elephant: 'Elefant',
  fish: 'Fisch',
  flamingo: 'Flamingo',
  frog: 'Frosch',
  giraffe: 'Giraffe',
  hedgehog: 'Igel',
  hen: 'Henne',
  'hermit-crab': 'Einsiedlerkrebs',
  hippopotamus: 'Nilpferd',
  horse: 'Pferd',
  jellyfish: 'Qualle',
  kangaroo: 'Känguru',
  kiwi: 'Kiwi',
  koala: 'Koala',
  lion: 'Löwe',
  llama: 'Lama',
  lobster: 'Hummer',
  meerkat: 'Erdmännchen',
  monkey: 'Affe',
  octopus: 'Oktopus',
  ostrich: 'Strauss',
  owl: 'Eule',
  'panda-bear': 'Pandabär',
  parrot: 'Papagei',
  penguin: 'Pinguin',
  pig: 'Schwein',
  rabbit: 'Kaninchen',
  seahorse: 'Seepferdchen',
  seal: 'Robbe',
  shark: 'Hai',
  sheep: 'Schaf',
  snail: 'Schnecke',
  snake: 'Schlange',
  squid: 'Tintenfisch',
  squirrel: 'Eichhörnchen',
  swan: 'Schwan',
  toucan: 'Tukan',
  turtle: 'Schildkröte',
  walrus: 'Walross',
  whale: 'Wal',
}

const avatarKeys = Object.keys(profiles).sort((a, b) =>
  AVATAR_LABELS[a].localeCompare(AVATAR_LABELS[b], 'de'),
)

function avatarLabel(key) {
  return key ? AVATAR_LABELS[key] : 'Kein Profilbild'
}

function avatarSrc(key) {
  return key ? profiles[key] : icons.user
}

const username = ref(authStore.user.username)
const email = ref(authStore.user.email)
const selectedAvatar = ref(authStore.user.avatar ?? '')
const error = ref('')
const saving = ref(false)
const avatarMenu = ref(null)

function chooseAvatar(key) {
  selectedAvatar.value = key
  avatarMenu.value?.hidePopover()
}

async function save() {
  error.value = ''
  saving.value = true
  try {
    await authStore.updateProfile({
      username: username.value,
      email: email.value,
      avatar: selectedAvatar.value,
    })
    router.push('/settings')
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <Page>
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-150">
        <h2 class="text-xl font-light my-4">Konto bearbeiten</h2>

        <Card class="p-6">
          <form class="fieldset" @submit.prevent="save">
            <label class="label" for="account-username">Benutzername</label>
            <input
              id="account-username"
              v-model="username"
              type="text"
              autocomplete="username"
              class="input w-full"
              required
            />

            <label class="label mt-2" for="account-email">E-Mail</label>
            <input
              id="account-email"
              v-model="email"
              type="email"
              autocomplete="email"
              class="input w-full"
              required
            />

            <label class="label mt-4">Profilbild</label>
            <div class="flex items-center gap-4">
              <Card class="size-16 shrink-0 flex items-center justify-center p-2">
                <img class="size-11" :src="avatarSrc(selectedAvatar)" alt="" />
              </Card>

              <div class="w-full">
                <button
                  type="button"
                  popovertarget="avatar-menu"
                  style="anchor-name: --avatar-menu-anchor"
                  class="select w-full flex items-center gap-2"
                >
                  <img class="size-5" :src="avatarSrc(selectedAvatar)" alt="" />
                  <span>{{ avatarLabel(selectedAvatar) }}</span>
                </button>

                <ul
                  id="avatar-menu"
                  ref="avatarMenu"
                  popover
                  class="dropdown menu rounded-box bg-base-100 shadow-sm max-h-72 overflow-y-auto flex-nowrap"
                  style="position-anchor: --avatar-menu-anchor; width: anchor-size(width)"
                >
                  <li>
                    <a :class="{ active: selectedAvatar === '' }" @click="chooseAvatar('')">
                      <img class="size-6" :src="icons.user" alt="" />
                      Kein Profilbild
                    </a>
                  </li>
                  <li v-for="key in avatarKeys" :key="key">
                    <a :class="{ active: selectedAvatar === key }" @click="chooseAvatar(key)">
                      <img class="size-6" :src="profiles[key]" alt="" />
                      {{ avatarLabel(key) }}
                    </a>
                  </li>
                </ul>
              </div>
            </div>

            <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

            <div class="flex gap-4 mt-4">
              <RouterLink to="/settings" class="btn shadow-none">Abbrechen</RouterLink>
              <button type="submit" class="btn btn-primary shadow-none" :disabled="saving">
                Speichern
              </button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  </Page>
</template>
