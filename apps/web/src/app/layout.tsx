import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PersonalityDNA AI — Discover Yourself. Understand Others. Transform Your Life.",
  description:
    "An AI-powered personality intelligence platform grounded in the Big Five, original archetypes, and a continuous development practice. Educational, not clinical.",
  applicationName: "PersonalityDNA AI",
  keywords: ["personality", "Big Five", "personal development", "AI coach"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Outfit:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="dna-grid min-h-screen">{children}</body>
    </html>
  );
}
