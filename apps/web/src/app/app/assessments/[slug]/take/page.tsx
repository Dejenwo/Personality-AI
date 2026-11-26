"use client";

import { useParams, useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Instrument = {
  items: { id: string; text: string }[];
  scale: { value: number; label: string }[];
  name: string;
};

type Session = {
  id: string;
  status: string;
  answered: number;
  item_count: number;
  responses: Record<string, number>;
  result_id?: string;
};

function TakeInner() {
  const { slug } = useParams<{ slug: string }>();
  const search = useSearchParams();
  const router = useRouter();
  const [instrument, setInstrument] = useState<Instrument | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [index, setIndex] = useState(0);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const inst = await api<Instrument>(`/api/v1/assessments/${slug}`);
        setInstrument(inst);
        const sessionId = search.get("session");
        const sess = sessionId
          ? await api<Session>(`/api/v1/sessions/${sessionId}`)
          : await api<Session>(`/api/v1/assessments/${slug}/sessions`, { method: "POST" });
        setSession(sess);
        const firstUnanswered = inst.items.findIndex((item) => sess.responses[item.id] == null);
        setIndex(firstUnanswered >= 0 ? firstUnanswered : 0);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load assessment");
      }
    }
    load();
  }, [slug, search]);

  const current = instrument?.items[index];
  const progress = useMemo(() => {
    if (!instrument || !session) return 0;
    return Math.round((Object.keys(session.responses).length / instrument.items.length) * 100);
  }, [instrument, session]);

  async function choose(value: number) {
    if (!session || !current || !instrument) return;
    setSaving(true);
    try {
      const last = index === instrument.items.length - 1;
      const updated = await api<{ id?: string; result?: { id: string }; status?: string; responses?: Record<string, number> }>(
        `/api/v1/sessions/${session.id}/responses`,
        {
          method: "POST",
          body: JSON.stringify({ responses: [{ item_id: current.id, value }], complete: last }),
        }
      );
      if (updated.result?.id) {
        router.push(`/app/assessments/${slug}/complete?result=${updated.result.id}`);
        return;
      }
      const responses = { ...(session.responses || {}), [current.id]: value, ...(updated.responses || {}) };
      setSession({ ...session, responses, answered: Object.keys(responses).length });
      setIndex((i) => Math.min(i + 1, instrument.items.length - 1));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  if (error) {
    return (
      <AppShell title="Assessment">
        <ErrorState message={error} />
      </AppShell>
    );
  }
  if (!instrument || !session || !current) {
    return (
      <AppShell title="Assessment">
        <Loading label="Loading questionnaire" />
      </AppShell>
    );
  }

  return (
    <AppShell>
      <p className="text-sm text-slate-500">
        {instrument.name} · question {index + 1} of {instrument.items.length}
      </p>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200" aria-label="Assessment progress">
        <div className="h-full bg-indigo" style={{ width: `${progress}%` }} />
      </div>
      <div className="card mt-6">
        <h1 className="font-display text-3xl">{current.text}</h1>
        <div className="mt-6 grid gap-2">
          {instrument.scale.map((option) => (
            <button
              key={option.value}
              className={`rounded-2xl border px-4 py-3 text-left min-h-12 ${
                session.responses[current.id] === option.value ? "border-indigo bg-indigo-50" : "border-slate-200"
              }`}
              onClick={() => choose(option.value)}
              disabled={saving}
            >
              {option.label}
            </button>
          ))}
        </div>
        <div className="mt-6 flex justify-between">
          <button className="btn-secondary" disabled={index === 0} onClick={() => setIndex((i) => Math.max(0, i - 1))}>
            Back
          </button>
          <span className="text-sm text-slate-500">{saving ? "Saving…" : "Answers save as you go"}</span>
        </div>
      </div>
    </AppShell>
  );
}

export default function TakePage() {
  return (
    <Suspense fallback={<AppShell title="Assessment"><Loading /></AppShell>}>
      <TakeInner />
    </Suspense>
  );
}
