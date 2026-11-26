"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function SubscriptionPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/subscriptions").then(setData);
  }, []);
  return (
    <AppShell title="Subscription management">
      <div className="card">
        <p>Plan: {data?.plan}</p>
        <p>Status: {data?.status}</p>
        <p className="mt-2 text-sm text-slate-500">{data?.pricing_hypothesis?.note}</p>
        <div className="mt-4 flex gap-3">
          <Link className="btn-primary" href="/app/premium">Upgrade</Link>
          <button className="btn-secondary" onClick={() => api("/api/v1/subscriptions/cancel", { method: "POST" })}>Cancel at period end</button>
        </div>
      </div>
    </AppShell>
  );
}
