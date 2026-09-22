<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Konto bearbeiten</h2>

      <BaseCard class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <p class="text-wntrs-muted text-sm">
            Benutzername und E-Mail verwaltest du auf
            <a href="/api/auth/oidc/account/" class="link link-primary">govex</a>.
          </p>

          <label class="label mt-4">Profilbild</label>
          <div class="flex items-center gap-4">
            <BaseCard class="size-16 shrink-0 flex items-center justify-center p-2">
              <img class="size-11" :src="avatarSrc(selectedAvatar)" alt="" />
            </BaseCard>

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
            <CancelButton to="/settings" />
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
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

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

export default {
  name: 'AccountEditView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, CancelButton },
  mixins: [asyncActionMixin],
  data() {
    const authStore = useAuthStore()
    return {
      icons,
      profiles,
      breadcrumbs: [
        { label: 'Einstellungen', to: '/settings' },
        { label: 'Konto bearbeiten' },
      ],
      selectedAvatar: authStore.user.avatar ?? '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    avatarKeys() {
      return Object.keys(profiles).sort((a, b) =>
        AVATAR_LABELS[a].localeCompare(AVATAR_LABELS[b], 'de'),
      )
    },
  },
  methods: {
    avatarLabel(key) {
      return key ? AVATAR_LABELS[key] : 'Kein Profilbild'
    },
    avatarSrc(key) {
      return key ? profiles[key] : icons.user
    },
    chooseAvatar(key) {
      this.selectedAvatar = key
      this.$refs.avatarMenu?.hidePopover()
    },
    async save() {
      await this.runAction(() =>
        this.authStore.updateProfile({ avatar: this.selectedAvatar }),
      )
      if (!this.error) this.$router.push('/settings')
    },
  },
}
</script>
