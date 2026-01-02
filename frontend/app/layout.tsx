import type { Metadata } from "next";
import { Poppins, Lavishly_Yours } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/components/auth/AuthProvider";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-poppins",
});

const lavishlyYours = Lavishly_Yours({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-lavishly-yours",
});

export const metadata: Metadata = {
  title: "Evolution of Todo",
  description: "Your personal task management solution",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${poppins.variable} ${lavishlyYours.variable} font-sans antialiased`}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
