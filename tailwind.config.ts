/** @type {import('tailwindcss').Config} */

/*
 * IMPORTANT — why every custom colour below is an object with a DEFAULT key.
 *
 * The colours were originally written as flat hex strings, e.g.  slate: '#1e293b'.
 * Because they sit under `extend`, a string REPLACES Tailwind's whole scale for
 * that name: `text-slate` worked, but `text-slate-100`, `border-slate-200`,
 * `text-slate-700` and `text-emerald-200` silently generated NO css at all.
 * That is what made the code blocks black-on-black (the <pre> fell back to the
 * inherited body colour #0f172a on a #0f172a background) and removed the border
 * from every card.
 *
 * Writing `slate: { DEFAULT: '#1e293b', 50: …, 100: … }` keeps the flat
 * `text-slate` working exactly as before AND restores the numeric shades.
 * Never collapse these back to strings.
 */

const slate = {
  DEFAULT: '#1e293b',
  50: '#f8fafc', 100: '#f1f5f9', 200: '#e2e8f0', 300: '#cbd5e1',
  400: '#94a3b8', 500: '#64748b', 600: '#475569', 700: '#334155',
  800: '#1e293b', 900: '#0f172a', 950: '#020617',
};

const amber = {
  DEFAULT: '#f59e0b',
  50: '#fffbeb', 100: '#fef3c7', 200: '#fde68a', 300: '#fcd34d',
  400: '#fbbf24', 500: '#f59e0b', 600: '#d97706', 700: '#b45309',
  800: '#92400e', 900: '#78350f', 950: '#451a03',
};

const emerald = {
  DEFAULT: '#059669',
  50: '#ecfdf5', 100: '#d1fae5', 200: '#a7f3d0', 300: '#6ee7b7',
  400: '#34d399', 500: '#10b981', 600: '#059669', 700: '#047857',
  800: '#065f46', 900: '#064e3b', 950: '#022c22',
};

const sky = {
  DEFAULT: '#0ea5e9',
  50: '#f0f9ff', 100: '#e0f2fe', 200: '#bae6fd', 300: '#7dd3fc',
  400: '#38bdf8', 500: '#0ea5e9', 600: '#0284c7', 700: '#0369a1',
  800: '#075985', 900: '#0c4a6e', 950: '#082f49',
};

const rose = {
  DEFAULT: '#e11d48',
  50: '#fff1f2', 100: '#ffe4e6', 200: '#fecdd3', 300: '#fda4af',
  400: '#fb7185', 500: '#f43f5e', 600: '#e11d48', 700: '#be123c',
  800: '#9f1239', 900: '#881337', 950: '#4c0519',
};

const violet = {
  DEFAULT: '#7c3aed',
  50: '#f5f3ff', 100: '#ede9fe', 200: '#ddd6fe', 300: '#c4b5fd',
  400: '#a78bfa', 500: '#8b5cf6', 600: '#7c3aed', 700: '#6d28d9',
  800: '#5b21b6', 900: '#4c1d95', 950: '#2e1065',
};

const stone = {
  DEFAULT: '#78716c',
  50: '#fafaf9', 100: '#f5f5f4', 200: '#e7e5e4', 300: '#d6d3d1',
  400: '#a8a29e', 500: '#78716c', 600: '#57534e', 700: '#44403c',
  800: '#292524', 900: '#1c1917', 950: '#0c0a09',
};

module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#0f172a',
        paper: '#f8fafc',
        cream: '#fff7ed',
        slate,
        amber,
        amberLight: '#fff7ed',
        'amber-deep': '#d97706',
        emerald,
        emeraldLight: '#ecfdf5',
        sky,
        skyLight: '#f0f9ff',
        rose,
        violet,
        stone,
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'Plus Jakarta Sans', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
        serif: ['var(--font-serif)', 'Literata', 'Georgia', 'Cambria', 'Times New Roman', 'serif'],
      },
      borderRadius: {
        '4xl': '2.5rem',
      },
    },
  },
  plugins: [],
}
