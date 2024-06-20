import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      boxShadow: {
        'custom-gray': '0 10px 20px rgba(209, 213, 219, 0.5)'
      },
      fontFamily: {
        sans: ['GangwonEdu_OTFBoldA', 'cursive'],
      },
      colors: {
        customYellow: '#FFF0CE',
        customNavy: '#FFCD4A',
      },
    },
  },
  plugins: [],
};
export default config;
