/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "/components/**/*.{js,ts,jsx,tsx,mdx}",
    "/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        white: "#FFF",
        black: "#000",
        gray: "#aaa",
        tertiary: "#4E0002",
      },
      backgroundImage: {
        "ou-background": "url(image.png)",
      },
    },
  },
  plugins: [],
};
