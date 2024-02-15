import { defineStore } from 'pinia'

interface IConfigData {
  endpoint: string | null,
  key: string | null
}

interface IConfig {
  data: IConfigData
}

export const useConfigStore = defineStore('config', {
  state: (): IConfig => ({
    data: {
      endpoint: import.meta.env.VITE_KNOWLEDGE_INDEX_ENDPOINT || '',
      key: import.meta.env.VITE_KNOWLEDGE_INDEX_KEY || '',
    }
  }),
  actions: {}
})
