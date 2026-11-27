"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function FamilyPage() {
  const [guide, setGuide] = useState<any>(null);
  const [slug, setSlug] = useState("mentor");
  async function load() {
    setGuide(await api(`/api/v1/life/parenting/${slug}`));
  }
  useEffect(() => {
    load().catch(() => undefined);
  }, []);
  return (
    <AppShell title="Parenting and family">
      <p className="max-w-2xl text-slate-600">
        This module is for adults reflecting on their own habits. We do not assign personality types to children
        and we do not infer developmental conditions.
      </p>
      <div className="mt-4 flex gap-2">
        <input className="rounded border px-3 py-2" value={slug} onChange={(e) => setSlug(e.target.value)} />
        <button className="btn-primary" onClick={load}>Load adult profile</button>
      </div>
      {guide ? (
        <div className="card mt-6">
          <h2 className="font-display text-2xl">{guide.adult_profile?.title}</h2>
          <ul className="mt-3 list-disc pl-5">
            {(guide.never || []).map((row: string) => <li key={row}>{row}</li>)}
          </ul>
          <h3 className="mt-4 font-semibold">Exercises</h3>
          <ul className="list-disc pl-5">
            {(guide.exercises || []).map((row: string) => <li key={row}>{row}</li>)}
          </ul>
        </div>
      ) : null}
    </AppShell>
  );
}
