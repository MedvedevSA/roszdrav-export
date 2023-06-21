import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path";
import { crx } from '@crxjs/vite-plugin'
import manifest from './manifest.json' // Node 14 & 16

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    crx({ manifest }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: '3000',
  },
})
