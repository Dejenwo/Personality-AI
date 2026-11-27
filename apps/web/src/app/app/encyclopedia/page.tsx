"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Profile = {
  slug: string;
  preference_code: string;
  title: string;
  cluster: string;
  archetype_name: string;
  tagline: string;
};

export default function EncyclopediaPage() {
  const [data, setData] = useState<{ disclaimer: string; profiles: Profile[] } | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api<{ disclaimer: string; profiles: Profile[] }>("/api/v1/life/encyclopedia")
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);
  if (error) return <AppShell title="Personality encyclopedia"><ErrorState message={error} /></AppShell>;
  if (!data) return <AppShell title="Personality encyclopedia"><Loading /></AppShell>;
  return (
    <AppShell title="Personality encyclopedia">
      <p className="max-w-3xl text-sm text-slate-600">{data.disclaimer}</p>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {data.profiles.map((profile) => (
          <Link key={profile.slug} href={`/app/encyclopedia/${profile.slug}`} className="card block">
            <p className="text-xs uppercase tracking-wide text-teal">{profile.cluster}</p>
            <h2 className="font-display mt-1 text-2xl">
              {profile.preference_code} · {profile.title}
            </h2>
            <p className="mt-1 text-sm text-slate-500">{profile.archetype_name}</p>
            <p className="mt-2 text-slate-600">{profile.tagline}</p>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
