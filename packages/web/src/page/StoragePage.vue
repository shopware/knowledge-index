<script setup lang="ts">
import { useCollectionStore } from '../store/collection'
import { computed } from 'vue'

const collectionStore = useCollectionStore()

collectionStore.fetchStorage()

const total = computed(() =>
  Object.values(collectionStore.storage).reduce((reduced, size) => {
    let diff = parseInt(size.substring(0, size.length - 1))
    if (size.endsWith('K')) {
      diff /= 1000
    } else if (size.endsWith('G')) {
      diff *= 1000
    }
    return reduced + diff
  }, 0.0)
)
</script>

<template>
  <main>
    <h1>Storage ({{ total }}MB)</h1>

    <table>
      <thead>
        <th>Directory</th>
        <th>Size</th>
      </thead>
      <tbody>
        <tr v-for="(size, collection) in collectionStore.storage" :key="collection">
          <td>
            {{ collection }}
          </td>
          <td>
            {{ size }}
          </td>
        </tr>
      </tbody>
    </table>
  </main>
</template>
