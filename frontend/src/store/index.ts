import { createStore } from "vuex";
import user from "./user";
import auth from "./auth";

const store = createStore({
  modules: {
    user,
    auth,
  },
});

export default store;
