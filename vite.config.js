import { defineConfig } from 'vite';
import uni from '@dcloudio/vite-plugin-uni';

export default defineConfig({
  plugins: [uni()],
  server: {
    proxy: {
      '/api': {
        target: 'https://agent.dinghuo123.com',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            proxyReq.setHeader('Origin', 'https://agent.dinghuo123.com');
            proxyReq.setHeader('Referer', 'https://agent.dinghuo123.com/product/product');
            proxyReq.setHeader('Host', 'agent.dinghuo123.com');
          });
        }
      },
      '/sso': {
        target: 'https://sso.dinghuo123.com',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/sso/, ''),
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            proxyReq.setHeader('Origin', 'https://sso.dinghuo123.com');
            proxyReq.setHeader('Host', 'sso.dinghuo123.com');
          });
        }
      }
    },
  },
});
