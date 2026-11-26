"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CardPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/personality/card").then(setData);
  }, []);
  return (
    <AppShell title="Shareable personality card">
      <div className="card max-w-md bg-navy text-white">
        <p className="text-teal">{data?.display_name}</p>
        <h2 className="font-display mt-2 text-4xl">{data?.archetype?.name || "Take an assessment first"}</h2>
        <p className="mt-3 text-slate-200">{data?.archetype?.tagline}</p>
      </div>
      <p className="mt-4 text-sm text-slate-500">{data?.disclaimer}</p>
    </AppShell>
  );
}
