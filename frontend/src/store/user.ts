import { Module } from "vuex";
import { CONFIG } from "@/constants/config";

interface UserState {
  username: string;
  userId: number | null;
  preferences: {
    theme: string;
  };
}

const user: Module<UserState, any> = {
  namespaced: true,
  state: {
    username: localStorage.getItem(CONFIG.AUTH.STORAGE_KEY.USERNAME) || "",
    userId: null,
    preferences: {
      theme: CONFIG.UI.THEME.DEFAULT,
    },
  },
  mutations: {
    setUsername(state, username: string) {
      state.username = username;
      localStorage.setItem(CONFIG.AUTH.STORAGE_KEY.USERNAME, username);
    },
    setUserId(state, userId: number) {
      state.userId = userId;
    },
    setTheme(state, theme: string) {
      state.preferences.theme = theme;
    },
  },
  actions: {
    updateUserTheme({ commit }, theme: string) {
      commit("setTheme", theme);
    },
    clearUsername({ commit }) {
      commit("setUsername", "");
      localStorage.removeItem(CONFIG.AUTH.STORAGE_KEY.USERNAME);
    },
  },
};

export default user;
