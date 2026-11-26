"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Communication insights">
      <div className="card max-w-3xl">
        <p>Use the Communication Preferences assessment in Discover. Results describe habits, not social skill.</p>
        <Link className="btn-primary mt-4" href="/app/assessments/communication">Open assessment</Link>
      </div>
    </AppShell>
  );
}
