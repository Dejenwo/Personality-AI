"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function RelationshipsPage() {
  const [data, setData] = useState<any>({ sent: [], received: [] });
  async function load() {
    setData(await api("/api/v1/relationships/invitations"));
  }
  useEffect(() => {
    load();
  }, []);
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/relationships/invitations", {
      method: "POST",
      body: JSON.stringify({ email: form.get("email"), relationship_type: form.get("relationship_type") }),
    });
    load();
  }
  return (
    <AppShell title="Relationship intelligence">
      <p className="mb-4 text-sm text-slate-600">
        Every participant must consent. Journals and coaching history are never included in a comparison.
        We do not predict relationship success.
      </p>
      <form className="card mb-6 flex flex-col gap-3 md:flex-row" onSubmit={onSubmit}>
        <input className="input" name="email" type="email" required placeholder="their@email.com" />
        <select className="input" name="relationship_type">
          <option value="partner">Romantic partner</option>
          <option value="spouse">Married couple</option>
          <option value="friend">Friend</option>
          <option value="family">Family</option>
          <option value="colleague">Colleague</option>
        </select>
        <button className="btn-primary">Invite</button>
      </form>
      <h2 className="font-semibold">Sent</h2>
      <ul className="mt-2 space-y-2">
        {data.sent.map((row: any) => (
          <li key={row.id} className="card flex justify-between">
            <span>{row.invitee_email} · {row.status}</span>
            <Link href={`/app/relationships/${row.id}`}>Open</Link>
          </li>
        ))}
      </ul>
      <h2 className="mt-6 font-semibold">Received</h2>
      <ul className="mt-2 space-y-2">
        {data.received.map((row: any) => (
          <li key={row.id} className="card flex justify-between">
            <span>{row.relationship_type} · {row.status}</span>
            {row.status === "pending" ? (
              <button
                className="btn-secondary"
                onClick={async () => {
                  await api(`/api/v1/relationships/invitations/${row.id}/accept`, { method: "POST" });
                  load();
                }}
              >
                Accept
              </button>
            ) : (
              <Link href={`/app/relationships/${row.id}`}>Compare</Link>
            )}
          </li>
        ))}
      </ul>
    </AppShell>
  );
}
