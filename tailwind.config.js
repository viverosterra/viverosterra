/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './public/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        primary:  '#1B5E20',
        secondary:'#2E7D32',
        accent:   '#66BB6A',
        gold:     '#C9A94E',
        dark:     '#0D2B0E',
        wa:       '#25D366',
        bgwarm:   '#FAFAF7',
        bggreen:  '#F0F7F0',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
      },
    },
  },
  plugins: [],
}
