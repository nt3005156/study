import type { ClassNode } from '@/lib/classes';

const CX = 400;
const CY = 300;
const RX = 290;
const RY = 208;

function point(i: number, total: number, rx: number, ry: number) {
  const a = ((-90 + (i * 360) / total) * Math.PI) / 180;
  return { x: CX + rx * Math.cos(a), y: CY + ry * Math.sin(a) };
}

/**
 * Interactive mind-map / spider-web of Class 6–12. Pure SVG + links: every
 * node is a real anchor (keyboard accessible, no JS needed) with CSS hover
 * glow and a staggered draw-in entrance. Nodes show the grade number only.
 */
export function MindMap({ nodes }: { nodes: ClassNode[] }) {
  const total = nodes.length;
  const outer = nodes.map((_, i) => point(i, total, RX, RY));
  const inner = nodes.map((_, i) => point(i, total, RX / 2, RY / 2));
  const ring = outer.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

  return (
    <svg
      viewBox="0 0 800 600"
      role="img"
      aria-label={`Mind map of study materials: ${nodes.map((n) => `Class ${n.n}`).join(', ')}`}
      className="mx-auto h-auto w-full max-w-3xl"
    >
      <defs>
        <radialGradient id="mindmap-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.10" />
          <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse cx={CX} cy={CY} rx={350} ry={270} fill="url(#mindmap-glow)" />

      {/* web rings */}
      <ellipse cx={CX} cy={CY} rx={RX / 2} ry={RY / 2} fill="none" className="stroke-amber/25" strokeWidth={1.25} />
      <ellipse cx={CX} cy={CY} rx={RX} ry={RY} fill="none" className="stroke-amber/30" strokeWidth={1.25} />
      <polygon points={ring} fill="none" pathLength={1} className="mindmap-draw stroke-amber/45" strokeWidth={1.25} style={{ animationDelay: '0.5s' }} />

      {/* spokes + web dots, converging on a bare centre point */}
      {outer.map((p, i) => (
        <g key={`spoke-${nodes[i].n}`}>
          <line
            x1={CX} y1={CY} x2={p.x} y2={p.y}
            pathLength={1}
            className="mindmap-draw stroke-amber/35"
            strokeWidth={1.5}
            style={{ animationDelay: `${0.15 + i * 0.08}s` }}
          />
          <circle cx={inner[i].x} cy={inner[i].y} r={3.5} className="fill-amber/50" />
        </g>
      ))}
      <circle cx={CX} cy={CY} r={4} className="fill-amber/70" />

      {/* class nodes: grade number only */}
      {nodes.map((node, i) => {
        const p = outer[i];
        return (
          <a
            key={node.n}
            href={node.href}
            aria-label={`Class ${node.n} Computer Science — ${node.chapters} chapters`}
            className="group outline-none"
          >
            <title>{`Class ${node.n}`}</title>
            <g className="mindmap-fade" style={{ animationDelay: `${0.3 + i * 0.08}s` }}>
              <g className="transition-transform duration-200 [transform-box:fill-box] [transform-origin:center] group-hover:scale-110 group-focus-visible:scale-110">
                <circle cx={p.x} cy={p.y} r={60} fill="none" className="stroke-amber-100 transition group-hover:stroke-amber-300 group-focus-visible:stroke-amber-300" strokeWidth={1.5} />
                <circle cx={p.x} cy={p.y} r={52} className="fill-white stroke-amber-200 transition group-hover:fill-amber-50 group-hover:stroke-amber group-hover:drop-shadow-[0_10px_24px_rgba(217,119,6,0.28)] group-focus-visible:fill-amber-50 group-focus-visible:stroke-amber" strokeWidth={2.5} />
                <text x={p.x} y={p.y + 12} textAnchor="middle" className="fill-ink font-serif" fontSize={34} fontWeight={800}>
                  {node.n}
                </text>
              </g>
            </g>
          </a>
        );
      })}
    </svg>
  );
}
