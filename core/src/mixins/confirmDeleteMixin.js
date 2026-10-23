export default {
  data() {
    return {
      dialogTitle: '',
      dialogMessage: '',
      pendingAction: null,
    }
  },
  methods: {
    confirmRemoval(title, message, action) {
      this.dialogTitle = title
      this.dialogMessage = message
      this.pendingAction = action
      this.$refs.confirmDialog?.open()
    },
    onConfirmDelete() {
      this.pendingAction?.()
    },
  },
}
