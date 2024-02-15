import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', {
  state: () => ({
    data: {
      endpoint: import.meta.env.VITE_KNOWLEDGE_INDEX_ENDPOINT,
      key: import.meta.env.VITE_KNOWLEDGE_INDEX_KEY,
    }
  }),
  actions: {}
})
