import compress from 'vite-plugin-compress'
import { VitePWA } from 'vite-plugin-pwa'
export default {
    root: 'src',
    publicDir: 'public',
    build: {
      outDir: '../dist',
      emptyOutDir: true
    },
    plugins: [
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
