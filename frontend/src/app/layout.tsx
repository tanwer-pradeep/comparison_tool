import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Visual QA Automation",
    description: "Automated Visual Regression Testing Platform",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={cn("min-h-screen bg-background font-sans antialiased", inter.className)}>
                <main className="flex min-h-screen flex-col">
                    {children}
                </main>
            </body>
        </html>
    );
}
