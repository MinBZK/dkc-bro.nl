import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: {
      email: "",
      token: "",
      admin: false,
      isAuthenticated: false,
      org_name: "",
      org_code: "",
      org_id: "",
    },
    APIurl: "http://localhost:8000/api",
  },
  mutations: {
    changeUserEmail(state, payload) {
      state.user.email = payload;
    },
    changeUserToken(state, payload) {
      state.user.token = payload;
    },
    changeUserAdmin(state, payload) {
      state.user.admin = payload;
    },
    changeUserAuthenticated(state, payload) {
      state.user.isAuthenticated = payload;
    },
    changeAPIurl(state, payload) {
      state.APIurl = payload;
    },
    changeUserOrgName(state, payload) {
      state.user.org_name = payload;
    },
    changeUserOrgCode(state, payload) {
      state.user.org_code = payload;
    },
    changeOrgId(state, payload) {
      state.user.org_id = payload;
    },
  },
  actions: {
    updateUserEmail({ commit }, payload) {
      commit("changeUserEmail", payload);
    },
    updateUserToken({ commit }, payload) {
      commit("changeUserToken", payload);
    },
    updateUserAdmin({ commit }, payload) {
      commit("changeUserAdmin", payload);
    },
    updateUserAuthenticated({ commit }, payload) {
      commit("changeUserAuthenticated", payload);
    },
    updateAPIurl({ commit }, payload) {
      commit("changeAPIurl", payload);
    },
  },
  modules: {},
});
