import { Breadcrumbs } from '@/components/Breadcrumbs';
import { MindMap } from '@/components/MindMap';
import { CLASS_NODES } from '@/lib/classes';

export const metadata = { title: 'Browse Materials — Choose Your Class | study.companion', description: 'Browse study materials by class from Class 6 to Class 12.' };

export default function BrowsePage() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials' }]} />
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-20 pt-4">
        <div className="text-center mb-2">
          <h1 className="font-serif text-4xl sm:text-5xl font-bold text-ink tracking-tight mb-4">Browse Materials</h1>
          <p className="text-stone text-lg">Click a class to open its chapters.</p>
        </div>
        <MindMap nodes={CLASS_NODES} />
      </section>
    </>
  );
}
