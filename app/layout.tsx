import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import HomeLink from "./components/HomeLink";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Commit Store Assistant",
  description: "The e-commerce assistant for your Store",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-secondary`}>
        <HomeLink />
        {children}
      </body>
    </html>
  );
}
