<template>
  <div id="basic-layout">
    <GlobalHeader />
    <main>
      <router-view />
    </main>
    <!-- <Footer /> -->
  </div>
</template>

<script setup lang="ts">
import GlobalHeader from "@/components/GlobalHeader.vue";
// import Footer from "../components/GlobalFooter.vue";
</script>

<style scoped>
#basic-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0; /* Add this line */
  padding: 0; /* Add this line */
}

main {
  flex-grow: 1;
  padding: 0; /* Ensure no padding */
  margin: 0; /* Ensure no margin */
}
</style>
