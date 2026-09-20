import { SearchBox } from '@/components/SearchBox';
import { MindMap } from '@/components/MindMap';
import { CLASS_NODES } from '@/lib/classes';

export default function HomePage() {
  return (
    <>
      {/* Minimal hero */}
      <section aria-label="Welcome" className="relative overflow-hidden bg-gradient-to-b from-amberLight via-paper to-paper">
        <div aria-hidden="true" className="absolute top-[-12%] right-[-8%] w-[520px] h-[520px] rounded-full bg-amber/10 blur-3xl" />
        <div aria-hidden="true" className="absolute bottom-[-8%] left-[-6%] w-[420px] h-[420px] rounded-full bg-sky/10 blur-3xl" />
        <div className="relative mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-14 pb-10 text-center">
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-amber-deep">
            Class 6–12 · Computer Science
          </p>
          <h1 className="font-serif text-4xl sm:text-5xl font-bold tracking-tight text-ink mb-4">
            What do you want to learn today?
          </h1>
          <p className="text-stone text-lg mb-8 max-w-xl mx-auto">
            Search any chapter, concept or question — or explore the map below.
          </p>
          <div className="max-w-xl mx-auto">
            <SearchBox size="lg" />
          </div>
        </div>
      </section>

      {/* Browse Materials mind map */}
      <section aria-label="Browse Materials" className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pt-4 pb-20">
        <div className="text-center mb-2">
          <h2 className="font-serif text-3xl sm:text-4xl font-bold text-ink tracking-tight mb-3">Browse Materials</h2>
          <p className="text-stone text-lg">Click a class to open its chapters.</p>
        </div>
        <MindMap nodes={CLASS_NODES} />
      </section>
    </>
  );
}
