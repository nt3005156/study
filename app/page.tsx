import Link from 'next/link';

export default function HomePage() {
  return (
    <section aria-label="Welcome" className="relative flex min-h-[calc(100vh-4rem)] flex-col overflow-hidden bg-gradient-to-b from-amberLight via-paper to-paper">
      <div aria-hidden="true" className="absolute top-[-12%] right-[-8%] w-[520px] h-[520px] rounded-full bg-amber/10 blur-3xl" />
      <div aria-hidden="true" className="absolute bottom-[-8%] left-[-6%] w-[420px] h-[420px] rounded-full bg-sky/10 blur-3xl" />
      <div className="relative m-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8 py-16 text-center">
        <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-amber-deep">
          Class 6–12 · Computer Science
        </p>
        <h1 className="font-serif text-4xl sm:text-6xl font-bold tracking-tight text-ink mb-4">
          What do you want to learn today?
        </h1>
        <p className="text-stone text-lg mb-10 max-w-xl mx-auto">
          Search any chapter, concept or question from the bar above — or explore
          every class in the interactive map.
        </p>
        <Link
          href="/browse"
          className="group relative inline-flex items-center gap-3 overflow-hidden rounded-2xl bg-gradient-to-r from-amber to-amber-deep px-10 py-4 text-lg font-bold text-white shadow-[0_20px_50px_-12px_rgba(217,119,6,0.55)] transition-all hover:-translate-y-0.5 hover:shadow-[0_28px_60px_-12px_rgba(217,119,6,0.65)] focus:outline-none focus:ring-4 focus:ring-amber/30"
          aria-label="Browse Materials"
        >
          <span aria-hidden="true" className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/30 to-transparent transition-transform duration-700 ease-out group-hover:translate-x-full" />
          <span className="relative">Browse Materials</span>
        </Link>
      </div>
    </section>
  );
}
