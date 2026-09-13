<script setup>
import { onMounted, ref } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import { profiles } from '@/assets/images.js'
import { icons } from '@/assets/icons.js'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'

const authStore = useAuthStore()
const rbacStore = useRbacStore()

const breadcrumbs = [{ label: 'Admin', to: '/admin' }, { label: 'Nutzer' }]

function avatarSrc(avatar) {
  return profiles[avatar] ?? icons.user
}

const error = ref('')

onMounted(async () => {
  try {
    await rbacStore.fetchAll()
  } catch (e) {
    error.value = e.message
  }
})

async function onUserRoleChange(user, event) {
  error.value = ''
  const value = event.target.value
  try {
    await rbacStore.setUserRole(user.id, value ? Number(value) : null)
  } catch (e) {
    error.value = e.message
  }
}

async function onUserVerifiedChange(user, event) {
  error.value = ''
  try {
    await rbacStore.setUserVerified(user.id, event.target.checked)
  } catch (e) {
    error.value = e.message
  }
}

async function onDeleteUser(user) {
  error.value = ''
  if (!confirm(`Möchtest du den Nutzer "${user.username}" wirklich löschen?`)) return
  try {
    await rbacStore.deleteUser(user.id)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <Page active-navigation="admin">
    <Breadcrumbs :items="breadcrumbs" />
    <div class="flex flex-col pt-8 pb-8 px-8 max-h-[calc(100vh-101px)] overflow-y-auto">
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
  </Page>
</template>

<style scoped>
.trash-icon {
  filter: brightness(0) saturate(100%) invert(54%) sepia(50%) saturate(3825%) hue-rotate(318deg)
    brightness(110%) contrast(101%);
}
</style>
