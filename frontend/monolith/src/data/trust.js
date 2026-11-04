export const trustRingLabels = {
  1: 'Absolutes Vertrauen',
  10: 'Bekannte',
}

export const conductLabels = {
  promise_kept: 'Versprechen eingehalten',
  promise_broken: 'Versprechen gebrochen',
  punctual: 'Pünktlich',
  late: 'Unpünktlich',
  cancelled: 'Kurzfristig abgesagt',
  secret_kept: 'Geheimnis bewahrt',
  secret_shared: 'Geheimnis ausgeplaudert',
  supported: 'Unterstützt',
  let_down: 'Im Stich gelassen',
  honest: 'Ehrlich',
  lied: 'Gelogen',
  debt_repaid: 'Schulden beglichen',
  debt_unpaid: 'Schulden nicht beglichen',
  fault_admitted: 'Fehler eingestanden',
  fault_denied: 'Fehler nicht eingestanden',
  competed: 'Alles zum Wettbewerb gemacht',
}

export function formatPoints(points) {
  return points > 0 ? `+${points}` : `${points}`
}
