"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function PurposePage() {
  const [keys, setKeys] = useState<string[]>([]);
  const [rankings, setRankings] = useState<Record<string, number>>({});
  const [result, setResult] = useState<any>(null);
  useEffect(() => {
    api<{ keys: string[] }>("/api/v1/life/values/catalog").then((data) => {
      setKeys(data.keys);
      setRankings(Object.fromEntries(data.keys.map((key, index) => [key, index + 1])));
    });
  }, []);
  return (
    <AppShell title="Values and purpose">
      <p className="max-w-2xl text-slate-600">
        Rank what matters to you. We will not infer faith or politics from a personality code.
      </p>
      <form
        className="mt-6 space-y-2"
        onSubmit={async (event) => {
          event.preventDefault();
          setResult(await api("/api/v1/life/values", { method: "POST", body: JSON.stringify({ rankings }) }));
        }}
      >
        {keys.map((key) => (
          <label key={key} className="flex items-center justify-between gap-4">
            <span>{key.replaceAll("_", " ")}</span>
            <input
              type="number"
              min={1}
              max={20}
              className="w-20 rounded border px-2 py-1"
              value={rankings[key] || 1}
              onChange={(e) => setRankings({ ...rankings, [key]: Number(e.target.value) })}
            />
          </label>
        ))}
        <button className="btn-primary mt-4" type="submit">Save ranking</button>
      </form>
      {result ? (
        <div className="card mt-6">
          <p>{result.mission_draft}</p>
          <p className="mt-2 text-sm text-slate-500">{result.disclaimer}</p>
        </div>
      ) : null}
    </AppShell>
  );
}
