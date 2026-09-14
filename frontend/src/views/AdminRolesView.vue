<template>
  <BasePage active-navigation="admin">
    <BaseBreadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-6 max-h-[calc(100dvh-101px)] overflow-y-auto">
      <div class="mx-auto w-full max-w-200">
        <h2 class="text-xl my-4">Rollen &amp; Rechte</h2>

        <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

        <div class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>Berechtigung</th>
                <th v-for="role in rbacStore.roles" :key="role.id" class="min-w-40">
                  <div class="flex flex-col gap-1">
                    <input
                      type="text"
                      class="input input-sm w-full"
                      :value="role.name"
                      :disabled="!authStore.user?.can_manage_roles"
                      @change="renameRole(role, $event)"
                    />
                    <button
                      v-if="authStore.user?.can_manage_roles"
                      type="button"
                      class="btn btn-ghost btn-xs"
                      @click="removeRole(role)"
                    >
                      Löschen
                    </button>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="permission in rbacStore.permissions" :key="permission.codename">
                <td class="text-wntrs-slate">{{ permission.name }}</td>
                <td v-for="role in rbacStore.roles" :key="role.id" class="text-center">
                  <input
                    type="checkbox"
                    class="checkbox"
                    :checked="hasPermission(role, permission.codename)"
                    :disabled="!authStore.user?.can_manage_permissions"
                    @change="togglePermission(role, permission.codename)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="authStore.user?.can_manage_roles" class="flex gap-4 mt-6">
          <input
            v-model="newRoleName"
            type="text"
            placeholder="Neue Rolle"
            class="input flex-1"
            @keyup.enter="addRole"
          />
          <button type="button" class="btn btn-primary shadow-none" @click="addRole">
            Rolle hinzufügen
          </button>
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
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'

export default {
  name: 'AdminRolesView',
  components: { BasePage, BaseBreadcrumbs, BaseFooter },
  data() {
    return {
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Rollen & Rechte' },
      ],
      error: '',
      newRoleName: '',
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
    hasPermission(role, codename) {
      return role.permissions.includes(codename)
    },
    async togglePermission(role, codename) {
      this.error = ''
      const next = this.hasPermission(role, codename)
        ? role.permissions.filter((p) => p !== codename)
        : [...role.permissions, codename]
      try {
        await this.rbacStore.setRolePermissions(role.id, next)
      } catch (e) {
        this.error = e.message
      }
    },
    async addRole() {
      this.error = ''
      const name = this.newRoleName.trim()
      if (!name) return
      try {
        await this.rbacStore.createRole(name)
        this.newRoleName = ''
      } catch (e) {
        this.error = e.message
      }
    },
    async removeRole(role) {
      this.error = ''
      try {
        await this.rbacStore.deleteRole(role.id)
      } catch (e) {
        this.error = e.message
      }
    },
    async renameRole(role, event) {
      const name = event.target.value.trim()
      event.target.value = name
      if (!name || name === role.name) return
      this.error = ''
      try {
        await this.rbacStore.renameRole(role.id, name)
      } catch (e) {
        this.error = e.message
      }
    },
  },
}
</script>
