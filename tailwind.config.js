/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      // Placeholder palette until docs/figma/design-tokens.md exists with
      // real values from a Figma file — swap these when that happens.
      colors: {
            navy: {
        50: "#eef1f7",
        100: "#d7deec",
        200: "#b0bed9", // Added for calculator & error pages
        300: "#859bc2", // Added for directory hover states
        400: "#5b76a8",
        700: "#243a63",
        900: "#152647",
      },
        gold: {
          50: "#fdf8ec",
          100: "#faeec9",
          200: "#f5dd98",
          300: "#f0c968",
          400: "#e8b23e",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
