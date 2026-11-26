"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function JournalPage() {
  const [entries, setEntries] = useState<any[]>([]);
  const [q, setQ] = useState("");
  async function load(query = "") {
    const path = query ? `/api/v1/journals?q=${encodeURIComponent(query)}` : "/api/v1/journals";
    setEntries(await api(path));
  }
  useEffect(() => {
    load();
  }, []);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/journals", {
      method: "POST",
      body: JSON.stringify({
        title: form.get("title"),
        body: form.get("body"),
        entry_type: form.get("entry_type"),
        allow_ai: form.get("allow_ai") === "on",
      }),
    });
    (event.currentTarget as HTMLFormElement).reset();
    load(q);
  }
  return (
    <AppShell title="Personal journal">
      <p className="mb-4 text-sm text-slate-600">Private by default. AI analysis requires a separate checkbox on each entry.</p>
      <form className="card space-y-3" onSubmit={onSubmit}>
        <input className="input" name="title" placeholder="Title" />
        <textarea className="input min-h-32" name="body" required placeholder="What are you noticing?" />
        <select className="input" name="entry_type" defaultValue="reflection">
          <option value="reflection">Daily reflection</option>
          <option value="gratitude">Gratitude</option>
          <option value="goal">Goal reflection</option>
          <option value="development">Development note</option>
          <option value="communication">Communication</option>
        </select>
        <label className="flex gap-2 text-sm">
          <input type="checkbox" name="allow_ai" /> Allow this entry in AI context
        </label>
        <button className="btn-primary">Save entry</button>
      </form>
      <div className="mt-4 flex gap-2">
        <input className="input" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search" />
        <button className="btn-secondary" onClick={() => load(q)}>Search</button>
      </div>
      <ul className="mt-4 space-y-3">
        {entries.map((entry) => (
          <li key={entry.id} className="card">
            <div className="flex justify-between">
              <strong>{entry.title || entry.entry_type}</strong>
              <button
                className="text-sm text-rose-600"
                onClick={async () => {
                  await api(`/api/v1/journals/${entry.id}`, { method: "DELETE" });
                  load(q);
                }}
              >
                Delete
              </button>
            </div>
            <p className="mt-2 whitespace-pre-wrap">{entry.body}</p>
          </li>
        ))}
        {entries.length === 0 ? <li className="text-slate-500">No entries yet.</li> : null}
      </ul>
    </AppShell>
  );
}
