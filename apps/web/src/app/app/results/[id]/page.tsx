"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { BarChart } from "@/components/BarChart";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";
import { traitColor } from "@/lib/format";

export default function ResultPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api<any>(`/api/v1/results/${id}`)
      .then(setData)
      .catch((err) => setError(err.message));
  }, [id]);
  if (error) return <AppShell title="Results"><ErrorState message={error} /></AppShell>;
  if (!data) return <AppShell title="Results"><Loading /></AppShell>;
  const payload = data.payload;
  const traits = Object.values(payload.trait_scores || {}) as any[];
  return (
    <AppShell title="Personality results">
      <p className="text-slate-500">Instrument {payload.instrument_slug} v{payload.instrument_version}</p>
      <h2 className="font-display mt-4 text-4xl">{payload.archetype?.name}</h2>
      <p className="mt-2 max-w-3xl">{payload.archetype?.description}</p>
      <div className="card mt-6">
        <BarChart items={traits.map((t) => ({ label: t.name, value: t.scaled_0_100, color: traitColor(t.trait) }))} />
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link className="btn-secondary" href={`/app/traits/${traits[0]?.trait || "openness"}`}>Trait details</Link>
        <Link className="btn-secondary" href="/app/coach">Ask the coach</Link>
        <Link className="btn-secondary" href="/app/reports">Reports</Link>
      </div>
    </AppShell>
  );
}
