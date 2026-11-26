"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { BarChart } from "@/components/BarChart";
import { RadarChart } from "@/components/RadarChart";
import { Empty, ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";
import { traitColor } from "@/lib/format";

type Dashboard = {
  has_profile: boolean;
  insight: string;
  premium: boolean;
  latest: null | {
    id: string;
    payload: {
      archetype?: { name: string; slug: string; tagline: string; mixed?: boolean; description: string };
      secondary_archetype?: { name: string; slug: string; tagline: string };
      trait_scores: Record<string, { name: string; mean: number; scaled_0_100: number; trait: string }>;
      strengths: string[];
      growth_areas: string[];
    };
  };
  history: { id: string; instrument_slug: string; created_at: string; archetype?: string }[];
};

export default function HomeDashboard() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api<Dashboard>("/api/v1/personality/dashboard")
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <AppShell title="Home">
        <ErrorState message={error} />
        <Link className="btn-secondary mt-4" href="/login">
          Log in
        </Link>
      </AppShell>
    );
  }
  if (!data) {
    return (
      <AppShell title="Home">
        <Loading label="Loading your personality dashboard" />
      </AppShell>
    );
  }
  if (!data.has_profile || !data.latest) {
    return (
      <AppShell title="Home">
        <Empty
          title="Your dashboard is ready when you are"
          body="Take the free Big Five assessment to see traits, a primary archetype, and a first set of development suggestions."
          action={
            <Link className="btn-primary" href="/app/discover">
              Open Discover
            </Link>
          }
        />
      </AppShell>
    );
  }

  const payload = data.latest.payload;
  const traits = Object.values(payload.trait_scores || {});
  const radar = traits
    .filter((t) => t.trait !== "negative_emotionality")
    .map((t) => ({ label: t.name.split(" ")[0], value: t.scaled_0_100, color: traitColor(t.trait) }));

  return (
    <AppShell>
      <p className="text-sm uppercase tracking-[0.2em] text-teal">Today</p>
      <h1 className="font-display mt-2 text-4xl">{payload.archetype?.name || "Your profile"}</h1>
      <p className="mt-2 max-w-2xl text-slate-600">{payload.archetype?.tagline}</p>
      {payload.archetype?.mixed ? (
        <p className="mt-2 text-sm text-indigo">Mixed profile — one or more traits were near the midpoint.</p>
      ) : null}

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="font-display text-2xl">Big Five</h2>
          <RadarChart points={radar} />
        </div>
        <div className="card">
          <h2 className="font-display text-2xl">Trait range</h2>
          <BarChart items={traits.map((t) => ({ label: t.name, value: t.scaled_0_100, color: traitColor(t.trait) }))} />
        </div>
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-3">
        <div className="card">
          <h2 className="font-display text-xl">Primary archetype</h2>
          <p className="mt-2">{payload.archetype?.description}</p>
          <Link className="btn-secondary mt-4" href={`/app/archetype/${payload.archetype?.slug || ""}`}>
            Open primary
          </Link>
        </div>
        <div className="card">
          <h2 className="font-display text-xl">Secondary archetype</h2>
          <p className="mt-2">{payload.secondary_archetype?.name}</p>
          <p className="text-slate-600">{payload.secondary_archetype?.tagline}</p>
          <Link className="btn-secondary mt-4" href={`/app/archetype/${payload.secondary_archetype?.slug || ""}`}>
            Open secondary
          </Link>
        </div>
        <div className="card">
          <h2 className="font-display text-xl">Daily insight</h2>
          <p className="mt-2">{data.insight}</p>
          <Link className="btn-secondary mt-4" href="/app/insights">
            More insights
          </Link>
        </div>
      </div>

      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="font-display text-xl">Potential strengths</h2>
          <ul className="mt-3 list-disc pl-5">
            {(payload.strengths || []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <Link className="mt-3 inline-block text-indigo" href="/app/strengths">
            Strengths
          </Link>
        </div>
        <div className="card">
          <h2 className="font-display text-xl">Growth opportunities</h2>
          <ul className="mt-3 list-disc pl-5">
            {(payload.growth_areas || []).map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          <Link className="mt-3 inline-block text-indigo" href="/app/growth">
            Growth
          </Link>
        </div>
      </div>

      <div className="card mt-6">
        <h2 className="font-display text-xl">Assessment history</h2>
        {data.history.length === 0 ? (
          <p className="mt-2 text-slate-500">No history yet.</p>
        ) : (
          <ul className="mt-3 space-y-2">
            {data.history.map((row) => (
              <li key={row.id}>
                <Link href={`/app/results/${row.id}`} className="text-indigo">
                  {row.instrument_slug} · {row.archetype || "profile"} · {new Date(row.created_at).toLocaleString()}
                </Link>
              </li>
            ))}
          </ul>
        )}
      </div>
    </AppShell>
  );
}
