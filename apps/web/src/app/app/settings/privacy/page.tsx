"use client";

import { FormEvent } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function PrivacySettings() {
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/users/me/preferences", {
      method: "PATCH",
      body: JSON.stringify({
        journal_ai_analysis: form.get("journal_ai_analysis") === "on",
        coach_may_use_journal: form.get("coach_may_use_journal") === "on",
        coach_may_use_assessments: form.get("coach_may_use_assessments") === "on",
      }),
    });
    alert("Saved");
  }
  return (
    <AppShell title="Privacy settings">
      <form className="card space-y-3" onSubmit={onSubmit}>
        <label className="flex gap-2"><input type="checkbox" name="coach_may_use_assessments" defaultChecked /> Coach may use assessment results</label>
        <label className="flex gap-2"><input type="checkbox" name="journal_ai_analysis" /> Enable journal AI analysis by default</label>
        <label className="flex gap-2"><input type="checkbox" name="coach_may_use_journal" /> Coach may use authorized journal entries</label>
        <button className="btn-primary">Save</button>
      </form>
    </AppShell>
  );
}
