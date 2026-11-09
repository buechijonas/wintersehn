<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="mx-auto flex w-full max-w-200 flex-1 flex-col gap-12 px-6 pt-4 pb-16">
    <div v-if="loading" class="flex flex-col gap-4">
      <div v-for="row in 4" :key="row" class="skeleton h-32 w-full"></div>
    </div>

    <section v-for="section in sections" :key="section.title" class="flex flex-col gap-4">
      <template v-if="section.kind === 'intro'">
        <h1 class="font-display text-5xl font-bold tracking-tighter text-wntrs-title">
          {{ section.title }}
        </h1>
        <p class="max-w-150 text-lg text-wntrs-slate">{{ section.text }}</p>
        <BaseButton
          v-if="section.link"
          class="self-start"
          :href="section.link.url"
          target="_blank"
          rel="noopener noreferrer"
        >
          <AppIcon name="share-square" />
          {{ section.link.label }}
        </BaseButton>
      </template>

      <template v-else-if="section.kind === 'group'">
        <div class="divider mt-4 mb-0 font-display text-2xl font-bold text-wntrs-title">
          {{ section.title }}
        </div>
        <p class="text-center text-wntrs-muted">{{ section.text }}</p>
        <div class="flex flex-wrap justify-center gap-2">
          <a
            v-for="site in section.sites"
            :key="site.url"
            :href="site.url"
            target="_blank"
            rel="noopener noreferrer"
            class="badge gap-1.5 badge-soft"
            :class="site.public ? 'badge-success' : 'badge-error'"
          >
            <AppIcon :name="site.public ? 'unlock' : 'lock'" />
            {{ site.label }} · {{ site.public ? 'Öffentlich' : 'Privat' }}
          </a>
        </div>
      </template>

      <template v-else>
        <h2 class="text-xl">{{ section.title }}</h2>
        <p v-if="section.text" class="text-wntrs-muted">{{ section.text }}</p>
      </template>

      <FlowDiagram
        v-if="section.kind === 'diagram'"
        :title="section.title"
        :columns="section.columns"
        :edges="section.edges"
      />

      <div v-else-if="section.kind === 'principles'" class="grid gap-4 sm:grid-cols-3">
        <BaseCard v-for="item in section.items" :key="item.title" class="flex flex-col gap-1 p-4">
          <span class="font-medium">{{ item.title }}</span>
          <span class="text-sm text-wntrs-muted">{{ item.text }}</span>
        </BaseCard>
      </div>

      <div v-else-if="section.kind === 'stack'" class="grid gap-4 sm:grid-cols-2">
        <BaseCard
          v-for="group in section.groups"
          :key="group.title"
          class="flex flex-col gap-3 p-4"
        >
          <span class="text-xs font-medium tracking-wide text-primary">{{ group.title }}</span>
          <div v-for="item in group.items" :key="item.name" class="flex flex-col">
            <span class="text-sm font-medium">{{ item.name }}</span>
            <span class="text-xs text-wntrs-muted">{{ item.note }}</span>
          </div>
        </BaseCard>
      </div>

      <BaseCard v-else-if="section.kind === 'formula'" class="flex flex-col gap-4 p-4">
        <div
          v-for="formula in section.formulas"
          :key="formula.label"
          class="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:gap-6"
        >
          <span class="w-28 shrink-0 text-xs text-wntrs-muted">{{ formula.label }}</span>
          <span class="font-serif text-xl italic">{{ formula.expression }}</span>
        </div>
        <p v-if="section.note" class="border-t border-wntrs-border pt-3 text-sm text-wntrs-muted">
          {{ section.note }}
        </p>
      </BaseCard>

      <template v-if="section.kind === 'formula'">
        <BaseCard v-if="section.graphic" class="p-4">
          <FormulaGraphic :name="section.graphic" :label="section.title" />
        </BaseCard>
        <CodeSnippet
          v-if="section.code"
          :file="section.file"
          :url="section.url"
          :code="section.code"
        />
      </template>

      <div v-else-if="section.kind === 'open'" class="grid gap-4 sm:grid-cols-2">
        <BaseCard
          v-for="item in section.items"
          :key="item.title"
          class="flex flex-col gap-1 border-dashed! p-4"
        >
          <span class="flex items-center gap-2 font-medium">
            <AppIcon name="triangle-warning" class="text-warning" />
            {{ item.title }}
          </span>
          <span class="text-sm text-wntrs-muted">{{ item.text }}</span>
        </BaseCard>
      </div>

      <CodeSnippet
        v-else-if="section.kind === 'code'"
        :file="section.file"
        :url="section.url"
        :code="section.code"
      />

      <ol v-else-if="section.kind === 'flow'" class="flex flex-col gap-3">
        <li v-for="(step, index) in section.steps" :key="step" class="flex gap-3">
          <span
            class="flex size-7 shrink-0 items-center justify-center rounded-full bg-primary text-sm text-primary-content"
          >
            {{ index + 1 }}
          </span>
          <span class="pt-0.5">{{ step }}</span>
        </li>
      </ol>

      <template v-else-if="section.kind === 'problem'">
        <div class="grid gap-4 sm:grid-cols-2">
          <BaseCard class="flex flex-col gap-1 p-4">
            <span class="text-xs font-medium tracking-wide text-error">Problem</span>
            <span class="text-sm">{{ section.problem }}</span>
          </BaseCard>
          <BaseCard class="flex flex-col gap-1 p-4">
            <span class="text-xs font-medium tracking-wide text-success">Lösung</span>
            <span class="text-sm">{{ section.solution }}</span>
          </BaseCard>
        </div>
        <CodeSnippet :file="section.file" :url="section.url" :code="section.code" />
      </template>
    </section>
  </div>
</template>

<script>
import AppIcon from '@core/components/common/AppIcon.vue'
import BaseBreadcrumbs from '@core/components/common/BaseBreadcrumbs.vue'
import BaseButton from '@core/components/common/BaseButton.vue'
import BaseCard from '@core/components/common/BaseCard.vue'
import { useContentStore } from '@core/stores/content.js'
import CodeSnippet from '@/components/common/CodeSnippet.vue'
import FlowDiagram from '@/components/common/FlowDiagram.vue'
import FormulaGraphic from '@/components/common/FormulaGraphic.vue'

export default {
  name: 'EngineeringView',
  components: {
    AppIcon,
    BaseBreadcrumbs,
    BaseButton,
    BaseCard,
    CodeSnippet,
    FlowDiagram,
    FormulaGraphic,
  },
  data() {
    return {
      breadcrumbs: [{ label: 'Engineering', to: '/' }],
    }
  },
  computed: {
    contentStore() {
      return useContentStore()
    },
    loading() {
      return !this.contentStore.items.engineering
    },
    sections() {
      return this.contentStore.items.engineering?.data ?? []
    },
  },
  mounted() {
    this.contentStore.fetchContent('engineering')
  },
}
</script>
