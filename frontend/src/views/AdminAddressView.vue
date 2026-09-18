<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">Adresse</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <SortableList
          :items="lines"
          :disabled="!canEdit"
          class="flex flex-col gap-4"
          @reorder="reorderLines"
        >
          <template #default="{ item: line, index: lineIndex }">
            <BaseCard class="p-6">
              <div class="flex items-center gap-2">
                <input
                  type="text"
                  class="input input-sm flex-1"
                  :value="line"
                  :disabled="!canEdit"
                  @change="updateLine(lineIndex, $event.target.value)"
                />
                <DeleteButton v-if="canEdit" :disabled="saving" @click="removeLine(lineIndex)" />
              </div>
            </BaseCard>
          </template>
        </SortableList>

        <div v-if="canEdit" class="flex gap-4 mt-6">
          <input
            v-model="newLine"
            type="text"
            placeholder="Neue Zeile"
            class="input flex-1"
            @keyup.enter="addLine"
          />
          <BaseButton variant="primary" @click="addLine">Zeile hinzufügen</BaseButton>
        </div>
      </div>
    </div>

    <BaseFooter />
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import SortableList from '@/components/common/SortableList.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useContentStore } from '@/stores/content.js'

export default {
  name: 'AdminAddressView',
  components: {
    BasePage,
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    DeleteButton,
    BaseFooter,
    SortableList,
  },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Adresse' },
      ],
      error: '',
      saving: false,
      newLine: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    lines() {
      return this.contentStore.items.address?.data?.lines ?? []
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
  },
  mounted() {
    this.contentStore.fetchContent('address')
  },
  methods: {
    async persist(lines) {
      this.error = ''
      this.saving = true
      try {
        await this.contentStore.saveContent('address', { lines })
      } catch (e) {
        this.error = e.message
      } finally {
        this.saving = false
      }
    },
    addLine() {
      const line = this.newLine.trim()
      if (!line) return
      this.newLine = ''
      this.persist([...this.lines, line])
    },
    updateLine(lineIndex, value) {
      const trimmed = value.trim()
      if (trimmed === this.lines[lineIndex]) return
      this.persist(this.lines.map((l, i) => (i === lineIndex ? trimmed : l)))
    },
    removeLine(lineIndex) {
      this.persist(this.lines.filter((_, i) => i !== lineIndex))
    },
    reorderLines(lines) {
      this.persist(lines)
    },
  },
}
</script>
