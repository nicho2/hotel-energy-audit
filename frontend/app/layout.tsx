import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { AppProvider } from "@/providers/app-provider";

export const metadata: Metadata = {
  title: "Hotel Energy Audit",
  description: "MVP de pre-audit energetique et de comparaison de scenarios.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className="app-body">
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}
