"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function EmotionsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/emotions/activities").then(setData);
  }, []);
  return (
    <AppShell title="Emotional awareness">
      <p className="text-sm text-slate-600">{data?.disclaimer}</p>
      <div className="mt-4 space-y-3">
        {data?.activities?.map((item: any) => (
          <article key={item.slug} className="card">
            <h2 className="font-display text-xl">{item.title}</h2>
            <p className="text-sm text-slate-500">{item.minutes} minutes</p>
            <p className="mt-2">{item.prompt}</p>
          </article>
        ))}
      </div>
    </AppShell>
  );
}
