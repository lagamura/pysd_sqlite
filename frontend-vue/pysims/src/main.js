import "bootstrap/dist/css/bootstrap.css";
import "bootstrap"
import { createApp } from "vue";
import router from '@/router/router'
import App from "./App.vue";

createApp(App).use(router).mount("#app");

//import "bootstrap/dist/js/bootstrap.js";
