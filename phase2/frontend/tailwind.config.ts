import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: "class",
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "rgb(0, 240, 255)", // Cyan
                "primary-dark": "rgb(0, 184, 196)",
                "background-dark": "rgb(10, 13, 20)",
                "surface-dark": "rgba(18, 24, 34, 0.2)",
                "border-grid": "rgba(0, 240, 255, 0.1)",
                "border-subtle": "rgba(255, 255, 255, 0.05)",
                "text-light": "rgb(176, 192, 208)",
                "text-dark": "rgb(112, 128, 144)",
                "node-bg": "rgba(0, 240, 255, 0.05)",
                "node-border": "rgba(0, 240, 255, 0.3)",
            },
            fontFamily: {
                display: ["'Space Grotesk'", "sans-serif"],
                body: ["'Space Grotesk'", "sans-serif"],
                mono: ["'Courier New'", "monospace"],
            },
            boxShadow: {
                "glow-sm": "0 0 5px rgba(0, 240, 255, 0.2)",
                "glow-md": "0 0 15px rgba(0, 240, 255, 0.3)",
                "glow-lg": "0 0 25px rgba(0, 240, 255, 0.4)",
                "glow-urgent": "0 0 10px rgba(255, 0, 100, 0.8)",
                "glow-high": "0 0 8px rgba(255, 165, 0, 0.6)",
                "glow-medium": "0 0 8px rgba(0, 200, 255, 0.6)",
                "glow-low": "0 0 8px rgba(0, 255, 0, 0.6)",
            },
            animation: {
                "glow-pulse": "glow-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
                "node-sparkle": "node-sparkle 3s ease-in-out infinite",
                flow: "flow 10s linear infinite",
            },
            keyframes: {
                "glow-pulse": {
                    "0%, 100%": {
                        opacity: "0.8",
                        transform: "scale(1)",
                        boxShadow: "0 0 5px rgba(0, 240, 255, 0.6)",
                    },
                    "50%": {
                        opacity: "1",
                        transform: "scale(1.05)",
                        boxShadow: "0 0 10px rgba(0, 240, 255, 0.8), 0 0 20px rgba(0, 240, 255, 0.6)",
                    },
                },
                "node-sparkle": {
                    "0%, 100%": { opacity: "0.8", transform: "scale(1)" },
                    "50%": { opacity: "1", transform: "scale(1.02)" },
                },
                flow: {
                    "0%": { backgroundPosition: "0% 0%" },
                    "100%": { backgroundPosition: "100% 100%" },
                },
            },
        },
    },
    plugins: [],
};

export default config;
