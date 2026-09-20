'use client';

/**
 * Textbook figure with a graceful offline fallback.
 *
 * The figure JPEGs live in public/figures/ (gitignored by design — see
 * SETUP.md), so a fresh clone or a git-based deploy may not have them. Instead
 * of a broken-image icon, readers get a styled placeholder carrying the
 * caption, so the page still reads as a complete textbook.
 */

import { useState } from 'react';
import { ImageOff } from 'lucide-react';

export function FigureImage({
  src,
  alt,
  width,
  variant = 'full',
}: {
  src?: string;
  alt?: string;
  width?: number;
  variant?: 'full' | 'thumb';
}) {
  const [failed, setFailed] = useState(false);

  if (!src || failed) {
    if (variant === 'thumb') {
      return (
        <div
          role="img"
          aria-label={alt || 'Figure unavailable'}
          className="flex h-32 w-full flex-col items-center justify-center gap-1 bg-slate-50 p-3 text-center"
        >
          <ImageOff size={20} className="text-slate-300" />
          <p className="text-xs font-semibold text-stone line-clamp-2">{alt || 'Figure'}</p>
          <p className="text-[10px] text-slate-400">Image file not included in this copy</p>
        </div>
      );
    }
    return (
      <div
        role="img"
        aria-label={alt || 'Figure unavailable'}
        className="flex w-full flex-col items-center justify-center gap-2 rounded-lg border border-dashed border-slate-300 bg-slate-50 px-6 py-10 text-center"
      >
        <ImageOff size={28} className="text-slate-300" />
        <p className="max-w-md text-sm font-semibold text-ink">{alt || 'Figure'}</p>
        <p className="max-w-md text-xs leading-relaxed text-stone">
          The textbook illustration for this section is not included in this copy of the
          site. The notes and questions below it are complete.
        </p>
      </div>
    );
  }

  if (variant === 'thumb') {
    return (
      /* eslint-disable-next-line @next/next/no-img-element */
      <img
        src={src}
        alt={alt || 'Textbook figure'}
        className="h-32 w-full object-contain bg-slate-50 p-2"
        loading="lazy"
        onError={() => setFailed(true)}
      />
    );
  }

  return (
    /* eslint-disable-next-line @next/next/no-img-element */
    <img
      src={src}
      alt={alt || 'Textbook figure'}
      width={width || 720}
      className="h-auto w-full max-w-full rounded-lg border border-slate-200 bg-white object-contain"
      loading="lazy"
      onError={() => setFailed(true)}
    />
  );
}

export default FigureImage;
