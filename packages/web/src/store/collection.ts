import { defineStore } from 'pinia'

import { useConfigStore } from './config'

const loadingRequest = async (
  store: ILoadingState & { loading: number },
  callback: CallableFunction
) => {
  const increase = () => store.loading++
  const decrease = () => store.loading--

  const pass = (response: any, callback: CallableFunction) => {
    callback()
    return response
  }

  try {
    increase()

    return pass(await callback(), decrease)
  } catch (e) {
    decrease()
    throw e
  }
}

class KnowledgeIndexAPI {
  async request(method: 'GET' | 'POST' | 'DELETE', url: string, data?: object) {
    const configStore = useConfigStore()
    const response = await fetch(`${configStore.data.endpoint}${url}`, {
      headers: {
        'X-Shopware-Api-Key': configStore.data.key
      },
      body: JSON.stringify(data)
    })
    if (response.status !== 200) {
      throw response;
    }
    return response.json()
  }

  get(url: string) {
    return this.request('GET', url)
  }

  post(url: string, data: object) {
    return this.request('POST', url, data)
  }

  delete(url: string) {
    return this.request('DELETE', url)
  }
}

interface ILoadingState {
  loading: number
}

interface IStorage {
  [key: string]: string
}

interface ICollectionState {
  collection: object
  storage: IStorage
  summary: {
    documents: IDocument[]
  }
}

interface IDocument {
  description?: string
  heading?: string
  id?: string
  index_id?: number
  source?: string
  version?: string
}

export const useCollectionStore = defineStore('collection', {
  state: (): ICollectionState & ILoadingState => ({
    loading: 0,
    collection: {},
    storage: {},
    summary: {
      documents: []
    }
  }),
  actions: {
    async requireStorage() {
      if (!Object.keys(this.storage).length) {
        return
      }

      await this.fetchStorage()
    },
    async fetchStorage() {
      this.storage = {}
      this.storage = await loadingRequest(this, () => apiKI.get('/storage'))
    },
    async fetchCollection(collection: string) {
      this.collection = {}
      this.collection = Object.keys(this.storage)
        .filter((dir) => dir.includes(collection))
        .reduce((reduced: IStorage, key) => {
          reduced[key] = this.storage[key]
          return reduced
        }, {})
    },
    async fetchSummary(collection: string) {
      this.summary.documents = []
      this.summary = await loadingRequest(this, () => apiKI.get(`/summary/${collection}`))
    }
  }
})

export const apiKI = new KnowledgeIndexAPI()
