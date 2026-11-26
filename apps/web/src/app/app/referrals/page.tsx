"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ReferralsPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/referrals").then(setData);
  }, []);
  return (
    <AppShell title="Referral dashboard">
      <div className="card">
        <p>Your code: <strong>{data?.code}</strong></p>
        <p className="mt-2 break-all text-sm">{data?.url}</p>
      </div>
    </AppShell>
  );
}
