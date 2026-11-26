"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ComparisonPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/relationships/${id}/comparison`).then(setData).catch(() => setData({ error: "Accept the invitation first." }));
  }, [id]);
  if (!data) return <AppShell title="Comparison"><p>Loading…</p></AppShell>;
  if (data.error) return <AppShell title="Comparison"><p>{data.error}</p></AppShell>;
  return (
    <AppShell title="Personality comparison">
      <p className="text-sm text-slate-600">{data.disclaimer}</p>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="card">
          <h2>You</h2>
          <p>{data.me?.payload?.archetype?.name || "No profile yet"}</p>
        </div>
        <div className="card">
          <h2>The other person</h2>
          <p>{data.other?.payload?.archetype?.name || "Waiting for their assessment"}</p>
        </div>
      </div>
      <h2 className="mt-6 font-semibold">Discussion prompts</h2>
      <ul className="list-disc pl-5">{data.prompts?.map((p: string) => <li key={p}>{p}</li>)}</ul>
    </AppShell>
  );
}
