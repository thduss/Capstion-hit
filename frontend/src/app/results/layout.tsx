// src/app/layout.js
import '../../styles/globals.css';

export const metadata = {
  title: 'My Shop',
  description: 'Shop your favorite items',
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="kor">
      <body>{children}</body>
    </html>
  );
}