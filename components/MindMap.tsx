import type { ClassNode } from '@/lib/classes';
import { TOTAL_CHAPTERS } from '@/lib/classes';

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
 * glow and a staggered draw-in entrance.
 */
export function MindMap({ nodes }: { nodes: ClassNode[] }) {
  const total = nodes.length;
  const outer = nodes.map((_, i) => point(i, total, RX, RY));
  const inner = nodes.map((_, i) => point(i, total, RX / 2, RY / 2));
  const ring = outer.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

  return (
    <svg
      viewBox="0 0 800 620"
      role="img"
      aria-label={`Mind map of study materials: ${nodes.map((n) => `Class ${n.n}`).join(', ')}`}
      className="mx-auto h-auto w-full max-w-3xl"
    >
      {/* web rings */}
      <ellipse cx={CX} cy={CY} rx={RX / 2} ry={RY / 2} fill="none" className="stroke-amber/30" strokeWidth={1.5} />
      <ellipse cx={CX} cy={CY} rx={RX} ry={RY} fill="none" className="stroke-amber/40" strokeWidth={1.5} />
      <polygon points={ring} fill="none" pathLength={1} className="mindmap-draw stroke-amber/50" strokeWidth={1.5} style={{ animationDelay: '0.5s' }} />

      {/* spokes + web dots */}
      {outer.map((p, i) => (
        <g key={`spoke-${nodes[i].n}`}>
          <line
            x1={CX} y1={CY} x2={p.x} y2={p.y}
            pathLength={1}
            className="mindmap-draw stroke-amber/40"
            strokeWidth={2}
            style={{ animationDelay: `${0.15 + i * 0.08}s` }}
          />
          <circle cx={inner[i].x} cy={inner[i].y} r={3.5} className="fill-amber/60" />
        </g>
      ))}

      {/* pulsing halo behind the hub */}
      <circle cx={CX} cy={CY} r={72} fill="none" className="mindmap-pulse stroke-amber" strokeWidth={2} />

      {/* hub */}
      <g className="mindmap-fade" style={{ animationDelay: '0.1s' }}>
        <circle cx={CX} cy={CY} r={64} className="fill-ink" />
        <circle cx={CX} cy={CY} r={64} fill="none" className="stroke-amber" strokeWidth={3} />
        <text x={CX} y={CY - 2} textAnchor="middle" className="fill-white" fontSize={17} fontWeight={800}>
          Browse
        </text>
        <text x={CX} y={CY + 18} textAnchor="middle" className="fill-amber" fontSize={13} fontWeight={600}>
          {TOTAL_CHAPTERS} chapters
        </text>
      </g>

      {/* class nodes */}
      {nodes.map((node, i) => {
        const p = outer[i];
        return (
          <a
            key={node.n}
            href={node.href}
            aria-label={`Class ${node.n} Computer Science — ${node.chapters} chapters`}
            className="group outline-none"
          >
            <title>{`Class ${node.n} — ${node.chapters} chapters`}</title>
            <g className="mindmap-fade" style={{ animationDelay: `${0.3 + i * 0.08}s` }}>
              <g className="transition-transform duration-200 [transform-box:fill-box] [transform-origin:center] group-hover:scale-110 group-focus-visible:scale-110">
                <circle cx={p.x} cy={p.y} r={48} className="fill-white stroke-amber-200 transition group-hover:fill-amber-50 group-hover:stroke-amber group-focus-visible:fill-amber-50" strokeWidth={2.5} />
                <text x={p.x} y={p.y + 11} textAnchor="middle" className="fill-ink" fontSize={30} fontWeight={800}>
                  {node.n}
                </text>
              </g>
              <text x={p.x} y={p.y + 74} textAnchor="middle" className="fill-ink transition group-hover:fill-amber-deep" fontSize={15} fontWeight={700}>
                Class {node.n}
              </text>
              <text x={p.x} y={p.y + 92} textAnchor="middle" className="fill-stone" fontSize={12} fontWeight={500}>
                {node.chapters} chapters
              </text>
            </g>
          </a>
        );
      })}
    </svg>
  );
}
