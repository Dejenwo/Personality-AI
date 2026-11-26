"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Progress analytics">
      <div className="card max-w-3xl">
        <p>Track programs, habits, and goals without shame-based streaks.</p>
        <div className="mt-4 flex gap-3"><Link className="btn-secondary" href="/app/habits">Habits</Link><Link className="btn-secondary" href="/app/goals">Goals</Link></div>
      </div>
    </AppShell>
  );
}
