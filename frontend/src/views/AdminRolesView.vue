<script setup>
import { onMounted, ref } from 'vue'
import Page from '@/components/layout/Page.vue'
import Breadcrumbs from '@/components/common/Breadcrumbs.vue'
import Footer from '@/components/common/Footer.vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRbacStore } from '@/stores/rbac.js'

const authStore = useAuthStore()
const rbacStore = useRbacStore()

const breadcrumbs = [
  { label: 'Admin', to: '/admin' },
  { label: 'Rollen & Rechte' },
]

const error = ref('')
const newRoleName = ref('')

onMounted(async () => {
  try {
    await rbacStore.fetchAll()
  } catch (e) {
    error.value = e.message
  }
})

function hasPermission(role, codename) {
  return role.permissions.includes(codename)
}

async function togglePermission(role, codename) {
  error.value = ''
  const next = hasPermission(role, codename)
    ? role.permissions.filter((p) => p !== codename)
    : [...role.permissions, codename]
  try {
    await rbacStore.setRolePermissions(role.id, next)
  } catch (e) {
    error.value = e.message
  }
}

async function addRole() {
  error.value = ''
  const name = newRoleName.value.trim()
  if (!name) return
  try {
    await rbacStore.createRole(name)
    newRoleName.value = ''
  } catch (e) {
    error.value = e.message
  }
}

async function removeRole(role) {
  error.value = ''
  try {
    await rbacStore.deleteRole(role.id)
  } catch (e) {
    error.value = e.message
  }
}

async function renameRole(role, event) {
  const name = event.target.value.trim()
  event.target.value = name
  if (!name || name === role.name) return
  error.value = ''
  try {
    await rbacStore.renameRole(role.id, name)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <Page active-navigation="admin">
    <Breadcrumbs :items="breadcrumbs" />
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
    <Footer />
  </Page>
</template>
