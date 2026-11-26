"use client";

import { FormEvent } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function EditProfile() {
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/users/me/profile", {
      method: "PATCH",
      body: JSON.stringify({ display_name: form.get("display_name"), headline: form.get("headline"), occupation: form.get("occupation") }),
    });
  }
  return (
    <AppShell title="Profile management">
      <form className="card space-y-3" onSubmit={onSubmit}>
        <input className="input" name="display_name" placeholder="Name" required />
        <input className="input" name="headline" placeholder="Headline" />
        <input className="input" name="occupation" placeholder="Occupation" />
        <button className="btn-primary">Save</button>
      </form>
    </AppShell>
  );
}
