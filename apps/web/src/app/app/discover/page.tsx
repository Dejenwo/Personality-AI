"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Assessment = {
  slug: string;
  name: string;
  description: string;
  duration_minutes: number;
  item_count: number;
  is_free: boolean;
  locked: boolean;
  category: string;
  scientific?: { validation_status?: string };
};

export default function DiscoverPage() {
  const [items, setItems] = useState<Assessment[] | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api<Assessment[]>("/api/v1/assessments")
      .then(setItems)
      .catch((err) => setError(err.message));
  }, []);
  return (
    <AppShell title="Discover">
      <p className="mb-6 max-w-2xl text-slate-600">
        Each instrument has documented methodology and limitations. Original PersonalityDNA inventories are
        educational until independently validated.
      </p>
      {error ? <ErrorState message={error} /> : null}
      {!items && !error ? <Loading label="Loading assessments" /> : null}
      <div className="grid gap-4 md:grid-cols-2">
        {items?.map((item) => (
          <article key={item.slug} className="card">
            <p className="text-xs uppercase tracking-wide text-teal">{item.category}</p>
            <h2 className="font-display mt-1 text-2xl">{item.name}</h2>
            <p className="mt-2 text-slate-600">{item.description}</p>
            <p className="mt-3 text-sm text-slate-500">
              {item.duration_minutes} min · {item.item_count} items · {item.is_free ? "Free" : "Premium"}
              {item.locked ? " · Locked" : ""}
            </p>
            <p className="mt-1 text-xs text-slate-500">{item.scientific?.validation_status}</p>
            <Link className="btn-primary mt-4" href={`/app/assessments/${item.slug}`}>
              {item.locked ? "View" : "Open"}
            </Link>
          </article>
        ))}
      </div>
    </AppShell>
  );
}
