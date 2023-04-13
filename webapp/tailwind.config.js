/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./index.html"
  ],
  theme: {
    extend: {
      colors: {
        // From https://www.happyhues.co/palettes/16
        'tinyui-chestnut': {
          // Let color into degree.
          // The author has not basic knowledge of music theory.
          'tonic': '#55423d',
          'superleading': '#fff3ec',
          'subdominant': '#9656a1',
          'dominant': '#ffc0ad',
          'submediant': '#e78fb3',
          'leading': '#140d0b',
        },
      },
    },
  },
  plugins: [],
}
