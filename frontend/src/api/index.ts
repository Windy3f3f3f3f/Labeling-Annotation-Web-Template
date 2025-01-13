import axios from "axios";
import { ElMessage } from "element-plus";
import { CONFIG } from "@/constants/config";

// Create axios instance with configuration
const instance = axios.create({
  baseURL: CONFIG.API.BASE_URL,
  headers: {
    "Content-Type": CONFIG.API.CONTENT_TYPE,
  },
  timeout: CONFIG.API.TIMEOUT,
});

// Add response interceptor
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle error responses
    if (error.response) {
      const message = error.response.data?.error || "An error occurred";
      ElMessage.error(message);
    } else {
      ElMessage.error("Network error");
    }
    return Promise.reject(error);
  }
);

export default instance;
