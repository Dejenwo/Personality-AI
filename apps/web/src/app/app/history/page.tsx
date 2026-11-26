"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Assessment history">
      <div className="card max-w-3xl">
        <p>Completed instruments appear on Home after you take them.</p>
        <Link className="btn-primary mt-4" href="/app">Back to dashboard</Link>
      </div>
    </AppShell>
  );
}
