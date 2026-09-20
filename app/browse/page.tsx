import Link from 'next/link';
import { ArrowRight, BookOpen, Monitor } from 'lucide-react';
import { Breadcrumbs } from '@/components/Breadcrumbs';

export const metadata = { title: 'Browse Materials — Choose Your Class | Study Platform', description: 'Browse study materials by class from Class 6 to Class 12.' };

export default function BrowsePage() {
  const classes = [
    { c: 6, name: 'Class 6', desc: 'Essentials of Computer Science — 15 chapters.', subjects: ['Computer Science'], icon: '🎒' },
    { c: 7, name: 'Class 7', desc: 'Essentials of Computer Science — 21 chapters.', subjects: ['Computer Science'], icon: '📘' },
    { c: 8, name: 'Class 8', desc: 'Essentials of Computer Science — 11 chapters, complete course.', subjects: ['Computer Science'], icon: '💻' },
    { c: 9, name: 'Class 9', desc: 'Computer Science — practical oriented.', subjects: ['Computer Science'], icon: '🖥️' },
    { c: 10, name: 'Class 10', desc: 'Computer Science — 5 chapters with detailed notes and figures.', subjects: ['Computer Science'], icon: '🌐' },
    { c: 11, name: 'Class 11', desc: 'Computer Science — 8 chapters with detailed notes and figures.', subjects: ['Computer Science'], icon: '💻' },
    { c: 12, name: 'Class 12', desc: 'Computer Science — 7 chapters, complete course.', subjects: ['Computer Science'], icon: '🎓' },
  ];
  return (
    <>
      <Breadcrumbs items={[{ label: 'Browse Materials' }]} />
      <section className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-6">
        <div className="text-center mb-14">
          <h1 className="font-serif text-4xl sm:text-6xl font-bold text-ink tracking-tight mb-4">Choose Your Class</h1>
          <p className="text-stone text-lg max-w-xl mx-auto">Select your grade to explore verified textbook summaries, concepts, and exercise solutions.</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {classes.map(({ c, name, desc, subjects, icon }) => (
            <Link key={c} href={`/class-${c}`} className="group rounded-3xl bg-white border border-slate-100 p-7 shadow-xl shadow-slate-200/20 hover:shadow-2xl hover:-translate-y-1 transition-all text-center" aria-label={`${name} materials`}>
              <div className="h-16 w-16 mx-auto rounded-2xl bg-gradient-to-br from-amber/90 to-amber-deep text-white flex items-center justify-center text-2xl font-extrabold shadow-lg shadow-amber/20 mb-4 group-hover:scale-110 transition-transform">{icon}</div>
              <h3 className="font-bold text-ink text-lg mb-1">{name}</h3>
              <p className="text-xs text-stone">{desc}</p>
              <span className="mt-4 inline-block text-sm font-semibold text-amber-deep group-hover:underline">View Materials →</span>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
