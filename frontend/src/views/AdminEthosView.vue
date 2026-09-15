<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">Ethos</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <div class="flex flex-col gap-4">
          <BaseCard v-for="(section, sectionIndex) in sections" :key="sectionIndex" class="p-6">
            <div class="flex items-center justify-between gap-4 mb-4">
              <input
                type="text"
                class="input input-sm w-full max-w-60"
                :value="section.title"
                :disabled="!canEdit"
                @change="renameSection(sectionIndex, $event)"
              />
              <DeleteButton
                v-if="canEdit"
                class="shrink-0"
                :disabled="saving"
                @click="askRemoveSection(sectionIndex)"
              >
                Abschnitt löschen
              </DeleteButton>
            </div>

            <div class="flex flex-wrap gap-2">
              <div
                v-for="(item, itemIndex) in section.items"
                :key="itemIndex"
                class="relative shrink-0"
              >
                <BaseCard class="size-40 flex items-center justify-center p-4">
                  <div class="flex flex-col items-center text-center gap-4">
                    <img class="size-16" :src="flatIcons[item.icon]" :alt="item.label" />
                    <p class="text-wntrs-slate text-sm">{{ item.label }}</p>
                  </div>
                </BaseCard>
                <DeleteButton
                  v-if="canEdit"
                  class="absolute top-2 right-2"
                  :disabled="saving"
                  @click="askRemoveItem(sectionIndex, itemIndex)"
                />
              </div>

              <BaseCard
                v-if="canEdit"
                tag="router-link"
                :to="`/admin/ethos/${sectionIndex}/create`"
                class="size-40 shrink-0 flex items-center justify-center p-4 hover:bg-base-200"
              >
                <span class="text-4xl text-wntrs-muted leading-none">+</span>
              </BaseCard>
            </div>
          </BaseCard>
        </div>

        <div v-if="canEdit" class="flex gap-4 mt-6">
          <input
            v-model="newSectionTitle"
            type="text"
            placeholder="Neuer Abschnitt"
            class="input flex-1"
            @keyup.enter="addSection"
          />
          <BaseButton variant="primary" @click="addSection">Abschnitt hinzufügen</BaseButton>
        </div>
      </div>
    </div>

    <ConfirmDialog
      ref="confirmDialog"
      :title="dialogTitle"
      :message="dialogMessage"
      @confirm="onConfirmDelete"
    />

    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import { flats } from '@/assets/images.js'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminEthosView',
  components: {
    BasePage,
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    DeleteButton,
    ConfirmDialog,
    BaseFooter,
  },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Ethos' },
      ],
      error: '',
      saving: false,
      newSectionTitle: '',
      dialogTitle: '',
      dialogMessage: '',
      pendingAction: null,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    flatIcons() {
      return flats
    },
    sections() {
      return this.contentStore.items.ethos?.data ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
  },
  mounted() {
    this.contentStore.fetchContent('ethos')
  },
  methods: {
    async persist(data) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('ethos', data)
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    addSection() {
      const title = this.newSectionTitle.trim()
      if (!title) return
      this.newSectionTitle = ''
      this.persist([...this.sections, { title, items: [] }])
    },
    renameSection(sectionIndex, event) {
      const title = event.target.value.trim()
      event.target.value = title
      if (!title || title === this.sections[sectionIndex].title) return
      this.persist(
        this.sections.map((section, i) => (i === sectionIndex ? { ...section, title } : section)),
      )
    },
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    askRemoveSection(sectionIndex) {
      const { title } = this.sections[sectionIndex]
      this.confirmRemoval('Abschnitt löschen', `Möchtest du "${title}" wirklich löschen?`, () =>
        this.persist(this.sections.filter((_, i) => i !== sectionIndex)),
      )
    },
    askRemoveItem(sectionIndex, itemIndex) {
      const { label } = this.sections[sectionIndex].items[itemIndex]
      this.confirmRemoval('Eintrag löschen', `Möchtest du "${label}" wirklich löschen?`, () =>
        this.persist(
          this.sections.map((section, i) =>
            i === sectionIndex
              ? { ...section, items: section.items.filter((_, j) => j !== itemIndex) }
              : section,
          ),
        ),
      )
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
</script>
