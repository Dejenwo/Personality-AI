"use client";

export function BarChart({
  items,
}: {
  items: { label: string; value: number; color?: string }[];
}) {
  return (
    <div className="space-y-3" role="img" aria-label="Trait bar chart">
      {items.map((item) => (
        <div key={item.label}>
          <div className="mb-1 flex justify-between text-sm">
            <span>{item.label}</span>
            <span className="tabular-nums text-slate-500">{Math.round(item.value)}</span>
          </div>
          <div className="h-2.5 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
            <div
              className="h-full rounded-full"
              style={{ width: `${Math.max(4, Math.min(100, item.value))}%`, background: item.color || "#6366F1" }}
            />
          </div>
        </div>
      ))}
      <p className="text-xs text-slate-500">0–100 values are min-max scaled raw sums, not population percentiles.</p>
    </div>
  );
}
