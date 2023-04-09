import { defineConfig } from "vite"

export default defineConfig({
  build: {
    rollupOptions: {
      input: "index.html"
    },
    outDir: "../public/webapp",
    assetsDir: "static", // assets in other folder.
    emptyOutDir: true,
  }
})