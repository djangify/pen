module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
    './**/*.html',
    './**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#227c81',
        secondary: '#f7f0e5',
        accent: '#f8fafc',
      },
    },
  },
  plugins: [
    '@tailwindcss/typography'
  ],
}
