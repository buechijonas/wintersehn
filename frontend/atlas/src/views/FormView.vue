<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="loading" :error="error">
    <template v-if="item" #actions>
      <DeleteAction :message="type.deleteMessage(item)" @confirm="destroy" />
    </template>
    <div class="mx-auto flex w-full max-w-160 flex-col gap-4">
      <h2 class="text-xl font-light">{{ title }}</h2>
      <BaseCard tag="form" class="flex flex-col gap-6 rounded-box p-6" @submit.prevent="save">
        <label class="flex flex-col gap-2">
          <span class="text-sm text-wntrs-muted">{{ type.label }}</span>
          <input
            v-model="value"
            type="text"
            :placeholder="type.placeholder"
            class="input w-full border-wntrs-border focus:border-primary focus:outline-none"
          />
        </label>
        <div class="grid grid-cols-2 gap-2 sm:flex sm:justify-end">
          <CancelButton :to="cancelTarget" />
          <BaseButton type="submit" variant="primary" :disabled="saving || !value.trim()">
            <AppIcon :name="editing ? 'disk' : 'plus'" />
            {{ editing ? 'Speichern' : 'Erstellen' }}
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </AtlasPage>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import CancelButton from '@core/components/common/CancelButton.vue'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'
import AtlasPage from '@/components/AtlasPage.vue'
import DeleteAction from '@/components/DeleteAction.vue'
import { formTypes } from '@/lib/forms.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'FormView',
  components: { AppIcon, AtlasPage, BaseButton, BaseCard, CancelButton, DeleteAction },
  mixins: [asyncActionMixin],
  data() {
    return {
      parent: null,
      item: null,
      value: '',
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    type() {
      return formTypes[this.$route.meta.form]
    },
    editing() {
      return this.$route.meta.mode === 'edit'
    },
    uuid() {
      return this.$route.params.uuid
    },
    parentPath() {
      return this.type.parent(this.uuid)
    },
    loading() {
      return this.editing ? !this.item : Boolean(this.parentPath && !this.parent)
    },
    title() {
      return this.editing ? this.type.editTitle : this.type.createTitle
    },
    breadcrumbs() {
      return [
        ...this.type.breadcrumbs({ parent: this.parent, item: this.item }),
        { label: this.title },
      ]
    },
    cancelTarget() {
      if (this.editing) return this.type.target({ uuid: this.uuid })
      return this.parentPath ? this.parentPath.slice(0, -1) : '/'
    },
  },
  mounted() {
    this.runAction(async () => {
      if (this.editing) {
        this.item = await this.store.load(this.type.itemPath(this.uuid), 'Laden fehlgeschlagen.')
        this.value = this.item[this.type.field]
      } else if (this.parentPath) {
        this.parent = await this.store.load(this.parentPath, 'Laden fehlgeschlagen.')
      }
    })
  },
  methods: {
    save() {
      return this.runAction(async () => {
        const data = { [this.type.field]: this.value.trim() }
        const item = this.editing
          ? await this.store.send(
              this.type.itemPath(this.uuid),
              'PATCH',
              data,
              'Speichern fehlgeschlagen.',
            )
          : await this.store.send(
              this.type.createPath(this.uuid),
              'POST',
              data,
              'Erstellen fehlgeschlagen.',
            )
        this.$router.push(this.type.target(item))
      })
    },
    destroy() {
      return this.runAction(async () => {
        await this.store.remove(this.type.itemPath(this.uuid), 'Löschen fehlgeschlagen.')
        this.$router.push(this.type.afterDelete(this.item))
      })
    },
  },
}
</script>
