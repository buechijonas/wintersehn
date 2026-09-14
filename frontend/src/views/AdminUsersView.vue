<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-8 max-h-[calc(100dvh-101px)] overflow-y-auto">
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
                  <button
                    v-if="authStore.user?.can_manage_roles && user.id !== authStore.user.id"
                    type="button"
                    class="btn btn-ghost btn-square btn-xs"
                    title="Löschen"
                    @click="onDeleteUser(user)"
                  >
                    <img :src="icons.trash" alt="Löschen" class="size-4 trash-icon" />
                  </button>
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
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'

export default {
  name: 'AdminUsersView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter },
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

<style scoped>
.trash-icon {
  filter: brightness(0) saturate(100%) invert(54%) sepia(50%) saturate(3825%) hue-rotate(318deg)
    brightness(110%) contrast(101%);
}
</style>
