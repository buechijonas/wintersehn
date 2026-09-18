<template>
  <BasePage active-navigation="admin">
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
                    :disabled="!authStore.user?.can_manage_roles"
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
                    :disabled="!authStore.user?.can_manage_roles"
                    @change="onUserVerifiedChange(user, $event)"
                  />
                </td>
                <td class="text-right">
                  <DeleteButton
                    v-if="authStore.user?.can_manage_roles && user.id !== authStore.user.id"
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
  </BasePage>
</template>

<script>
import BasePage from '@/components/layout/BasePage.vue'
import BaseBreadcrumbs from '@/components/common/BaseBreadcrumbs.vue'
import BaseFooter from '@/components/common/BaseFooter.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'

export default {
  name: 'AdminUsersView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter, DeleteButton },
  data() {
    return {
      breadcrumbs: [{ label: 'Admin', to: '/admin' }, { label: 'Nutzer' }],
      icons,
      error: '',
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
  async mounted() {
    try {
      await this.rbacStore.fetchAll()
    } catch (e) {
      this.error = e.message
    }
  },
  methods: {
    avatarSrc(avatar) {
      return profiles[avatar] ?? icons.user
    },
    async onUserRoleChange(user, event) {
      this.error = ''
      const value = event.target.value
      try {
        await this.rbacStore.setUserRole(user.id, value ? Number(value) : null)
      } catch (e) {
        this.error = e.message
      }
    },
    async onUserVerifiedChange(user, event) {
      this.error = ''
      try {
        await this.rbacStore.setUserVerified(user.id, event.target.checked)
      } catch (e) {
        this.error = e.message
      }
    },
    async onDeleteUser(user) {
      this.error = ''
      if (!confirm(`Möchtest du den Nutzer "${user.username}" wirklich löschen?`)) return
      try {
        await this.rbacStore.deleteUser(user.id)
      } catch (e) {
        this.error = e.message
      }
    },
  },
}
</script>
