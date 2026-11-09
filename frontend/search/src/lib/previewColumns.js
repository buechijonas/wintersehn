import { ref, watch } from 'vue'

const STORAGE_KEY = 'wntrs-image-preview-columns'
export const GRID_COLUMNS = 5
export const DEFAULT_PREVIEW_COLUMNS = 2
const MIN_COLUMNS = 1
const MAX_COLUMNS = 3

export function clampPreviewColumns(columns) {
  return Math.min(Math.max(Math.round(columns), MIN_COLUMNS), MAX_COLUMNS)
}

function readStoredColumns() {
  try {
    const stored = Number(localStorage.getItem(STORAGE_KEY))
    return stored ? clampPreviewColumns(stored) : DEFAULT_PREVIEW_COLUMNS
  } catch {
    return DEFAULT_PREVIEW_COLUMNS
  }
}

export const previewColumns = ref(readStoredColumns())

watch(previewColumns, (columns) => {
  try {
    localStorage.setItem(STORAGE_KEY, String(columns))
  } catch {
    return
  }
})
