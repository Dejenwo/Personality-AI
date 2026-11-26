"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AdminPage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api("/api/v1/admin/overview").then(setData).catch((err) => setError(err.message));
  }, []);
  return (
    <div className="mx-auto max-w-5xl px-4 py-10">
      <h1 className="font-display text-4xl">Administrative portal</h1>
      <p className="mt-2 text-slate-600">Least-privilege. Demo admin: admin@personalitydna.ai / DemoPass123!</p>
      {error ? <p className="mt-6 text-rose-600">{error}</p> : null}
      {data ? (
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <div className="card">Users {data.users}</div>
          <div className="card">Results {data.results}</div>
          <div className="card">Conversations {data.conversations}</div>
          <div className="card">Free {data.plans?.free}</div>
          <div className="card">Premium {data.plans?.premium}</div>
        </div>
      ) : null}
    </div>
  );
}
