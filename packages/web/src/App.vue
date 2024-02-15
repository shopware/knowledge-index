<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav class="MainNav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/collections">Collections</RouterLink>
      <RouterLink to="/storage">Storage</RouterLink>
      <RouterLink to="/cache">Cache</RouterLink>
      <RouterLink to="/healthcheck">Healthcheck</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style>
.MainNav {
  @apply flex gap-2;
}
</style>
