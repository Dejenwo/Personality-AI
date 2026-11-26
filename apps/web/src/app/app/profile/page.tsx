"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api, clearTokens } from "@/lib/api";

const LINKS = [
  ["/app/settings/language", "Language"],
  ["/app/settings/accessibility", "Accessibility"],
  ["/app/settings/notifications", "Notifications"],
  ["/app/settings/privacy", "Privacy"],
  ["/app/settings/export", "Data export"],
  ["/app/settings/delete", "Account deletion"],
  ["/app/settings/subscription", "Subscription"],
  ["/app/referrals", "Referrals"],
  ["/app/help", "Help center"],
  ["/app/feedback", "Feedback"],
  ["/app/support", "Customer support"],
  ["/legal/privacy", "Legal"],
];

export default function ProfilePage() {
  const [me, setMe] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api("/api/v1/users/me").then(setMe).catch((err) => setError(err.message));
  }, []);
  if (error) return <AppShell title="Profile"><ErrorState message={error} /></AppShell>;
  if (!me) return <AppShell title="Profile"><Loading /></AppShell>;
  return (
    <AppShell title="Profile">
      <div className="card">
        <h2 className="font-display text-2xl">{me.profile.display_name}</h2>
        <p className="text-slate-500">{me.email}</p>
        <p className="mt-2 text-sm">Plan: {me.subscription.plan}</p>
        <Link className="btn-secondary mt-4" href="/app/profile/edit">
          Edit profile
        </Link>
      </div>
      <ul className="mt-6 grid gap-2 md:grid-cols-2">
        {LINKS.map(([href, label]) => (
          <li key={href}>
            <Link className="card block" href={href}>
              {label}
            </Link>
          </li>
        ))}
      </ul>
      <button
        className="btn-secondary mt-6"
        onClick={() => {
          clearTokens();
          window.location.href = "/login";
        }}
      >
        Log out
      </button>
    </AppShell>
  );
}
