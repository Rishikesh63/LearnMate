import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ReactNode } from "react";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core";

// Load fonts for branding
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Metadata for the site
export const metadata: Metadata = {
  title: "LearnMate - Your Study Assistant",
  description:
    "LearnMate helps you create and manage personalized study plans, track your progress, and get feedback.",
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta property="og:title" content="LearnMate - Your Study Assistant" />
        <meta
          property="og:description"
          content="LearnMate helps you create and manage personalized study plans, track your progress, and get feedback."
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {/* Wrap entire app with CopilotKit context */}
        <CopilotKit publicApiKey="ck_pub_015b2209d137f7554858956ec69b014e">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
