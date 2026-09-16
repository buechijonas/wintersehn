<template>
  <div>
    <label v-if="label" class="label">{{ label }}</label>
    <div class="flex items-center gap-4">
      <BaseCard class="size-16 shrink-0 flex items-center justify-center p-2">
        <img
          v-if="previewIcon"
          class="size-11"
          :class="{ 'opacity-40': !modelValue }"
          :src="icons[previewIcon]"
          alt=""
        />
      </BaseCard>

      <BaseButton
        type="button"
        class="flex-1 min-w-0 justify-start gap-2"
        @click="openDialog"
      >
        <img v-if="modelValue" class="size-5 shrink-0" :src="icons[modelValue]" alt="" />
        <span class="truncate">{{ currentLabel }}</span>
      </BaseButton>
    </div>

    <BaseDialog
      ref="dialog"
      title="Icon wählen"
      box-class="w-full h-full max-w-full max-h-full rounded-none sm:rounded-box sm:h-[600px] sm:max-h-[85vh] sm:w-11/12 sm:max-w-2xl"
    >
      <div class="flex flex-col h-full min-h-0">
        <input
          v-model="search"
          type="text"
          placeholder="Icon suchen…"
          class="input w-full mb-4 shrink-0"
          autofocus
        />
        <div v-if="categoryNames.length" class="flex items-center gap-1 mb-4 shrink-0">
          <BaseButton
            type="button"
            variant="ghost"
            shape="circle"
            size="xs"
            class="shrink-0"
            @click="scrollCategories(-1)"
          >
            ‹
          </BaseButton>
          <div
            ref="categoryScroll"
            class="flex flex-nowrap gap-2 overflow-x-auto pb-1"
            @wheel="onCategoryWheel"
          >
            <BaseButton
              type="button"
              size="xs"
              class="shrink-0"
              :variant="activeCategory ? 'ghost' : 'primary'"
              @click="selectCategory('')"
            >
              Alle
            </BaseButton>
            <BaseButton
              v-for="name in visibleCategoryNames"
              :key="name"
              type="button"
              size="xs"
              class="shrink-0"
              :variant="activeCategory === name ? 'primary' : 'ghost'"
              @click="selectCategory(name)"
            >
              {{ humanize(name) }}
            </BaseButton>
          </div>
          <BaseButton
            type="button"
            variant="ghost"
            shape="circle"
            size="xs"
            class="shrink-0"
            @click="scrollCategories(1)"
          >
            ›
          </BaseButton>
        </div>

        <div class="flex-1 min-h-0 overflow-y-auto">
          <div class="grid grid-cols-6 sm:grid-cols-8 gap-2">
            <button
              v-if="allowEmpty && currentPage === 1"
              type="button"
              :title="emptyLabel"
              class="flex items-center justify-center p-2 rounded hover:bg-base-200"
              :class="{ 'bg-base-200': !modelValue }"
              @click="choose('')"
            >
              <img class="size-8" :src="icons[emptyIcon]" alt="" />
            </button>
            <button
              v-for="key in pagedKeys"
              :key="key"
              type="button"
              :title="iconLabel(key)"
              class="flex items-center justify-center p-2 rounded hover:bg-base-200"
              :class="{ 'bg-base-200': modelValue === key }"
              @click="choose(key)"
            >
              <img class="size-8" :src="icons[key]" :alt="iconLabel(key)" />
            </button>
          </div>
          <p
            v-if="!filteredKeys.length"
            class="text-wntrs-muted text-sm text-center py-4"
          >
            Keine Icons gefunden.
          </p>
        </div>

        <div v-if="totalPages > 1" class="join mt-4 flex justify-center shrink-0">
          <button
            type="button"
            class="join-item btn btn-sm"
            :disabled="currentPage === 1"
            @click="currentPage--"
          >
            «
          </button>
          <button
            v-if="pageNumbers[0] > 1"
            type="button"
            class="join-item btn btn-sm"
            @click="currentPage = 1"
          >
            1
          </button>
          <button v-if="pageNumbers[0] > 2" type="button" class="join-item btn btn-sm btn-disabled">
            …
          </button>
          <button
            v-for="page in pageNumbers"
            :key="page"
            type="button"
            class="join-item btn btn-sm"
            :class="{ 'btn-active': page === currentPage }"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
          <button
            v-if="pageNumbers[pageNumbers.length - 1] < totalPages - 1"
            type="button"
            class="join-item btn btn-sm btn-disabled"
          >
            …
          </button>
          <button
            v-if="pageNumbers[pageNumbers.length - 1] < totalPages"
            type="button"
            class="join-item btn btn-sm"
            @click="currentPage = totalPages"
          >
            {{ totalPages }}
          </button>
          <button
            type="button"
            class="join-item btn btn-sm"
            :disabled="currentPage === totalPages"
            @click="currentPage++"
          >
            »
          </button>
        </div>
      </div>
    </BaseDialog>
  </div>
</template>

<script>
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'

const PAGE_SIZE = 48

export default {
  name: 'IconPickerField',
  components: { BaseCard, BaseButton, BaseDialog },
  props: {
    modelValue: { type: String, default: '' },
    icons: { type: Object, required: true },
    label: { type: String, default: 'Icon' },
    allowEmpty: { type: Boolean, default: false },
    emptyIcon: { type: String, default: '' },
    emptyLabel: { type: String, default: 'Kein Icon' },
    categories: { type: Object, default: () => ({}) },
  },
  emits: ['update:modelValue'],
  data() {
    return { search: '', activeCategory: '', currentPage: 1 }
  },
  watch: {
    search() {
      this.currentPage = 1
    },
  },
  computed: {
    categoryNames() {
      return Object.keys(this.categories).sort((a, b) => a.localeCompare(b, 'de'))
    },
    // Built once per icons/categories change (not per keystroke): each icon's
    // searchable text (key + label + folder name) is pre-joined and lowercased
    // so filtering is a single substring check instead of re-deriving it every time.
    iconIndex() {
      return Object.keys(this.icons)
        .sort((a, b) => a.localeCompare(b, 'de'))
        .map((key) => {
          const folder = key.includes('/') ? key.split('/')[0] : ''
          const searchText = [
            key.replace(/[-_/]/g, ' '),
            this.iconLabel(key),
            folder,
            folder ? this.humanize(folder) : '',
          ]
            .join(' ')
            .toLowerCase()
          return { key, folder, searchText }
        })
    },
    categorySearchText() {
      const map = {}
      for (const entry of this.iconIndex) {
        if (!entry.folder) continue
        map[entry.folder] = map[entry.folder] ? `${map[entry.folder]} ${entry.searchText}` : entry.searchText
      }
      return map
    },
    categoryEntries() {
      if (!this.activeCategory) return this.iconIndex
      const allowed = new Set(this.categories[this.activeCategory] ?? [])
      return this.iconIndex.filter((entry) => allowed.has(entry.key))
    },
    filteredKeys() {
      const query = this.search.trim().toLowerCase()
      const entries = query
        ? this.categoryEntries.filter((entry) => entry.searchText.includes(query))
        : this.categoryEntries
      return entries.map((entry) => entry.key)
    },
    visibleCategoryNames() {
      const query = this.search.trim().toLowerCase()
      if (!query) return this.categoryNames
      return this.categoryNames.filter(
        (name) => name === this.activeCategory || (this.categorySearchText[name] ?? '').includes(query),
      )
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.filteredKeys.length / PAGE_SIZE))
    },
    pagedKeys() {
      const start = (this.currentPage - 1) * PAGE_SIZE
      return this.filteredKeys.slice(start, start + PAGE_SIZE)
    },
    pageNumbers() {
      const delta = 2
      const from = Math.max(1, this.currentPage - delta)
      const to = Math.min(this.totalPages, this.currentPage + delta)
      const pages = []
      for (let page = from; page <= to; page++) pages.push(page)
      return pages
    },
    previewIcon() {
      return this.modelValue || this.emptyIcon
    },
    currentLabel() {
      if (this.modelValue) return this.iconLabel(this.modelValue)
      return this.allowEmpty ? this.emptyLabel : 'Icon wählen'
    },
  },
  methods: {
    humanize(name) {
      return name
        .split(/[-_]/)
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
    },
    iconLabel(key) {
      if (!key) return 'Icon wählen'
      const name = key.includes('/') ? key.split('/').pop() : key
      return this.humanize(name)
    },
    onCategoryWheel(event) {
      const el = event.currentTarget
      if (el.scrollWidth <= el.clientWidth) return
      el.scrollLeft += event.deltaY
      event.preventDefault()
    },
    scrollCategories(direction) {
      this.$refs.categoryScroll?.scrollBy({ left: direction * 160, behavior: 'smooth' })
    },
    selectCategory(name) {
      this.activeCategory = this.activeCategory === name ? '' : name
      this.currentPage = 1
    },
    openDialog() {
      this.search = ''
      this.activeCategory = ''
      this.currentPage = 1
      this.$refs.dialog?.open()
    },
    choose(key) {
      this.$emit('update:modelValue', key)
      this.$refs.dialog?.close()
    },
  },
}
</script>
