import { RouteRecordRaw } from "vue-router";
import AnnotationView from "@/views/AnnotationView.vue";
import HomeView from "@/views/HomeView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Annotation",
    component: AnnotationView,
  },
  {
    path: "/home",
    name: "Home",
    component: HomeView,
  },
];

export default routes;
