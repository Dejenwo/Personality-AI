"use client";

import { FormEvent, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Success } from "@/components/State";
import { api } from "@/lib/api";

export default function FeedbackPage() {
  const [ok, setOk] = useState(false);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/feedback", { method: "POST", body: JSON.stringify({ category: form.get("category"), message: form.get("message") }) });
    setOk(true);
  }
  return (
    <AppShell title="Feedback">
      <form className="card space-y-3" onSubmit={onSubmit}>
        <select className="input" name="category">
          <option value="general">General</option>
          <option value="bug">Bug</option>
          <option value="safety">Safety / harm</option>
          <option value="science">Scientific concern</option>
        </select>
        <textarea className="input min-h-32" name="message" required />
        <button className="btn-primary">Send</button>
      </form>
      {ok ? <div className="mt-4"><Success message="Thank you. We read safety reports first." /></div> : null}
    </AppShell>
  );
}
