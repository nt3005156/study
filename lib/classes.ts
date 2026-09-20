import c6 from '@/content/class-6-computer-science.json';
import c7 from '@/content/class-7-computer-science.json';
import c8 from '@/content/class-8-computer-science.json';
import c9 from '@/content/class-9-computer-science.json';
import c10 from '@/content/class-10-computer-science.json';
import c11 from '@/content/class-11-computer-science.json';
import c12 from '@/content/class-12-computer-science.json';

export type ClassNode = { n: number; chapters: number; href: string };

const books = [c6, c7, c8, c9, c10, c11, c12];

/** Class 6–12 with live chapter counts; links go straight to each subject. */
export const CLASS_NODES: ClassNode[] = books.map((book) => {
  const n = (book as { class?: number }).class ?? 0;
  const chapters = (book as { units?: unknown[] }).units?.length ?? 0;
  return { n, chapters, href: `/class-${n}/computer-science` };
});

export const TOTAL_CHAPTERS = CLASS_NODES.reduce((acc, c) => acc + c.chapters, 0);
