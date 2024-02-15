import { defineStore } from 'pinia'

interface IConfig {
  data: {
    endpoint?: string,
    key?: string
  }
}

export const useConfigStore = defineStore('config', {
  state: (): IConfig => ({
    data: {
      endpoint: import.meta.env.VITE_KNOWLEDGE_INDEX_ENDPOINT,
      key: import.meta.env.VITE_KNOWLEDGE_INDEX_KEY,
    }
  }),
  actions: {}
})
