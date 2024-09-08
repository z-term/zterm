<script setup lang="ts">
import { ref } from "vue";

const command = ref("");

// async function greet() {
//   greetMsg.value = await invoke("greet", { name: name.value });
// }
</script>

<template>
  <textarea id="stream" v-model="command" />
</template>


<style scoped>

textarea {
  border: none;
  width: 100%;
  background-color: black;
  color: white;
  outline: none;
  resize: none;
}

textarea::-webkit-scrollbar {
  display: none;
}

</style>