"use client";

import { FormEvent, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api, clearTokens } from "@/lib/api";

export default function DeletePage() {
  const [done, setDone] = useState(false);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/privacy/delete", { method: "POST", body: JSON.stringify({ reason: form.get("reason") }) });
    clearTokens();
    setDone(true);
  }
  return (
    <AppShell title="Account deletion">
      {done ? <p>Deletion requested. You have been signed out.</p> : (
        <form className="card space-y-3" onSubmit={onSubmit}>
          <textarea className="input" name="reason" placeholder="Optional reason" />
          <button className="btn-primary">Request deletion</button>
        </form>
      )}
    </AppShell>
  );
}
