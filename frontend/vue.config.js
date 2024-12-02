const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/': {
        target: 'http://192.168.10.27',
        changeOrigin: true,
        ws: false, // Desativa suporte a WebSocket
      },
    },
  },
});