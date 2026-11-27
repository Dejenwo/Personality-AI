"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CareerGuidancePage() {
  const [items, setItems] = useState<any[]>([]);
  const [q, setQ] = useState("");
  const [riasec, setRiasec] = useState("");
  const [explore, setExplore] = useState<any>(null);
  async function load() {
    const data = await api<{ items: any[] }>(`/api/v1/life/occupations?q=${encodeURIComponent(q)}&riasec=${encodeURIComponent(riasec)}`);
    setItems(data.items);
  }
  useEffect(() => {
    load().catch(() => undefined);
  }, []);
  return (
    <AppShell title="Career intelligence">
      <p className="max-w-2xl text-slate-600">
        Occupations are public O*NET titles. Wages are not stored here — follow the BLS link. Personality type is not
        used to exclude careers.
      </p>
      <div className="mt-4 flex flex-wrap gap-2">
        <input className="rounded border px-3 py-2" placeholder="Search title" value={q} onChange={(e) => setQ(e.target.value)} />
        <input className="rounded border px-3 py-2" placeholder="RIASEC letter e.g. I" value={riasec} onChange={(e) => setRiasec(e.target.value)} />
        <button className="btn-secondary" onClick={() => load()}>Search</button>
        <button
          className="btn-primary"
          onClick={async () => {
            const result = await api("/api/v1/life/career/explore", {
              method: "POST",
              body: JSON.stringify({ riasec: riasec ? [riasec] : ["I", "S"], skills: [] }),
            });
            setExplore(result);
          }}
        >
          Explore from interests
        </button>
      </div>
      {explore ? <p className="mt-4 text-sm text-slate-600">{explore.why}</p> : null}
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {(explore?.primary || items).map((job: any) => (
          <article key={job.slug} className="card">
            <h2 className="font-display text-xl">{job.title}</h2>
            <p className="mt-2 text-slate-600">{job.summary}</p>
            <p className="mt-2 text-sm">{job.education}</p>
            <p className="mt-2 text-sm text-slate-500">{job.salary_note}</p>
            <a className="mt-2 inline-block text-indigo" href={job.source_url} target="_blank" rel="noreferrer">
              O*NET source
            </a>
          </article>
        ))}
      </div>
      <Link className="btn-secondary mt-6" href="/app/assessments/career-interests">Career interests assessment</Link>
    </AppShell>
  );
}
