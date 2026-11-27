"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function MoneyPage() {
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [result, setResult] = useState<any>(null);
  useEffect(() => {
    api<{ questions: any[] }>("/api/v1/life/finance/questions").then((data) => setQuestions(data.questions));
  }, []);
  return (
    <AppShell title="Financial habit reflection">
      <p className="max-w-2xl text-slate-600">
        These questions are about actual habits. They are not inferred from personality type and are not investment,
        tax, or legal advice.
      </p>
      <form
        className="mt-6 space-y-4"
        onSubmit={async (event) => {
          event.preventDefault();
          setResult(await api("/api/v1/life/finance", { method: "POST", body: JSON.stringify({ responses: answers }) }));
        }}
      >
        {questions.map((item) => (
          <label key={item.id} className="card block">
            <p>{item.text}</p>
            <input
              type="range"
              min={1}
              max={5}
              className="mt-2 w-full"
              onChange={(e) => setAnswers((prev) => ({ ...prev, [item.id]: Number(e.target.value) }))}
            />
          </label>
        ))}
        <button className="btn-primary" type="submit">Save reflection</button>
      </form>
      {result ? (
        <div className="card mt-6">
          <p>{result.disclaimer}</p>
          <ul className="mt-3 list-disc pl-5">
            {(result.education || []).map((row: string) => <li key={row}>{row}</li>)}
          </ul>
        </div>
      ) : null}
    </AppShell>
  );
}
