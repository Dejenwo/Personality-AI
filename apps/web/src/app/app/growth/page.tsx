"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function GrowthPage() {
  const [programs, setPrograms] = useState<any[]>([]);
  const [habits, setHabits] = useState<any[]>([]);
  const [goals, setGoals] = useState<any[]>([]);
  useEffect(() => {
    api<any[]>("/api/v1/growth/programs").then(setPrograms);
    api<any[]>("/api/v1/habits").then(setHabits);
    api<any[]>("/api/v1/goals").then(setGoals);
  }, []);
  return (
    <AppShell title="My Growth">
      <div className="grid gap-4 md:grid-cols-3">
        <Link className="card" href="/app/habits">Habits · {habits.length}</Link>
        <Link className="card" href="/app/goals">Goals · {goals.length}</Link>
        <Link className="card" href="/app/journal">Journal</Link>
        <Link className="card" href="/app/blueprint">Life Blueprint</Link>
        <Link className="card" href="/app/encyclopedia">Encyclopedia</Link>
        <Link className="card" href="/app/profile">Profile and privacy</Link>
      </div>
      <h2 className="font-display mt-8 text-2xl">Development academy</h2>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        {programs.map((program) => (
          <Link key={program.slug} href={`/app/programs/${program.slug}`} className="card block">
            <h3 className="font-display text-xl">{program.name}</h3>
            <p className="mt-2 text-slate-600">{program.summary}</p>
            <p className="mt-2 text-sm text-slate-500">{program.days} days · {program.category}</p>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
