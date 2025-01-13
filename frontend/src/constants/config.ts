/**
 * Global configuration
 */
export const CONFIG = {
  // Backend API configuration
  API: {
    BASE_URL: "http://YOUR_IP:5000",
    TIMEOUT: 10000,
    CONTENT_TYPE: "application/json",
  },

  // Frontend configuration
  FRONTEND: {
    PORT: 8080,
  },

  // Auth configuration
  AUTH: {
    STORAGE_KEY: {
      USERNAME: "username",
    },
  },

  // UI configuration
  UI: {
    THEME: {
      DEFAULT: "light",
    },
  },
};

// Helper functions
export const getBaseUrl = () => CONFIG.API.BASE_URL;
