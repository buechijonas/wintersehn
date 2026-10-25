<template>
  <div class="flex flex-col gap-4 min-h-0">
    <div class="flex flex-wrap items-center gap-2">
      <input
        v-model.trim="query"
        type="search"
        placeholder="Dateiname suchen"
        aria-label="Dateiname suchen"
        class="input input-sm flex-1 min-w-40"
      />
      <input ref="file" type="file" accept="image/*" multiple class="hidden" @change="upload" />
      <BaseButton size="sm" :disabled="saving" @click="$refs.file.click()">
        <AppIcon name="plus" />
        Hochladen
      </BaseButton>
      <BaseButton
        v-if="!selectable && unusedCount"
        variant="neutral"
        size="sm"
        :disabled="saving"
        @click="$refs.confirmUnused.open()"
      >
        <AppIcon name="trash" />
        {{ unusedCount }} unbenutzte löschen
      </BaseButton>
    </div>

    <p v-if="error" class="text-error text-sm">{{ error }}</p>

    <div v-if="!images" class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
      <div v-for="n in 8" :key="n" class="skeleton aspect-square w-full"></div>
    </div>

    <p v-else-if="!visible.length" class="py-8 text-center text-sm text-wntrs-muted">
      {{ images.length ? 'Kein Bild gefunden.' : 'Noch keine Bilder hochgeladen.' }}
    </p>

    <ul v-else class="grid grid-cols-2 gap-3 overflow-y-auto sm:grid-cols-3 md:grid-cols-4">
      <li
        v-for="image in visible"
        :key="image.uuid"
        class="flex flex-col overflow-hidden rounded-box border border-wntrs-border"
        :class="{ 'ring-2 ring-primary': image.uuid === selected }"
      >
        <component
          :is="selectable ? 'button' : 'div'"
          :type="selectable ? 'button' : undefined"
          class="block w-full aspect-square overflow-hidden bg-base-200"
          :class="{ 'cursor-pointer hover:opacity-80': selectable }"
          :title="selectable ? `${image.name} wählen` : image.name"
          @click="selectable && $emit('select', image)"
        >
          <img
            :src="dossiersStore.imageUrl(image.uuid, 256)"
            :alt="image.name"
            loading="lazy"
            class="size-full object-cover"
          />
        </component>
        <div class="flex items-center gap-1 px-2 py-1.5">
          <div class="flex flex-col min-w-0 flex-1">
            <span class="text-xs font-bold truncate" :title="image.name">{{ image.name }}</span>
            <span class="text-xs" :class="image.usage ? 'text-wntrs-muted' : 'text-warning'">
              {{ image.usage ? `${image.usage}× verwendet` : 'Unbenutzt' }}
            </span>
          </div>
          <BaseButton
            variant="ghost"
            shape="square"
            size="xs"
            :title="`${image.name} umbenennen`"
            :disabled="saving"
            @click="startRename(image)"
          >
            <AppIcon name="pencil" :alt="`${image.name} umbenennen`" />
          </BaseButton>
          <BaseButton
            variant="ghost"
            shape="square"
            size="xs"
            :title="`${image.name} löschen`"
            :disabled="saving"
            @click="requestRemove(image)"
          >
            <AppIcon name="trash" :alt="`${image.name} löschen`" />
          </BaseButton>
        </div>
      </li>
    </ul>

    <SectionDialog
      ref="renameDialog"
      title="Bild umbenennen"
      placeholder="Dateiname"
      label="Dateiname"
      confirm-label="Speichern"
      confirm-icon="disk"
      @confirm="rename"
    />
    <ConfirmDialog
      ref="confirmRemove"
      title="Bild wird verwendet"
      :message="`«${removing?.name}» wird ${removing?.usage}× in Chats verwendet. Wenn du es löschst, verschwindet es dort als Profilbild oder Nachrichtenbild. Trotzdem endgültig vom Server löschen?`"
      @confirm="remove(removing)"
    />
    <ConfirmDialog
      ref="confirmUnused"
      title="Unbenutzte Bilder löschen"
      :message="`Möchtest du ${unusedCount} Bilder, die in keinem Chat verwendet werden, endgültig vom Server löschen?`"
      @confirm="removeUnused"
    />
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import ConfirmDialog from '@core/components/common/ConfirmDialog.vue'
import SectionDialog from '@core/components/common/SectionDialog.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import { useDossiersStore } from '@/stores/dossiers.js'

export default {
  name: 'ImageLibrary',
  components: { AppIcon, BaseButton, ConfirmDialog, SectionDialog },
  mixins: [asyncActionMixin],
  props: {
    selectable: { type: Boolean, default: false },
    selected: { type: String, default: null },
  },
  emits: ['select', 'removed'],
  data() {
    return {
      images: null,
      query: '',
      renaming: null,
      removing: null,
    }
  },
  computed: {
    dossiersStore() {
      return useDossiersStore()
    },
    visible() {
      const query = this.query.toLowerCase()
      return this.images.filter((image) => image.name.toLowerCase().includes(query))
    },
    unusedCount() {
      return this.images?.filter((image) => !image.usage).length ?? 0
    },
  },
  mounted() {
    return this.load()
  },
  methods: {
    load() {
      return this.runAction(async () => {
        this.images = await this.dossiersStore.fetchImages()
      })
    },
    upload(event) {
      const files = [...event.target.files]
      event.target.value = ''
      return this.runAction(async () => {
        const uploaded = await Promise.all(
          files.map((file) => this.dossiersStore.uploadImage(file)),
        )
        const known = new Set(this.images.map((image) => image.uuid))
        this.images = [...uploaded.filter((image) => !known.has(image.uuid)), ...this.images]
        if (this.selectable && uploaded.length === 1) this.$emit('select', uploaded[0])
      })
    },
    startRename(image) {
      this.renaming = image
      this.$refs.renameDialog.open(image.name)
    },
    rename(name) {
      return this.runAction(async () => {
        const renamed = await this.dossiersStore.renameImage(this.renaming.uuid, name)
        this.images = this.images.map((image) => (image.uuid === renamed.uuid ? renamed : image))
      })
    },
    requestRemove(image) {
      if (!image.usage) return this.remove(image)
      this.removing = image
      this.$refs.confirmRemove.open()
    },
    remove(image) {
      return this.runAction(async () => {
        await this.dossiersStore.deleteImage(image.uuid)
        this.images = this.images.filter((other) => other.uuid !== image.uuid)
        this.$emit('removed', image.uuid)
      })
    },
    removeUnused() {
      return this.runAction(async () => {
        this.images = await this.dossiersStore.deleteUnusedImages()
      })
    },
  },
}
</script>
