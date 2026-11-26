"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Customer support">
      <div className="card max-w-3xl">
        <p>Production support will use a ticketing provider. Until then, send product feedback.</p>
        <Link className="btn-primary mt-4" href="/app/feedback">Feedback</Link>
      </div>
    </AppShell>
  );
}
