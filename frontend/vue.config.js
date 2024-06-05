'use strict'
const path = require('path')
const defaultSettings = require('./src/settings.js')

function resolve(dir) {
  return path.join(__dirname, dir)
}

const name = defaultSettings.title || 'vue Element Admin' // page title

const port = process.env.port || process.env.npm_config_port || 9527 // dev port

// Get local IP address
const os = require('os');
const networkInterfaces = os.networkInterfaces();
let localIp = '127.0.0.1';  // Default to localhost
Object.keys(networkInterfaces).forEach(interfaceName => {
  const interfaces = networkInterfaces[interfaceName];
  for (const iface of interfaces) {
    if ('IPv4' !== iface.family || iface.internal !== false) continue;
    localIp = iface.address;
    break;
  }
});

module.exports = {
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',
  lintOnSave: process.env.NODE_ENV === 'development',
  productionSourceMap: false,
  devServer: {
    allowedHosts: [ 'localhost', 'websystem.life', '140.113.207.22', ],
    host: '0.0.0.0',  // Listen on all network interfaces
    port: 8080,
    open: true,
    overlay: {
      warnings: false,
      errors: true
    },
    public: `http://${localIp}:8080`,  // Use the detected local IP
    proxy: {
      '/api/':{
        target: `http://0.0.0.0:8000`,  // Assuming your backend is also on the same machine
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    name: name,
    resolve: {
      alias: {
        '@': resolve('src')
      }
    }
  },
  chainWebpack(config) {
    // ... (rest of the configuration remains unchanged)
  }
}