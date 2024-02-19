<script setup lang="ts">
import { ref, watch } from "vue";
import { useConfigStore } from "../store/config";
import { apiKI } from "../store/collection";
const configStore = useConfigStore();

const response = ref();
const checkMe = async () => {
  response.value = await apiKI.get('/me');
}

configStore.data.endpoint = localStorage.getItem('ai-web-endpoint') || '';
configStore.data.key = localStorage.getItem('ai-web-key') || '';

watch(
  () => configStore.data.endpoint,
  (value) => {
    localStorage.setItem("ai-web-endpoint", value);
  }
)

watch(
  () => configStore.data.key,
  (value) => {
    localStorage.setItem("ai-web-key", value);
  }
)

</script>

<template>
  <main>
    <h1>Me</h1>

    <div>
      <label>
        Endpoint
      </label>
      <input type="text" placeholder="http://172.18.0.1:10002" v-model="configStore.data.endpoint" />
    </div>
    <div>
      <label>
        API key
      </label>
      <input type="text" placeholder="X-Shopware-Api-Key" v-model="configStore.data.key" />
    </div>

    <p>Credentials will be stored in local storage unencrypted.</p>

    <button type="button" @click.prevent="checkMe">Check</button>
    {{ response }}
  </main>
</template>
