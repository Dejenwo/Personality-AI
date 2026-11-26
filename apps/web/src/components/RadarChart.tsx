"use client";

type Point = { label: string; value: number; color?: string };

export function RadarChart({ points }: { points: Point[] }) {
  const size = 280;
  const cx = size / 2;
  const cy = size / 2;
  const radius = 96;
  const n = points.length || 1;
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const coord = (i: number, value: number) => {
    const r = (Math.max(0, Math.min(100, value)) / 100) * radius;
    return [cx + r * Math.cos(angle(i)), cy + r * Math.sin(angle(i))];
  };
  const polygon = points
    .map((_, i) => coord(i, points[i].value).join(","))
    .join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} role="img" aria-label="Big Five trait radar chart" className="w-full max-w-sm">
      {[0.25, 0.5, 0.75, 1].map((scale) => (
        <polygon
          key={scale}
          fill="none"
          stroke="currentColor"
          className="text-slate-200 dark:text-slate-700"
          points={points
            .map((_, i) => {
              const r = radius * scale;
              return `${cx + r * Math.cos(angle(i))},${cy + r * Math.sin(angle(i))}`;
            })
            .join(" ")}
        />
      ))}
      {points.map((_, i) => {
        const [x, y] = coord(i, 100);
        return <line key={i} x1={cx} y1={cy} x2={x} y2={y} className="stroke-slate-200 dark:stroke-slate-700" />;
      })}
      <polygon points={polygon} fill="rgba(99,102,241,0.28)" stroke="#6366F1" strokeWidth="2" />
      {points.map((point, i) => {
        const [x, y] = coord(i, point.value);
        const [lx, ly] = coord(i, 118);
        return (
          <g key={point.label}>
            <circle cx={x} cy={y} r="4" fill={point.color || "#6366F1"} />
            <text x={lx} y={ly} textAnchor="middle" className="fill-slate-600 dark:fill-slate-300" fontSize="10">
              {point.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
