<script setup lang="ts">
import { ref } from "vue";
import { apiKI } from "../store/collection";

const isOpen = ref(false);
const dialog = ref<HTMLDialogElement>();
const close = () => {
  dialog.value?.close('cancel');
  isOpen.value = false;
}

const clearCache = () => {
  apiKI.delete('/cache');
  isOpen.value = false;
};
</script>

<template>
  <main>
    <h1>Cache</h1>

    <button type="button" @click.prevent="isOpen = true">Clear</button>

    <dialog :open="isOpen" @cancel="console.log" @clear="console.error" :ref="dialog">
      Do you really want to delete all cache?
      <form method="dialog">
        <button type="button" value="cancel" @click.prevent="close">Cancel</button>
        <button type="button" value="clear" @click.prevent="clearCache">Okay, clear cache</button>
      </form>
    </dialog>
  </main>
</template>
