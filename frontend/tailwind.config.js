/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        healthcare: {
          dark: '#0b1329',
          card: '#111c38',
          border: '#1e2d54',
          cyan: '#06b6d4',
          blue: '#3b82f6',
          emerald: '#10b981',
          rose: '#f43f5e',
        }
      }
    },
  },
  plugins: [],
}
