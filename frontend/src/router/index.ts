import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import PendingView from "../views/PendingView.vue";
import SubmitPostView from "../views/SubmitPostView.vue";
import LoginRegisterView from "../views/LoginRegisterView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/pending",
      name: "pending",
      component: PendingView,
    },
    {
      path: "/upload",
      name: "upload",
      component: SubmitPostView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginRegisterView,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("user");
  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) {
    next("/login");
  } else {
    next();
  }
});

export default router;
