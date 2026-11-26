"use client";

import { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Success } from "@/components/State";
import { api } from "@/lib/api";

export default function PremiumPage() {
  const [done, setDone] = useState(false);
  return (
    <AppShell title="Premium subscription">
      <p className="max-w-xl text-slate-600">
        Proposed pricing (hypothesis, not validated): $9.99 / month or $69.99 / year. Stripe, RevenueCat, Apple,
        and Google purchases require credentials and store review.
      </p>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="card">
          <h2 className="font-display text-2xl">Monthly</h2>
          <p className="mt-2 text-3xl">$9.99</p>
        </div>
        <div className="card">
          <h2 className="font-display text-2xl">Annual</h2>
          <p className="mt-2 text-3xl">$69.99</p>
        </div>
      </div>
      <button
        className="btn-primary mt-6"
        onClick={async () => {
          await api("/api/v1/subscriptions/premium-dev", { method: "POST" });
          setDone(true);
        }}
      >
        Grant local premium (development only)
      </button>
      {done ? <div className="mt-4"><Success message="Premium entitlement granted in this development environment." /></div> : null}
    </AppShell>
  );
}
