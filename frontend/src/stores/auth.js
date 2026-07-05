import { defineStore } from 'pinia'
import { api } from '../api'

export const useAuth = defineStore('auth', {
  state: () => ({ token: localStorage.getItem('lotalf_token') || '', error: '' }),
  getters: { isEditor: (s) => !!s.token },
  actions: {
    async login(password) {
      this.error = ''
      try {
        const { token } = await api.login(password)
        this.token = token
        localStorage.setItem('lotalf_token', token)
        return true
      } catch (e) {
        this.error = e.message || 'No se pudo identificar'
        return false
      }
    },
    logout() {
      this.token = ''
      localStorage.removeItem('lotalf_token')
    },
  },
})
