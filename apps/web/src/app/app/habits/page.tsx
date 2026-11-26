"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function HabitsPage() {
  const [habits, setHabits] = useState<any[]>([]);
  async function load() {
    setHabits(await api("/api/v1/habits"));
  }
  useEffect(() => {
    load();
  }, []);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/habits", { method: "POST", body: JSON.stringify({ name: form.get("name") }) });
    event.currentTarget.reset();
    load();
  }
  return (
    <AppShell title="Habit tracker">
      <p className="mb-4 text-sm text-slate-600">No streak-shaming. Missed days are information, not a verdict.</p>
      <form className="mb-4 flex gap-2" onSubmit={onSubmit}>
        <input className="input" name="name" required placeholder="A small daily practice" />
        <button className="btn-primary">Add</button>
      </form>
      <ul className="space-y-3">
        {habits.map((habit) => (
          <li key={habit.id} className="card flex items-center justify-between">
            <span>{habit.name}</span>
            <button
              className={habit.completed_today ? "btn-primary" : "btn-secondary"}
              onClick={async () => {
                await api(`/api/v1/habits/${habit.id}/log`, { method: "POST" });
                load();
              }}
            >
              {habit.completed_today ? "Done today" : "Mark done"}
            </button>
          </li>
        ))}
      </ul>
    </AppShell>
  );
}
