"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { BarChart } from "@/components/BarChart";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";
import { traitColor } from "@/lib/format";

const SECTIONS = [
  { href: "/app/encyclopedia", label: "Who You Are" },
  { href: "/app/guidance", label: "How You Think" },
  { href: "/app/communication", label: "How You Communicate" },
  { href: "/app/strengths", label: "Your Strengths" },
  { href: "/app/guidance", label: "Your Blind Spots" },
  { href: "/app/guidance/career", label: "Your Career" },
  { href: "/app/relationships", label: "Your Relationships" },
  { href: "/app/guidance/marriage", label: "Your Marriage" },
  { href: "/app/guidance/family", label: "Your Family" },
  { href: "/app/guidance/money", label: "Your Money Habits" },
  { href: "/app/leadership", label: "Your Leadership" },
  { href: "/app/guidance/decisions", label: "Your Life Decisions" },
  { href: "/app/growth", label: "Your Growth Journey" },
];

export default function ResultPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [who, setWho] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api<any>(`/api/v1/results/${id}`)
      .then(setData)
      .catch((err) => setError(err.message));
    api("/api/v1/life/who-you-are").then(setWho).catch(() => undefined);
  }, [id]);
  if (error) return <AppShell title="Results"><ErrorState message={error} /></AppShell>;
  if (!data) return <AppShell title="Results"><Loading /></AppShell>;
  const payload = data.payload;
  const traits = Object.values(payload.trait_scores || {}) as any[];
  return (
    <AppShell title="Personal intelligence">
      <p className="text-slate-500">Instrument {payload.instrument_slug} v{payload.instrument_version} · scores are not percentiles</p>
      <h2 className="font-display mt-4 text-4xl">{payload.archetype?.name}</h2>
      {payload.archetype?.preference_code ? (
        <p className="mt-2 text-xl text-indigo">{payload.archetype.preference_code} · {payload.archetype.preference_title}</p>
      ) : null}
      <p className="mt-2 max-w-3xl">{payload.archetype?.description}</p>
      {who?.personalized?.what_may_distinguish_you ? (
        <p className="card mt-4 max-w-3xl">{who.personalized.what_may_distinguish_you}</p>
      ) : null}
      <div className="card mt-6">
        <BarChart items={traits.map((t) => ({ label: t.name, value: t.scaled_0_100, color: traitColor(t.trait) }))} />
      </div>
      <div className="mt-6 grid gap-3 md:grid-cols-2">
        {SECTIONS.map((section) => (
          <Link key={section.label} className="card block" href={section.href}>{section.label}</Link>
        ))}
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link className="btn-secondary" href="/app/blueprint">Life Blueprint</Link>
        <Link className="btn-secondary" href="/app/coach">Ask the coach</Link>
        <Link className="btn-secondary" href="/app/reports">Reports</Link>
      </div>
    </AppShell>
  );
}
