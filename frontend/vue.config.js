const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/': {
        target: 'http://192.168.1.5:8000',
        changeOrigin: true,
      }
    }
  }
});