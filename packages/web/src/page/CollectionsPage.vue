<script setup lang="ts">
import { useCollectionStore } from '../store/collection'
import { computed } from 'vue'
import { useConfigStore } from '../store/config'

const collectionStore = useCollectionStore()
const configStore = useConfigStore()

collectionStore.fetchStorage()

const collectionsInfo = computed(() =>
  Object.keys(collectionStore.storage)
    .map((dir) => dir.split('/').slice(2).join('/'))
    .filter((dir) => !['docs', 'cache', 'db', 'sqlite', 'lost+found'].includes(dir))
    .map((dir) => ({ dir, collection: dir, type: '' }))
    .map((dirObj) => {
      const prefixes = [
        'docs-',
        'db-',
        'sqlite-'
        // 'cache-', // singleton
      ]
      dirObj = prefixes.reduce((reduced, prefix) => {
        if (reduced.dir.startsWith(prefix)) {
          reduced.type = prefix.substring(0, prefix.length - 1)
          reduced.collection = reduced.collection.substring(prefix.length)
        }
        return reduced
      }, dirObj)

      if (dirObj.dir.endsWith('_ingested')) {
        dirObj.type = 'ingested'
        dirObj.collection = dirObj.collection.substring(
          0,
          dirObj.collection.length - '_ingested'.length
        )
      }

      return dirObj
    })
)

const collections = computed(() => [
  ...new Set(collectionsInfo.value.map(({ collection }) => collection))
])
</script>

<template>
  <main>
    <h1>
      Collections ({{ collections.length }})
      <span class="loader" v-if="collectionStore.loading">Loading</span>
    </h1>

    <table>
      <thead>
        <th>Collection</th>
        <th>Download</th>
      </thead>
      <tbody>
        <tr v-for="collection in collections" :key="collection">
          <td>
            <router-link :to="{ name: 'collection', params: { collection: collection } }">{{
              collection
            }}</router-link>
          </td>
          <td>
            <a :href="`${configStore.data.endpoint}/download/docs/${collection}`" target="_blank"
              >docs.zip</a
            >
            &nbsp;
            <a :href="`${configStore.data.endpoint}/download/db/${collection}`" target="_blank"
              >db.zip</a
            >
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>
