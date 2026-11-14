/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        kivu: {
          50: "#EAF1F3",
          100: "#D3E1E6",
          200: "#A9C3CC",
          400: "#4F8294",
          600: "#1F5A70",
          700: "#14475C",
          800: "#0D3B4F",
          900: "#082A39",
        },
        mist: {
          DEFAULT: "#EFF3F1",
          deep: "#E2E9E6",
        },
        sun: {
          100: "#FDF0CC",
          300: "#F9D26B",
          400: "#F6B72B",
          500: "#E3A01A",
        },
        hill: {
          100: "#DDEEE3",
          600: "#2C7A4B",
          700: "#236240",
        },
        clay: {
          100: "#F6DFD9",
          600: "#B4432F",
        },
        slate2: "#4A6672",
      },
      fontFamily: {
        sans: ["Bricolage Grotesque", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Bricolage Grotesque", "ui-sans-serif", "system-ui", "sans-serif"],
        serif: ["Source Serif 4", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
        reading: ["Source Serif 4", "ui-serif", "Georgia", "Cambria", "Times New Roman", "Times", "serif"],
      },
      typography: ({ theme }) => ({
        tera: {
          css: {
            '--tw-prose-body': theme('colors.kivu.900'),
            '--tw-prose-headings': theme('colors.kivu.900'),
            '--tw-prose-lead': theme('colors.kivu.700'),
            '--tw-prose-links': theme('colors.kivu.700'),
            '--tw-prose-bold': theme('colors.kivu.900'),
            '--tw-prose-counters': theme('colors.slate2'),
            '--tw-prose-bullets': theme('colors.slate2'),
            '--tw-prose-hr': theme('colors.kivu.100'),
            '--tw-prose-quotes': theme('colors.kivu.900'),
            '--tw-prose-quote-borders': theme('colors.sun.400'),
            '--tw-prose-captions': theme('colors.slate2'),
            '--tw-prose-code': theme('colors.kivu.900'),
            '--tw-prose-pre-code': theme('colors.kivu.50'),
            '--tw-prose-pre-bg': theme('colors.kivu.900'),
            '--tw-prose-th-borders': theme('colors.kivu.100'),
            '--tw-prose-td-borders': theme('colors.kivu.100'),
            fontSize: '1.1875rem',
            lineHeight: '1.72',
            fontFamily: theme('fontFamily.serif').join(', '),
            a: {
              color: theme('colors.kivu.700'),
              textDecoration: 'underline',
              textDecorationColor: theme('colors.sun.400'),
              textDecorationThickness: '2px',
              textUnderlineOffset: '4px',
              fontWeight: '500',
              '&:hover': {
                color: theme('colors.kivu.900'),
              },
            },
            'h1, h2, h3, h4': {
              fontFamily: theme('fontFamily.display').join(', '),
              letterSpacing: '-0.025em',
            },
          },
        },
      }),
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
