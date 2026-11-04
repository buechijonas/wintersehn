import { ref, watch } from 'vue'

const STORAGE_KEY = 'handedness'
const VALID_MODES = ['right', 'left']

function readStoredMode() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    return VALID_MODES.includes(stored) ? stored : 'right'
  } catch {
    return 'right'
  }
}

export const handedness = ref(readStoredMode())

watch(handedness, (mode) => {
  try {
    localStorage.setItem(STORAGE_KEY, mode)
  } catch {
    return
  }
})
