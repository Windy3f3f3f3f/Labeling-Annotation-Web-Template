const { CONFIG } = require("./src/constants/config.ts");

module.exports = {
  transpileDependencies: true,
  devServer: {
    port: CONFIG.FRONTEND.PORT,
  },
};
