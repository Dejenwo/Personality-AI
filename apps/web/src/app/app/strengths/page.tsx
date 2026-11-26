"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Strengths">
      <div className="card max-w-3xl">
        <p>Strengths are hypotheses from your scores and self-reflection, not a ranked talent list.</p>
        <Link className="btn-primary mt-4" href="/app/assessments/strengths">Strengths reflection</Link>
      </div>
    </AppShell>
  );
}
