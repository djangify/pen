import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./static/js/**/*.js",
    "./**/*.html",
    "./**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [typography],
};
