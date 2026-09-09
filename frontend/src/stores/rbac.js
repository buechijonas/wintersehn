import { ref } from 'vue'
import { defineStore } from 'pinia'
import { apiFetch, extractErrorMessage } from '@/lib/api.js'

export const useRbacStore = defineStore('rbac', () => {
  const roles = ref([])
  const permissions = ref([])
  const users = ref([])

  async function fetchAll() {
    const [rolesResponse, permissionsResponse, usersResponse] = await Promise.all([
      apiFetch('/api/content/roles/'),
      apiFetch('/api/content/permissions/'),
      apiFetch('/api/auth/users/'),
    ])
    if (!rolesResponse.ok || !permissionsResponse.ok || !usersResponse.ok) {
      throw new Error('Rollen konnten nicht geladen werden.')
    }
    roles.value = await rolesResponse.json()
    permissions.value = await permissionsResponse.json()
    users.value = await usersResponse.json()
  }

  async function setUserRole(userId, roleId) {
    const response = await apiFetch(`/api/auth/users/${userId}/role/`, {
      method: 'PATCH',
      body: JSON.stringify({ role: roleId }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Rolle konnte nicht zugewiesen werden.'))
    }
    const user = users.value.find((u) => u.id === userId)
    if (user) user.role = data.role
    return data
  }

  async function setUserVerified(userId, verified) {
    const response = await apiFetch(`/api/auth/users/${userId}/verify/`, {
      method: 'PATCH',
      body: JSON.stringify({ verified }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Verifizierung konnte nicht geändert werden.'))
    }
    const user = users.value.find((u) => u.id === userId)
    if (user) user.verified = data.verified
    return data
  }

  async function deleteUser(userId) {
    const response = await apiFetch(`/api/auth/users/${userId}/`, { method: 'DELETE' })
    if (!response.ok) {
      const data = await response.json().catch(() => null)
      throw new Error(extractErrorMessage(data, 'Nutzer konnte nicht gelöscht werden.'))
    }
    users.value = users.value.filter((u) => u.id !== userId)
  }

  async function createRole(name) {
    const response = await apiFetch('/api/content/roles/', {
      method: 'POST',
      body: JSON.stringify({ name, permissions: [] }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Rolle konnte nicht erstellt werden.'))
    }
    roles.value.push(data)
    return data
  }

  async function renameRole(id, name) {
    const response = await apiFetch(`/api/content/roles/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ name }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Rolle konnte nicht umbenannt werden.'))
    }
    const role = roles.value.find((r) => r.id === id)
    if (role) role.name = data.name
    return data
  }

  async function setRolePermissions(id, permissionCodenames) {
    const response = await apiFetch(`/api/content/roles/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ permissions: permissionCodenames }),
    })
    const data = await response.json().catch(() => null)
    if (!response.ok) {
      throw new Error(extractErrorMessage(data, 'Berechtigungen konnten nicht geändert werden.'))
    }
    const role = roles.value.find((r) => r.id === id)
    if (role) role.permissions = data.permissions
    return data
  }

  async function deleteRole(id) {
    const response = await apiFetch(`/api/content/roles/${id}/`, { method: 'DELETE' })
    if (!response.ok) {
      const data = await response.json().catch(() => null)
      throw new Error(extractErrorMessage(data, 'Rolle konnte nicht gelöscht werden.'))
    }
    roles.value = roles.value.filter((r) => r.id !== id)
  }

  return {
    roles,
    permissions,
    users,
    fetchAll,
    createRole,
    renameRole,
    setRolePermissions,
    deleteRole,
    setUserRole,
    setUserVerified,
    deleteUser,
  }
})
