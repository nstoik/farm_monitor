// vue.config.js

/**
 *  @tyype {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
  publicPath: process.env.VUE_APP_PUBLIC_PATH,
  pwa: {
    workboxPluginMode: "GenerateSW",
  },
};
