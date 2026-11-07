<template>
  <AtlasPage :breadcrumbs="breadcrumbs" :loading="!draft" :error="error">
    <template v-if="exam" #actions>
      <DeleteAction :message="`${exam.name} löschen?`" @confirm="destroy" />
    </template>
    <div class="mx-auto flex w-full max-w-160 flex-col gap-4">
      <h2 class="text-xl font-light">{{ editing ? 'Prüfung bearbeiten' : 'Neue Prüfung' }}</h2>
      <BaseCard tag="form" class="flex flex-col gap-6 rounded-box p-6" @submit.prevent="save">
        <label class="flex flex-col gap-2">
          <span class="text-sm text-wntrs-muted">Name</span>
          <input v-model="draft.name" type="text" placeholder="z.B. Algebra" :class="inputClass" />
        </label>
        <div class="grid grid-cols-2 gap-4">
          <label class="flex flex-col gap-2">
            <span class="text-sm text-wntrs-muted">Gewichtung</span>
            <input
              v-model="draft.weight"
              type="number"
              min="0.01"
              step="0.01"
              :class="inputClass"
            />
          </label>
          <label v-if="!draft.parts.length" class="flex flex-col gap-2">
            <span class="text-sm text-wntrs-muted">Note</span>
            <input
              v-model="draft.grade"
              type="number"
              min="1"
              max="6"
              step="0.01"
              placeholder="1 bis 6"
              :class="inputClass"
            />
          </label>
        </div>

        <section class="flex flex-col gap-3">
          <div class="flex items-center justify-between gap-4">
            <span class="text-sm text-wntrs-muted">Teilnoten</span>
            <BaseButton size="sm" @click="addPart">
              <AppIcon name="plus" />
              Teilnote
            </BaseButton>
          </div>
          <p v-if="draft.parts.length" class="text-xs text-wntrs-muted">
            Die Note der Prüfung ist der gewichtete Durchschnitt der Teilnoten.
          </p>
          <div
            v-if="draft.parts.length"
            class="grid grid-cols-[1fr_5rem_5rem_2.5rem] gap-2 text-xs text-wntrs-muted"
          >
            <span>Name</span>
            <span>Gewichtung</span>
            <span>Note</span>
          </div>
          <div
            v-for="(part, index) in draft.parts"
            :key="index"
            class="grid grid-cols-[1fr_5rem_5rem_2.5rem] items-center gap-2"
          >
            <input
              v-model="part.name"
              type="text"
              placeholder="Name"
              aria-label="Name der Teilnote"
              :class="inputClass"
            />
            <input
              v-model="part.weight"
              type="number"
              min="0.01"
              step="0.01"
              aria-label="Gewichtung"
              :class="inputClass"
            />
            <input
              v-model="part.grade"
              type="number"
              min="1"
              max="6"
              step="0.01"
              placeholder="Note"
              aria-label="Note"
              :class="inputClass"
            />
            <BaseButton
              shape="square"
              title="Teilnote entfernen"
              @click="draft.parts.splice(index, 1)"
            >
              <AppIcon name="cross" alt="Teilnote entfernen" />
            </BaseButton>
          </div>
        </section>

        <div class="grid grid-cols-2 gap-2 sm:flex sm:justify-end">
          <CancelButton :to="`/subjects/${subjectUuid}`" />
          <BaseButton type="submit" variant="primary" :disabled="saving || !draft.name.trim()">
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
import { subjectBreadcrumbs } from '@/lib/breadcrumbs.js'
import { useAtlasStore } from '@/stores/atlas.js'

export default {
  name: 'ExamFormView',
  components: { AppIcon, AtlasPage, BaseButton, BaseCard, CancelButton, DeleteAction },
  mixins: [asyncActionMixin],
  data() {
    return {
      exam: null,
      subject: null,
      draft: null,
      inputClass: 'input w-full border-wntrs-border focus:border-primary focus:outline-none',
    }
  },
  computed: {
    store() {
      return useAtlasStore()
    },
    editing() {
      return this.$route.meta.mode === 'edit'
    },
    subjectUuid() {
      return this.editing ? this.exam?.subject.uuid : this.$route.params.uuid
    },
    breadcrumbs() {
      const label = this.editing ? (this.exam?.name ?? '') : 'Neue Prüfung'
      return [...subjectBreadcrumbs(this.editing ? this.exam?.subject : this.subject), { label }]
    },
  },
  mounted() {
    this.runAction(async () => {
      if (!this.editing) {
        this.subject = await this.store.load(
          `/subjects/${this.$route.params.uuid}/`,
          'Fach konnte nicht geladen werden.',
        )
        this.draft = { name: '', weight: '1', grade: '', parts: [] }
        return
      }
      this.exam = await this.store.load(
        `/exams/${this.$route.params.uuid}/`,
        'Prüfung konnte nicht geladen werden.',
      )
      const { name, weight, grade, parts } = this.exam
      this.draft = { name, weight, grade: grade ?? '', parts: parts.map((part) => ({ ...part })) }
    })
  },
  methods: {
    addPart() {
      this.draft.parts.push({ name: '', weight: '1', grade: '' })
    },
    save() {
      return this.runAction(async () => {
        const { name, weight, grade, parts } = this.draft
        const data = {
          name: name.trim(),
          weight,
          grade: parts.length || grade === '' ? null : grade,
          parts,
        }
        if (this.editing) {
          await this.store.send(
            `/exams/${this.exam.uuid}/`,
            'PATCH',
            data,
            'Speichern fehlgeschlagen.',
          )
        } else {
          await this.store.send(
            `/subjects/${this.subjectUuid}/exams/`,
            'POST',
            data,
            'Erstellen fehlgeschlagen.',
          )
        }
        this.$router.push(`/subjects/${this.subjectUuid}`)
      })
    },
    destroy() {
      return this.runAction(async () => {
        await this.store.remove(`/exams/${this.exam.uuid}/`, 'Löschen fehlgeschlagen.')
        this.$router.push(`/subjects/${this.subjectUuid}`)
      })
    },
  },
}
</script>
