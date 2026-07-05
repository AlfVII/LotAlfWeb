import { defineStore } from 'pinia'

// Region/province/town selection carried across the app (replaces the old
// server-side Flask session — no more /update_session auth-bypass endpoint).
export const useSelection = defineStore('selection', {
  state: () => ({ region: '', province: '', town: '', number: '' }),
  actions: {
    set(patch) { Object.assign(this.$state, patch) },
    reset() { this.region = ''; this.province = ''; this.town = ''; this.number = '' },
  },
})
