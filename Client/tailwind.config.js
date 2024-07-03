/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "spotify-black": "#131313",
        "spotify-green": "#18d860",
      },
    },
  },
  plugins: [],
};
