import { createApp } from "vue";
// import Notification from "vue-notification"
import App from "./App.vue";
import router from "./router";
import authStore from "./store";

const app = createApp(App);

app.use(router);
app.use(authStore);
// app.use(Notification);

app.mount("#app");
