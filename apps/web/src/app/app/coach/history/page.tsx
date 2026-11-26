"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CoachHistory() {
  const [rows, setRows] = useState<any[]>([]);
  useEffect(() => {
    api<any[]>("/api/v1/coach/conversations").then(setRows);
  }, []);
  return (
    <AppShell title="Coaching conversation history">
      <ul className="space-y-3">
        {rows.map((row) => (
          <li key={row.id} className="card">
            <Link href="/app/coach">{row.title}</Link>
          </li>
        ))}
        {rows.length === 0 ? <li>No conversations yet.</li> : null}
      </ul>
    </AppShell>
  );
}
