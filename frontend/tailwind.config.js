/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        wellsRed: "#c41230",
        wellsGold: "#ffcc00",
      },
    },
  },
  plugins: [],
}

