<script setup lang="ts">
import { Terminal } from "@xterm/xterm";
import "@xterm/xterm/css/xterm.css";

import { onMounted } from "vue";

onMounted(() => {
  var terminal = new Terminal({
    cursorBlink: "block",
    fontFamily: "monospace",
  });
  terminal.open(document.getElementById("terminal-container")!);

  let line = "";
  terminal.write("Welcome to ZTerm\n\r");
  terminal.write("Hello from \x1B[1;3;31mxterm.js\x1B[0m\n\r");
  terminal.write("$ ");

  terminal.attachCustomKeyEventHandler((ev) => {
    // console.log(ev.keyCode);
    if (ev.type === "keydown") {
      if (ev.keyCode === 13) {
        terminal.write("\n\r$ ");
        line = "";
      } else if (ev.keyCode == 8) {
        terminal.write("\b \b");
      } else {
        line += ev.key;
        terminal.write(ev.key);
      }
    }
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
  padding: 0.4em;
  background-color: white;
  color: white;
}
</style>
