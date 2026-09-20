import Link from 'next/link';
import { SearchBox } from '@/components/SearchBox';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-xl border-b border-slate-100 no-print">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        <Link href="/" className="shrink-0 text-lg font-extrabold tracking-tight text-ink" aria-label="study.companion home">
          study<span className="text-amber-deep">.companion</span>
        </Link>
        <div className="min-w-0 flex-1 sm:flex-none sm:w-80">
          <SearchBox size="sm" />
        </div>
      </div>
    </header>
  );
}
