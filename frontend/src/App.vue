<template>
  <BasicLayout>
    <router-view />
  </BasicLayout>
</template>

<script setup lang="ts">
// Import basic layout component
import BasicLayout from "./layouts/BasicLayout.vue";
</script>

<style scoped>
body {
  font-family: "Roboto", sans-serif;
  color: #333333;
}
</style>
