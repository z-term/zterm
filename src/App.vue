<script setup lang="ts">
import Terminal from "./components/Terminal.vue";
</script>

<template>
  <div class="container">
    <Terminal />
  </div>
</template>

<style scoped>

.container {
  display: flex;
  justify-content: start;
  align-items: top;
  height: calc(100vh - 40px);
}

</style>
