<script setup lang="ts">
import { useCollectionStore } from '../store/collection'
import { useConfigStore } from '../store/config'
import { useRoute } from 'vue-router'
import { watch } from 'vue'

const collectionStore = useCollectionStore()
const configStore = useConfigStore()

const route = useRoute()

const updateState = async () => {
  await collectionStore.requireStorage()
  collectionStore.fetchCollection(route.params.collection as string)
  collectionStore.fetchSummary(route.params.collection as string)
}

watch(
  () => route.params.collection,
  (value) => value && updateState(),
  {
    immediate: true
  }
)
</script>

<template>
  <main>
    <h1>
      {{ $route.params.collection }}
      <span v-if="collectionStore.loading">Loading</span>
      <span v-else>({{ collectionStore.summary.documents.length }} documents)</span>
    </h1>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Version</th>
          <th>Heading</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(document, i) in collectionStore.summary.documents"
          :key="`${i}${document.source}`"
        >
          <td :title="document.source">
            <a :href="`${configStore.data.endpoint}/download${document.source}`" target="_blank">{{
              document.id
            }}</a>
          </td>
          <td>{{ document.version }}</td>
          <td>{{ document.heading }}</td>
          <td>{{ document.description }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>
