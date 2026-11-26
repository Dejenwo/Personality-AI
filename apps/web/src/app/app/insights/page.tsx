"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function InsightsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/insights/today").then(setData);
  }, []);
  return (
    <AppShell title="Daily insights">
      <div className="card">
        <p className="text-sm text-slate-500">{data?.date}</p>
        <p className="mt-3 text-xl">{data?.insight}</p>
      </div>
    </AppShell>
  );
}
