/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // TLP colors
        tlp: {
          white: '#FFFFFF',
          green: '#33FF00',
          amber: '#FFC000',
          red: '#FF0033',
        },
      },
    },
  },
  plugins: [],
};
