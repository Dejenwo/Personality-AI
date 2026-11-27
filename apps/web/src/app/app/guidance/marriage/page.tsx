"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function MarriagePage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [category, setCategory] = useState("");
  const [pairing, setPairing] = useState<any>(null);
  const [a, setA] = useState("analyst");
  const [b, setB] = useState("connector");
  useEffect(() => {
    const query = category ? `?category=${category}` : "";
    api<{ items: any[] }>(`/api/v1/life/marriage/questions${query}`).then((data) => setQuestions(data.items));
  }, [category]);
  return (
    <AppShell title="Marriage and relationship intelligence">
      <p className="max-w-2xl text-slate-600">
        These questions support discussion. They are not a pass/fail marriage test. We do not assign compatibility
        percentages. Abuse is not a personality difference.
      </p>
      <label className="mt-4 block text-sm">
        Category
        <select className="ml-2 rounded border px-2 py-1" value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">All</option>
          {Array.from(new Set(questions.map((row) => row.category))).map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
      </label>
      <ol className="mt-6 list-decimal space-y-2 pl-5">
        {questions.map((row) => (
          <li key={row.text}>{row.text}</li>
        ))}
      </ol>
      <h2 className="font-display mt-10 text-2xl">Educational pairing notes</h2>
      <div className="mt-3 flex gap-2">
        <input className="rounded border px-2 py-1" value={a} onChange={(e) => setA(e.target.value)} />
        <input className="rounded border px-2 py-1" value={b} onChange={(e) => setB(e.target.value)} />
        <button
          className="btn-secondary"
          onClick={async () => setPairing(await api(`/api/v1/life/marriage/pairing/${a}/${b}`))}
        >
          Compare codes
        </button>
      </div>
      {pairing ? (
        <div className="card mt-4">
          <p>{pairing.code_a} and {pairing.code_b}</p>
          <p className="mt-2 text-sm">{pairing.disclaimer}</p>
          <p className="mt-2 text-sm text-rose-700">{pairing.safety}</p>
          <ul className="mt-3 list-disc pl-5">
            {pairing.differences.map((row: string) => <li key={row}>{row}</li>)}
          </ul>
        </div>
      ) : null}
    </AppShell>
  );
}
