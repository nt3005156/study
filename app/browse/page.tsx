import { Breadcrumbs } from '@/components/Breadcrumbs';
import { MindMap } from '@/components/MindMap';
import { CLASS_NODES } from '@/lib/classes';

export const metadata = { title: 'Browse Materials — Choose Your Class | study.companion', description: 'Browse study materials by class from Class 6 to Class 12.' };

export default function BrowsePage() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials' }]} />
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-20 pt-8">
        <div className="text-center mb-4">
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.2em] text-amber-deep">
            Class 6–12 · Computer Science
          </p>
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-4">Browse Materials</h1>
          <p className="text-stone text-lg">Seven grades, one map — click a number to open its chapters.</p>
        </div>
        <MindMap nodes={CLASS_NODES} />
      </section>
    </>
  );
}
