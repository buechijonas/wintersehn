<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-8 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="w-full">
      <h2 class="text-xl my-4">Nutzer</h2>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>Benutzername</th>
              <th>E-Mail</th>
              <th>Rolle</th>
              <th>Verifiziert</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in rbacStore.users" :key="user.id">
              <td class="flex items-center gap-2">
                <img class="size-6" :src="avatarSrc(user.avatar)" alt="" />
                {{ user.username }}
              </td>
              <td class="text-wntrs-muted">{{ user.email }}</td>
              <td>
                <select
                  class="select select-sm"
                  :value="user.role ?? ''"
                  :disabled="!authStore.user?.can_change_role"
                  @change="onUserRoleChange(user, $event)"
                >
                  <option value="">Keine Rolle</option>
                  <option v-for="role in rbacStore.roles" :key="role.id" :value="role.id">
                    {{ role.name }}
                  </option>
                </select>
              </td>
              <td class="text-center">
                <input
                  type="checkbox"
                  class="checkbox"
                  :checked="user.verified"
                  :disabled="!authStore.user?.can_change_role"
                  @change="onUserVerifiedChange(user, $event)"
                />
              </td>
              <td class="text-right">
                <DeleteButton
                  v-if="authStore.user?.can_change_role && user.id !== authStore.user.id"
                  title="Löschen"
                  @click="onDeleteUser(user)"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <BaseFooter />
</template>

<script>
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

export default {
  name: 'AdminUsersView',
  components: { BaseBreadcrumbs, BaseFooter, DeleteButton },
  mixins: [asyncActionMixin],
  data() {
    return {
      breadcrumbs: [{ label: 'Admin', to: '/admin' }, { label: 'Nutzer' }],
      icons,
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    rbacStore() {
      return useRbacStore()
    },
  },
  mounted() {
    return this.runAction(() => this.rbacStore.fetchAll())
  },
  methods: {
    avatarSrc(avatar) {
      return profiles[avatar] ?? icons.user
    },
    onUserRoleChange(user, event) {
      const value = event.target.value
      return this.runAction(() => this.rbacStore.setUserRole(user.id, value ? Number(value) : null))
    },
    onUserVerifiedChange(user, event) {
      return this.runAction(() => this.rbacStore.setUserVerified(user.id, event.target.checked))
    },
    onDeleteUser(user) {
      if (!confirm(`Möchtest du den Nutzer "${user.username}" wirklich löschen?`)) return
      return this.runAction(() => this.rbacStore.deleteUser(user.id))
    },
  },
}
</script>
