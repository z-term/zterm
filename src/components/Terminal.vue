<script setup lang="ts">
import { Terminal } from '@xterm/xterm';
import "@xterm/xterm/css/xterm.css";

import { onMounted } from 'vue';

onMounted(() => {
  var terminal = new Terminal({
    cursorBlink: 'block',
    fontFamily: 'monospace'
  });
  terminal.open(document.getElementById('terminal-container')!);
  terminal.write("Welcome to ZTerm\n\r\n\r");
  terminal.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ');
  console.log("hello world");

  terminal.onData((data) => {
    console.log('Terminal input:', data);
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

</style>
