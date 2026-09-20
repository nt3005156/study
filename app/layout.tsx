import type { Metadata } from 'next';
import { Plus_Jakarta_Sans, Literata } from 'next/font/google';
import './globals.css';
import { Header } from '@/components/Header';

// Plus Jakarta Sans = UI + body text, Literata = headings. Both self-hosted by
// next/font at build time, so the site never depends on a font CDN at runtime.
const jakarta = Plus_Jakarta_Sans({ subsets: ['latin'], display: 'swap', variable: '--font-sans' });
const literata = Literata({ subsets: ['latin'], display: 'swap', variable: '--font-serif' });

export const metadata: Metadata = {
  title: 'study.companion — Smart Digital Study Materials for Class 6 to 12',
  description: 'Learn smarter. Understand better. Search and browse study materials, concepts, questions and diagrams for Computer Science (Class 6–12).',
  openGraph: { title: 'study.companion — Digital Study Materials', type: 'website', locale: 'en_NP' },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${jakarta.variable} ${literata.variable}`}>
      <body className="min-h-screen bg-paper text-ink antialiased flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
}
