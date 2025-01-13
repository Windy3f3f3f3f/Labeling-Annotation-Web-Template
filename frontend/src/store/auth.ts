import { Module } from "vuex";

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
}

const auth: Module<AuthState, any> = {
  namespaced: true,
  state: {
    token: null,
    isAuthenticated: false,
  },
  mutations: {
    setToken(state, token: string) {
      state.token = token;
      state.isAuthenticated = true;
    },
    clearAuth(state) {
      state.token = null;
      state.isAuthenticated = false;
    },
  },
  actions: {
    login({ commit }, token: string) {
      commit("setToken", token);
    },
    logout({ commit }) {
      commit("clearAuth");
    },
  },
};

export default auth;
