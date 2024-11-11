import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import axios from "axios";
import store from "@/store/index";
import { User } from "@/types/user";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: () => import("@/views/Home.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/logout",
    name: "Logout",
    component: () => import("@/views/Logout.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/registreer-gebruiker",
    name: "Register-User",
    component: () => import("@/views/RegisterUser.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/wachtwoord-wijzigen",
    name: "update-password",
    component: () => import("@/views/UpdatePassword.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/wachtwoord-vergeten",
    name: "reset-password",
    component: () => import("@/views/ResetPassword.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/regels",
    name: "Rules",
    component: () => import("../views/Rules.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/bevindingen",
    name: "Findings",
    component: () => import("../views/Findings.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/documenten",
    name: "Documents",
    component: () => import("../views/Documents.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/batches",
    name: "Batches",
    component: () => import("../views/Batches.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("../views/Dashboard.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/demonstratie",
    name: "Demonstration",
    component: () => import("../views/Demonstration.vue"),
    meta: {
      requiresAuth: false,
    },
  },
  {
    path: "/projecten",
    name: "Projects",
    component: () => import("../views/Projects.vue"),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/verwerkingen",
    name: "Verwerkingen",
    component: () => import("../views/DemoTable.vue"),
    meta: {
      requiresAuth: true,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (sessionStorage.getItem("jwt") == null) {
      next({
        path: "/login",
        params: { nextUrl: to.fullPath },
      });
    } else {
      let token: string | null;
      if (store.state.user.token == "") {
        token = localStorage.getItem("jwt");
      } else {
        token = store.state.user.token;
      }
      axios
        .get(`${store.state.APIurl}/user/login/verifieer`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => {
          const response_data: User = response.data;
          store.commit("changeUserToken", token);
          store.commit("changeUserEmail", response_data.email);
          store.commit("changeUserAdmin", response_data.admin);
          store.commit("changeUserAuthenticated", true);
          store.commit("changeUserOrgName", response_data.org_name);
          store.commit("changeUserOrgCode", response_data.org_code);
          store.commit("changeOrgId", response_data.org_id);
          next({});
        })
        .catch((error) => {
          sessionStorage.removeItem("jwt");
          store.commit("changeUserToken", "");
          store.commit("changeUserEmail", "");
          store.commit("changeUserAdmin", false);
          store.commit("changeUserAuthenticated", false);
          store.commit("changeUserOrgName", "");
          store.commit("changeUserOrgCode", "");
          store.commit("changeOrgId", "");
          next({
            path: "/login",
            params: { nextUrl: to.fullPath },
          });
        });
    }
  } else {
    next({});
  }
});

export default router;
