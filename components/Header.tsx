import Link from 'next/link';
import { SearchBox } from '@/components/SearchBox';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-xl border-b border-slate-100 no-print">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 h-16 grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        <Link href="/" className="justify-self-start text-lg font-extrabold tracking-tight text-ink" aria-label="study.companion home">
          study<span className="text-amber-deep">.companion</span>
        </Link>
        <div className="w-[min(100%,32rem)]">
          <SearchBox size="sm" />
        </div>
        <div aria-hidden="true" />
      </div>
    </header>
  );
}
