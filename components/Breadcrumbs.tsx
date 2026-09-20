'use client';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';

export function Breadcrumbs({ items }: { items: { label: string; href?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-3 no-print">
      <ol className="flex items-center gap-1.5 text-xs sm:text-sm text-stone flex-wrap">
        <li><Link href="/" className="hover:text-ink transition flex items-center gap-1"><Home size={14} /> Home</Link></li>
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-1.5">
            <ChevronRight size={14} className="text-slate-300" />
            {item.href ? <Link href={item.href} className="hover:text-ink transition hover:underline">{item.label}</Link> : <span className="text-ink font-medium">{item.label}</span>}
          </li>
        ))}
      </ol>
    </nav>
  );
}
