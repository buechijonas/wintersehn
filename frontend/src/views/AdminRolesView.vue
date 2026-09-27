<template>
  <BaseBreadcrumbs :items="breadcrumbs" />
  <div class="flex flex-col pb-8 px-8 max-h-[calc(100dvh-101px)] overflow-y-auto lg:max-h-none lg:overflow-y-visible lg:flex-1">
    <div class="w-full">
      <div class="flex items-center justify-between gap-4 my-4">
        <h2 class="text-xl">Rollen &amp; Rechte</h2>
        <AddButton
          v-if="authStore.user?.can_add_role"
          label="Rolle hinzufügen"
          to="/admin/roles/create"
        />
      </div>

      <p v-if="error" class="text-error text-sm mb-4">{{ error }}</p>

      <div class="overflow-x-auto">
        <table class="table">
          <thead>
            <tr>
              <th>Berechtigung</th>
              <th v-for="role in rbacStore.roles" :key="role.id" class="w-56 min-w-56">
                <div class="flex flex-col gap-1">
                  <div v-if="isEditingRole(role.id)" class="flex items-center gap-1">
                    <input
                      type="text"
                      class="input input-sm w-full min-w-0"
                      :value="role.name"
                      :disabled="!authStore.user?.can_change_role"
                      @change="renameRole(role, $event)"
                    />
                    <SaveButton class="shrink-0" @click="stopEditingRole(role.id)" />
                    <DeleteButton
                      v-if="authStore.user?.can_delete_role"
                      class="shrink-0"
                      @click="removeRole(role)"
                    />
                  </div>
                  <div v-else class="flex items-center justify-between gap-2">
                    <span class="font-medium truncate">{{ role.name }}</span>
                    <EditButton
                      class="shrink-0"
                      :disabled="!!editRoleBlockedReason(role)"
                      :title="editRoleBlockedReason(role) || 'Bearbeiten'"
                      @click="startEditingRole(role.id)"
                    />
                  </div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(permission, index) in sortedPermissions" :key="permission.codename">
              <tr v-if="isNewGroup(index)">
                <td
                  :colspan="1 + rbacStore.roles.length"
                  class="bg-base-200 text-xs uppercase tracking-wide text-wntrs-muted font-medium"
                >
                  {{ permissionGroupLabel(permission.codename) }}
                </td>
              </tr>
              <tr>
                <td class="text-wntrs-slate">
                  <div class="flex items-center gap-2">
                    <img
                      v-if="permissionMeta(permission.codename)"
                      :src="icons[permissionMeta(permission.codename).icon]"
                      alt=""
                      class="size-4 shrink-0"
                      :class="permissionMeta(permission.codename).iconFilterClass"
                    />
                    <span>{{ permissionLabel(permission) }}</span>
                  </div>
                </td>
                <td v-for="role in rbacStore.roles" :key="role.id" class="text-center">
                  <input
                    v-if="isEditingRole(role.id)"
                    type="checkbox"
                    class="checkbox align-middle"
                    :checked="hasPermission(role, permission.codename)"
                    :disabled="!canTogglePermission(role, permission.codename)"
                    @change="togglePermission(role, permission.codename)"
                  />
                  <span v-else class="inline-flex size-6 items-center justify-center align-middle">
                    <img
                      :src="hasPermission(role, permission.codename) ? icons['check-circle'] : icons.circle"
                      alt=""
                      class="size-4"
                      :class="hasPermission(role, permission.codename) ? 'icon-tint-success' : 'icon-tint-slate'"
                    />
                  </span>
                </td>
              </tr>
            </template>
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
import AddButton from '@/components/common/AddButton.vue'
import EditButton from '@/components/common/EditButton.vue'
import SaveButton from '@/components/common/SaveButton.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'
import { icons } from '@/assets/icons.js'
import asyncActionMixin from '@/mixins/asyncActionMixin.js'

const PERMISSION_META = {
  add: { icon: 'add', iconFilterClass: 'icon-tint-success' },
  view: { icon: 'circle-book-open', iconFilterClass: 'icon-tint-neutral' },
  change: { icon: 'pen-circle', iconFilterClass: 'icon-tint-warning' },
  delete: { icon: 'circle-trash', iconFilterClass: 'icon-tint-error' },
  assign: { icon: 'crown', iconFilterClass: 'icon-tint-warning' },
}

const VERB_ORDER = ['add', 'view', 'change', 'assign', 'delete']

const RESOURCE_ORDER = [
  'about',
  'ethos',
  'cv',
  'countries',
  'media',
  'role',
  'permission',
  'user',
  'admin',
  'sitecontent',
]

const RESOURCE_LABELS = {
  about: 'Über mich',
  ethos: 'Ethos',
  cv: 'Lebenslauf',
  countries: 'Länder',
  media: 'Medien',
  role: 'Rollen',
  permission: 'Berechtigungen',
  user: 'Nutzer',
  admin: 'Admin',
  sitecontent: 'Inhalte (allgemein)',
}

export default {
  name: 'AdminRolesView',
  components: {
    BaseBreadcrumbs,
    BaseFooter,
    DeleteButton,
    EditButton,
    SaveButton,
    AddButton,
  },
  mixins: [asyncActionMixin],
  data() {
    return {
      icons,
      breadcrumbs: [
        { label: 'Admin', to: '/admin' },
        { label: 'Rollen & Rechte' },
      ],
      editingRoleIds: [],
    }
  },
  computed: {
    authStore() {
      return useAuthStore()
    },
    rbacStore() {
      return useRbacStore()
    },
    sortedPermissions() {
      return [...this.rbacStore.permissions].sort((a, b) => {
        const [verbA, resourceA] = a.codename.split('_')
        const [verbB, resourceB] = b.codename.split('_')
        const resourceDiff = this.resourceIndex(resourceA) - this.resourceIndex(resourceB)
        if (resourceDiff !== 0) return resourceDiff
        return this.verbIndex(verbA) - this.verbIndex(verbB)
      })
    },
  },
  mounted() {
    return this.runAction(() => this.rbacStore.fetchAll())
  },
  methods: {
    permissionMeta(codename) {
      const verb = codename.split('_')[0]
      // "manage" permissions are treated the same as "change" until they're
      // split into granular add/change/delete/view permissions server-side.
      return PERMISSION_META[verb] ?? (verb === 'manage' ? PERMISSION_META.change : null)
    },
    permissionLabel(permission) {
      if (!this.permissionMeta(permission.codename)) return permission.name
      return permission.name.replace(/^Can\s+\S+\s+/i, '')
    },
    resourceOf(codename) {
      return codename.split('_').slice(1).join('_')
    },
    resourceIndex(resource) {
      const index = RESOURCE_ORDER.indexOf(resource)
      return index === -1 ? RESOURCE_ORDER.length : index
    },
    verbIndex(verb) {
      const index = VERB_ORDER.indexOf(verb)
      return index === -1 ? VERB_ORDER.length : index
    },
    permissionGroupLabel(codename) {
      const resource = this.resourceOf(codename)
      return RESOURCE_LABELS[resource] ?? resource
    },
    isNewGroup(index) {
      if (index === 0) return true
      const current = this.resourceOf(this.sortedPermissions[index].codename)
      const previous = this.resourceOf(this.sortedPermissions[index - 1].codename)
      return current !== previous
    },
    isOwnRole(role) {
      return role.name === this.authStore.user?.role
    },
    editRoleBlockedReason(role) {
      if (!this.authStore.user?.can_change_role) return 'Du hast keine Berechtigung, Rollen zu bearbeiten.'
      if (this.isOwnRole(role)) return 'Du kannst deine eigene aktuelle Rolle nicht bearbeiten.'
      return ''
    },
    canTogglePermission(role, codename) {
      const user = this.authStore.user
      if (!user?.can_change_role) return false
      if (this.hasPermission(role, codename)) return !!user.can_delete_permission
      return !!user.can_add_permission && !!user.permissions?.includes(codename)
    },
    isEditingRole(roleId) {
      return this.editingRoleIds.includes(roleId)
    },
    startEditingRole(roleId) {
      if (!this.isEditingRole(roleId)) this.editingRoleIds.push(roleId)
    },
    stopEditingRole(roleId) {
      this.editingRoleIds = this.editingRoleIds.filter((id) => id !== roleId)
    },
    hasPermission(role, codename) {
      return role.permissions.includes(codename)
    },
    togglePermission(role, codename) {
      const next = this.hasPermission(role, codename)
        ? role.permissions.filter((p) => p !== codename)
        : [...role.permissions, codename]
      return this.runAction(() => this.rbacStore.setRolePermissions(role.id, next))
    },
    removeRole(role) {
      return this.runAction(() => this.rbacStore.deleteRole(role.id))
    },
    renameRole(role, event) {
      const name = event.target.value.trim()
      event.target.value = name
      if (!name || name === role.name) return
      return this.runAction(() => this.rbacStore.renameRole(role.id, name))
    },
  },
}
</script>
