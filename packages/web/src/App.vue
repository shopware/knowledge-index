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
      <RouterLink to="/me">Me</RouterLink>
    </nav>

    <div>
      <input type="text" placeholder="X-Shopware-Api-Key" />
    </div>
  </header>

  <RouterView />
</template>

<style>
.MainNav {
  @apply flex gap-2;
}
</style>
