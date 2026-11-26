"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Help center">
      <div className="card max-w-3xl">
        <p>Scoring is deterministic. This product is not therapy. Privacy controls are in settings. Crisis: 988 (US) or iasp.info.</p>
        <Link className="btn-secondary mt-4" href="/legal/privacy">Privacy</Link>
      </div>
    </AppShell>
  );
}
