import { appWindow } from "@tauri-apps/api/window";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/base.css";

document.getElementById("titlebar-minimize")?.addEventListener("click", () => appWindow.minimize());
document.getElementById("titlebar-maximize")?.addEventListener("click", () => appWindow.toggleMaximize());
document.getElementById("titlebar-close")?.addEventListener("click", () => appWindow.close());

window.addEventListener("keydown", (ev) => {
  if (ev.ctrlKey && ev.key === "r") {
    ev.preventDefault();
  }

  if (ev.ctrlKey && ev.shiftKey && ev.key === "I") {
    console.log("DONT OPEN");
    ev.preventDefault();
  }
});

window.addEventListener("keyup", (ev) => {
  if (ev.ctrlKey && ev.shiftKey && ev.key === "I") {
    console.log("DONT OPEN");
    ev.preventDefault();
  }
});

document.querySelector(".titlebar")?.addEventListener("contextmenu", (ev) => {
  ev.preventDefault();
});

createApp(App).mount("#app");
