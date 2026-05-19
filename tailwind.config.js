module.exports = {
  content: ['./frontend/**/*.{html,js}', './contents/**/*.md'],
  theme: {
    extend: {},
    fontFamily: {
      'title': ['Crimson Text', 'serif'],
      'sidebar': ['Karla', 'sans-serif'],
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
