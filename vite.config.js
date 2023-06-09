import { VitePWA } from 'vite-plugin-pwa'
import { resolve } from 'path'
import forwardToTrailingSlash from './vite/forward-to-trailing-slash.js'

const build = {
  outDir: '../dist',
  emptyOutDir: true,
  rollupOptions: {
    input: {
      index: resolve(__dirname, 'src/index.html'),
      store: resolve(__dirname, 'src/store/index.html'),
    }
  }
};
export default {
    root: 'src',
    publicDir: 'public',
    build: build,
    plugins: [
      forwardToTrailingSlash(Object.keys(build.rollupOptions.input)),
        VitePWA({
          "manifest": {
            name: "Bird Camera",
            short_name: "Bird.Camera",
            description: "Bird Feeder Camera in Cypress, Texas",
            start_url: "index.html",
            icons: [
              {
                src: "images/birb.svg",
                sizes: "48x48 72x72 96x96 128x128 256x256 512x512",
                type: "image/svg+xml",
                purpose: "any"
              }
            ],
            theme_color: "#67151b",
            background_color: "#a61b24",
            display: "standalone"  
          },
          workbox: {
            globPatterns: ['**/*.{js,css,html,ico,png,svg}']
          },
          registerType: 'autoUpdate',
          filename: 'service-worker.js'
        })
    ]
}
