"use client";

import { FormEvent, useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function EnterprisePage() {
  const [orgs, setOrgs] = useState<any[]>([]);
  async function load() {
    try {
      setOrgs(await api("/api/v1/organizations"));
    } catch {
      setOrgs([]);
    }
  }
  useEffect(() => {
    load();
  }, []);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/organizations", {
      method: "POST",
      body: JSON.stringify({ name: form.get("name"), slug: form.get("slug") }),
    });
    load();
  }
  return (
    <div className="mx-auto max-w-4xl px-4 py-10">
      <h1 className="font-display text-4xl">Enterprise development portal</h1>
      <p className="mt-3 max-w-2xl text-slate-600">
        Voluntary organizational development only. Individual results are not visible to employers without
        explicit, revocable consent. No automated hiring, firing, promotion, or compensation decisions.
      </p>
      <form className="card mt-6 flex flex-col gap-3 md:flex-row" onSubmit={onSubmit}>
        <input className="input" name="name" required placeholder="Organization name" />
        <input className="input" name="slug" required placeholder="slug" />
        <button className="btn-primary">Register organization</button>
      </form>
      <ul className="mt-6 space-y-3">
        {orgs.map((org) => (
          <li key={org.id} className="card">
            {org.name} · {org.role} · consent {String(org.results_consent)}
          </li>
        ))}
      </ul>
    </div>
  );
}
