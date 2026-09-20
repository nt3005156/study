import { redirect } from 'next/navigation';

/** Class 8 has a single subject, so its landing page goes straight to it. */
export default function Class8Page() {
  redirect('/class-8/computer-science');
}
