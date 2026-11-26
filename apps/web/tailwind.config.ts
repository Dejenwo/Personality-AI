import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        navy: "#101828",
        indigo: {
          DEFAULT: "#6366F1",
          50: "#EEF2FF",
          100: "#E0E7FF",
        },
        teal: "#14B8A6",
        lavender: "#EDE9FE",
        paper: "#F8FAFC",
        ink: "#0F172A",
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        sans: ["Outfit", "system-ui", "sans-serif"],
      },
      boxShadow: {
        lift: "0 24px 60px -28px rgba(15, 23, 42, 0.45)",
      },
    },
  },
  plugins: [],
};

export default config;
