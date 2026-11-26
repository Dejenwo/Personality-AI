"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function GoalsPage() {
  const [goals, setGoals] = useState<any[]>([]);
  async function load() {
    setGoals(await api("/api/v1/goals"));
  }
  useEffect(() => {
    load();
  }, []);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/goals", {
      method: "POST",
      body: JSON.stringify({ title: form.get("title"), description: form.get("description") }),
    });
    event.currentTarget.reset();
    load();
  }
  return (
    <AppShell title="Goal management">
      <form className="card space-y-3" onSubmit={onSubmit}>
        <input className="input" name="title" required placeholder="A specific, observable goal" />
        <textarea className="input" name="description" placeholder="Why it matters" />
        <button className="btn-primary">Save goal</button>
      </form>
      <ul className="mt-4 space-y-3">
        {goals.map((goal) => (
          <li key={goal.id} className="card">
            <strong>{goal.title}</strong>
            <p className="text-slate-600">{goal.description}</p>
            <p className="text-sm text-slate-500">Progress {goal.progress}%</p>
          </li>
        ))}
      </ul>
    </AppShell>
  );
}
