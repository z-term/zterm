import { appWindow } from '@tauri-apps/api/window';
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/base.css";


document.getElementById('titlebar-minimize')?.addEventListener('click', () => appWindow.minimize());
document.getElementById('titlebar-maximize')?.addEventListener('click', () => appWindow.toggleMaximize());
document.getElementById('titlebar-close')?.addEventListener('click', () => appWindow.close());

createApp(App).mount("#app");
