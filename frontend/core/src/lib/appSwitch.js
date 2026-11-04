export function appSwitchTargets(app, user) {
  if (!app.appSwitches || !user) return []
  return app.appSwitches.filter((target) => !target.permission || user[target.permission])
}
