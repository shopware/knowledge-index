<script setup lang="ts">
import { ref } from "vue";
import { useConfigStore } from "../store/config";
import { apiKI } from "../store/collection";
const configStore = useConfigStore();

const response = ref();
const checkMe = async () => {
  response.value = await apiKI.get('/me');
}

</script>

<template>
  <main>
    <h1>Me</h1>

    <div>
      <label>
        Endpoint
      </label>
      <input type="text" placeholder="http://172.18.0.1:10002" v-model="configStore.data.endpoint" />
      <label>
        API key
      </label>
      <input type="text" placeholder="X-Shopware-Api-Key" v-model="configStore.data.key" />
    </div>

    <button type="button" @click.prevent="checkMe">Check</button>
    {{ response }}
  </main>
</template>
