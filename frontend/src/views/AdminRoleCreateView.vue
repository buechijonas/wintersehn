<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="mx-auto w-full max-w-150">
      <h2 class="text-xl font-light my-4">Neue Rolle</h2>

      <BaseCard class="p-6">
        <form class="fieldset" @submit.prevent="save">
          <label class="label" for="role-name">Name</label>
          <input id="role-name" v-model="name" type="text" class="input w-full" required />

          <p v-if="error" class="text-error text-sm mt-3">{{ error }}</p>

          <div class="flex justify-end gap-4 mt-4">
            <CancelButton to="/admin/roles" />
            <BaseButton type="submit" variant="primary" :disabled="saving">
              <AppIcon name="disk" />
              Speichern
            </BaseButton>
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
import AppIcon from '@/components/common/AppIcon.vue'
import CancelButton from '@/components/common/CancelButton.vue'
import { useRbacStore } from '@/stores/rbac.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminRoleCreateView',
  components: { BaseBreadcrumbs, BaseCard, BaseFooter, BaseButton, AppIcon, CancelButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      name: '',
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Rollen & Rechte', to: '/admin/roles' },
        { label: 'Neue Rolle' },
      ],
    }
  },
  computed: {
    rbacStore() {
      return useRbacStore()
    },
  },
  methods: {
    async save() {
      this.error = ''
      const name = this.name.trim()
      if (!name) {
        this.error = 'Name ist erforderlich.'
        return
      }
      await this.runAction(() => this.rbacStore.createRole(name))
      if (!this.error) this.$router.push('/admin/roles')
    },
  },
}
</script>
