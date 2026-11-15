<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 flex-1">
    <div class="mx-auto w-full max-w-200">
      <h2 class="text-xl my-4">{{ label }}</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <form v-if="contentData && canEdit" class="flex flex-col gap-4" @submit.prevent="save">
        <p class="text-sm text-wntrs-slate">
          Mit <code>[[address]]</code> auf einer eigenen Zeile fügst du den Adressblock ein.
        </p>
        <MarkdownEditor v-model="body" preview-url="/api/content/markdown/preview/" />
        <BaseButton
          type="submit"
          variant="primary"
          class="self-end"
          :disabled="saving || body === contentData.body"
        >
          <AppIcon name="disk" />
          Speichern
        </BaseButton>
      </form>
      <BaseCard v-else-if="contentData" class="p-6">
        <MarkdownContent :html="html" placeholder="Noch kein Text." />
      </BaseCard>
    </div>
  </div>
</template>

<script>
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import AppIcon from '@core/components/common/AppIcon.vue'
import MarkdownContent from '@core/components/common/MarkdownContent.vue'
import MarkdownEditor from '@core/components/common/MarkdownEditor.vue'
import { useAuthStore } from '@core/stores/auth.js'
import { useContentStore } from '@core/stores/content.js'
import asyncActionMixin from '@core/mixins/asyncActionMixin.js'

export default {
  name: 'AdminLegalView',
  components: {
    BaseBreadcrumbs,
    BaseCard,
    BaseButton,
    AppIcon,
    MarkdownContent,
    MarkdownEditor,
  },
  mixins: [asyncActionMixin],
  props: {
    contentKey: { type: String, required: true },
    label: { type: String, required: true },
  },
  data() {
    return {
      body: '',
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    contentStore() {
      return useContentStore()
    },
    contentData() {
      return this.contentStore.items[this.contentKey]?.data ?? null
    },
    html() {
      return this.contentStore.items[this.contentKey]?.html ?? ''
    },
    canEdit() {
      return !!this.authStore.user?.can_edit_content
    },
    breadcrumbs() {
      return [{ label: 'Admin', to: '/admin' }, { label: this.label }]
    },
  },
  watch: {
    contentKey: {
      immediate: true,
      handler() {
        this.contentStore.fetchContent(this.contentKey)
      },
    },
    'contentData.body': {
      immediate: true,
      handler(body) {
        this.body = body ?? ''
      },
    },
  },
  methods: {
    save() {
      return this.runAction(() =>
        this.contentStore.saveContent(this.contentKey, { ...this.contentData, body: this.body }),
      )
    },
  },
}
</script>
