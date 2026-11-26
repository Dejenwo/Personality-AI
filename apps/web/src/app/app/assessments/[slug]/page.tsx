"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Instrument = {
  slug: string;
  name: string;
  description: string;
  instructions: string;
  duration_minutes: number;
  item_count: number;
  scientific: Record<string, unknown>;
};

export default function AssessmentIntroPage() {
  const { slug } = useParams<{ slug: string }>();
  const router = useRouter();
  const [item, setItem] = useState<Instrument | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api<Instrument>(`/api/v1/assessments/${slug}`)
      .then(setItem)
      .catch((err) => setError(err.message));
  }, [slug]);

  async function start() {
    const session = await api<{ id: string }>(`/api/v1/assessments/${slug}/sessions`, { method: "POST" });
    router.push(`/app/assessments/${slug}/take?session=${session.id}`);
  }

  return (
    <AppShell>
      {error ? <ErrorState message={error} /> : null}
      {!item && !error ? <Loading /> : null}
      {item ? (
        <div className="card max-w-3xl">
          <p className="text-sm text-teal">Assessment introduction</p>
          <h1 className="font-display mt-2 text-4xl">{item.name}</h1>
          <p className="mt-4 text-slate-600">{item.description}</p>
          <p className="mt-4">{item.instructions}</p>
          <p className="mt-4 text-sm text-slate-500">
            {item.duration_minutes} minutes · {item.item_count} statements · you can resume if you leave.
          </p>
          <pre className="mt-4 overflow-auto rounded-2xl bg-slate-50 p-4 text-xs dark:bg-slate-950">
            {JSON.stringify(item.scientific, null, 2)}
          </pre>
          <div className="mt-6 flex gap-3">
            <button className="btn-primary" onClick={start}>
              Begin or resume
            </button>
            <Link className="btn-secondary" href="/app/discover">
              Back to marketplace
            </Link>
          </div>
        </div>
      ) : null}
    </AppShell>
  );
}
