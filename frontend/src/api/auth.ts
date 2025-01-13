import axios from "./index";

export const login = async (username: string, password: string) => {
  try {
    const response = await axios.post("/auth/login", { username, password });
    return response.data;
  } catch (error) {
    throw new Error("Login failed");
  }
};

export const logout = async () => {
  try {
    const response = await axios.post("/auth/logout");
    return response.data;
  } catch (error) {
    throw new Error("Logout failed");
  }
};
