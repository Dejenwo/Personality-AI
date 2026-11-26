"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Invitation management">
      <div className="card max-w-3xl">
        <p>Sent and received invitations live with Relationship intelligence.</p>
        <Link className="btn-primary mt-4" href="/app/relationships">Open invitations</Link>
      </div>
    </AppShell>
  );
}
