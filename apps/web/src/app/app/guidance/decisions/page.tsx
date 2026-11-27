"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

const CRITERIA = [
  "financial_stability",
  "personal_fulfillment",
  "family_considerations",
  "professional_growth",
  "risk",
];

export default function DecisionsPage() {
  const [weights, setWeights] = useState<Record<string, number>>({
    financial_stability: 5,
    personal_fulfillment: 5,
    family_considerations: 5,
    professional_growth: 5,
    risk: 5,
  });
  const [result, setResult] = useState<any>(null);
  const [journal, setJournal] = useState<any[]>([]);
  useEffect(() => {
    api<any[]>("/api/v1/life/decisions").then(setJournal).catch(() => undefined);
  }, []);
  return (
    <AppShell title="Life decision assistant">
      <p className="max-w-2xl text-slate-600">
        You assign the weights. The score is a transparent weighted sum, not a scientific prediction. We will not
        make the decision for you.
      </p>
      <div className="mt-4 space-y-3">
        {CRITERIA.map((id) => (
          <label key={id} className="block">
            {id.replaceAll("_", " ")} · {weights[id]}
            <input
              type="range"
              min={0}
              max={10}
              className="ml-3"
              value={weights[id]}
              onChange={(e) => setWeights({ ...weights, [id]: Number(e.target.value) })}
            />
          </label>
        ))}
      </div>
      <button
        className="btn-primary mt-4"
        onClick={async () => {
          const scored = await api("/api/v1/life/decisions/matrix", {
            method: "POST",
            body: JSON.stringify({
              title: "Stay or change",
              criteria: CRITERIA.map((id) => ({ id, weight: weights[id] })),
              options: [
                { id: "stay", title: "Stay", ratings: Object.fromEntries(CRITERIA.map((id) => [id, 6])) },
                { id: "change", title: "Change", ratings: Object.fromEntries(CRITERIA.map((id) => [id, 7])) },
              ],
            }),
          });
          setResult(scored);
        }}
      >
        Score a sample stay vs change
      </button>
      {result ? (
        <div className="card mt-4">
          <p>{result.disclaimer}</p>
          <ul className="mt-2">
            {result.options.map((row: any) => (
              <li key={row.id}>{row.title}: {row.score}</li>
            ))}
          </ul>
        </div>
      ) : null}
      <h2 className="font-display mt-8 text-2xl">Decision journal</h2>
      <button
        className="btn-secondary mt-2"
        onClick={async () => {
          await api("/api/v1/life/decisions", { method: "POST", body: JSON.stringify({ title: "Untitled decision", decision: "Describe the choice" }) });
          setJournal(await api("/api/v1/life/decisions"));
        }}
      >
        Add a private entry
      </button>
      <ul className="mt-3 list-disc pl-5">
        {journal.map((row) => <li key={row.id}>{row.title}</li>)}
      </ul>
    </AppShell>
  );
}
