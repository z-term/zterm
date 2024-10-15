<script setup lang="ts">
import { Terminal } from "@xterm/xterm";
import "@xterm/xterm/css/xterm.css";

import { FitAddon } from "@xterm/addon-fit";
import { onMounted } from "vue";

const terminal = new Terminal({
  cursorBlink: "block",
  fontFamily: "monospace",
});
const fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);

const fitTerm = () => {
  fitAddon.fit();
};

onMounted(() => {
  window.addEventListener("resize", fitTerm);

  terminal.open(document.getElementById("terminal-container")!);
  fitAddon.fit();

  let line = "";
  terminal.write("Welcome to \x1B[1;3;31mZTerm\x1B[0m\n\r");
  terminal.write("$ ");

  terminal.attachCustomKeyEventHandler((ev) => {
    if (ev.type === "keydown") {
      if (ev.code === "Enter") {
        terminal.write("\n\r$ ");
        line = "";
      } else if (ev.code == "Backspace") {
        terminal.write("\b \b");
      } else if (ev.ctrlKey) {
        if (ev.code == "KeyU") {
          terminal.clear();
        }
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
  height: calc(100vh-40px);
  padding: 0.4em;
  background-color: black;
  color: white;
  overflow-y: clip;
}

#terminal-container::-webkit-scrollbar {
  display: none;
}
</style>
