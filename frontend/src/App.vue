<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="bg-blue-500 text-white py-4">
    <div class="wrapper mx-auto flex justify-between items-center">
      <nav class="flex justify-center w-full">
        <RouterLink to="/" class="text-lg font-semibold hover:text-gray-200">Home</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.wrapper {
  max-width: 1200px;
  padding: 0 20px;
}

nav a {
  text-decoration: none;
  color: inherit;
  margin-right: 20px;
}

nav a:hover {
  color: #d1d5db; /* Tailwind's gray-200 */
}
</style>
