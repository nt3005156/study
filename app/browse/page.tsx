import { Breadcrumbs } from '@/components/Breadcrumbs';
import { MindMap } from '@/components/MindMap';
import { CLASS_NODES } from '@/lib/classes';

export const metadata = { title: 'Browse Materials — Choose Your Class | study.companion', description: 'Browse study materials by class from Class 6 to Class 12.' };

export default function BrowsePage() {
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials' }]} center />
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-8 pt-3">
        <div className="text-center mb-1">
          <h1 className="font-serif text-3xl sm:text-4xl font-bold text-ink tracking-tight">Browse Materials</h1>
        </div>
        <MindMap nodes={CLASS_NODES} />
      </section>
    </>
  );
}
