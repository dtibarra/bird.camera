/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      keyframes: {
        "flip-horizontal": {
          '50%': { transform: 'rotateY(180deg)' }
        },
      },
      animation: {
        "flip-horizontal": 'flip-horizontal 2s linear',
      },
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
}