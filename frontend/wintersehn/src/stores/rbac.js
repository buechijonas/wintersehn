import { ref } from 'vue'
import { defineStore } from 'pinia'
import { json, request } from '@core/lib/api.js'

export const useRbacStore = defineStore('rbac', () => {
  const roles = ref([])
  const permissions = ref([])
  const users = ref([])

  async function fetchAll() {
    const fallback = 'Rollen konnten nicht geladen werden.'
    ;[roles.value, permissions.value, users.value] = await Promise.all([
      request('/api/content/roles/', fallback),
      request('/api/content/permissions/', fallback),
      request('/api/auth/users/', fallback),
    ])
  }

  async function changeUser(userId, action, data, fallback) {
    const changed = await request(
      `/api/auth/users/${userId}/${action}/`,
      fallback,
      json('PATCH', data),
    )
    users.value = users.value.map((user) => (user.id === userId ? changed : user))
    return changed
  }

  function setUserRole(userId, roleId) {
    return changeUser(userId, 'role', { role: roleId }, 'Rolle konnte nicht zugewiesen werden.')
  }

  function setUserVerified(userId, verified) {
    return changeUser(userId, 'verify', { verified }, 'Verifizierung konnte nicht geändert werden.')
  }

  async function createRole(name) {
    const role = await request(
      '/api/content/roles/',
      'Rolle konnte nicht erstellt werden.',
      json('POST', { name, permissions: [] }),
    )
    roles.value.push(role)
    return role
  }

  async function changeRole(id, data, fallback) {
    const changed = await request(`/api/content/roles/${id}/`, fallback, json('PATCH', data))
    roles.value = roles.value.map((role) => (role.id === id ? changed : role))
    return changed
  }

  function renameRole(id, name) {
    return changeRole(id, { name }, 'Rolle konnte nicht umbenannt werden.')
  }

  function setRolePermissions(id, codenames) {
    return changeRole(
      id,
      { permissions: codenames },
      'Berechtigungen konnten nicht geändert werden.',
    )
  }

  async function deleteRole(id) {
    await request(`/api/content/roles/${id}/`, 'Rolle konnte nicht gelöscht werden.', {
      method: 'DELETE',
    })
    roles.value = roles.value.filter((role) => role.id !== id)
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
  }
})
