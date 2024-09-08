<script setup lang="ts">
import { Terminal } from '@xterm/xterm';
import { onMounted } from 'vue';


onMounted(() => {
  var terminal = new Terminal();
  terminal.open(document.getElementById('terminal-container')!);
  terminal.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ');
  console.log("hello world");

  terminal.onData((data) => {
    console.log('Terminal input:', data);
    // backend
  });
});

// async function greet() {
//   greetMsg.value = await invoke("greet", { name: name.value });
// }

</script>

<template>
  <div id="terminal-container" />
</template>


<style scoped>


#terminal-container {
  width: 100%;
  height: 100%;
  background-color: black;
  color: white;
}

/* 
textarea {
  border: none;
  width: 100%;
  background-color: black;
  color: white; 
  outline: none;
  resize: none;
  font-size: 1.5rem;
}

textarea::-webkit-scrollbar {
  display: none;
} */

</style>