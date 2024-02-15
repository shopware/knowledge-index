<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="items-center justify-between">
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

<style lang="scss">
.MainNav {
  @apply flex gap-4 items-center justify-center h-[4rem];

  a {
    @apply text-lg decoration-none text-inherit;
    &.router-link-active,
    &:hover {
      @apply decoration-underline;
    }
  }
}

main {
  margin: 0 auto;
  max-width: 1024px;
  width: 100%;
}
</style>
