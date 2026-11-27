"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

const FALLBACK = [
  { slug: "self", href: "/app/encyclopedia", name: "Self Intelligence", note: "16 educational profiles, 60 sections each." },
  { slug: "career", href: "/app/guidance/career", name: "Career Intelligence", note: "O*NET explorer. No fabricated wages." },
  { slug: "marriage", href: "/app/guidance/marriage", name: "Marriage Intelligence", note: "Premarital questions. No compatibility %." },
  { slug: "family", href: "/app/guidance/family", name: "Family Intelligence", note: "Adult parenting reflection. No child typing." },
  { slug: "finance", href: "/app/guidance/money", name: "Financial Intelligence", note: "Habit questionnaire, not inferred from type." },
  { slug: "leadership", href: "/app/leadership", name: "Leadership Intelligence", note: "Preferences, not competence certificates." },
  { slug: "decisions", href: "/app/guidance/decisions", name: "Life Decision Intelligence", note: "Your weights. We do not decide for you." },
  { slug: "growth", href: "/app/growth", name: "Personal Growth", note: "Programs, habits, Life Blueprint." },
];

export default function GuidancePage() {
  const [centers, setCenters] = useState(FALLBACK);
  useEffect(() => {
    api<{ centers: typeof FALLBACK }>("/api/v1/life/centers")
      .then((data) => {
        const notes = Object.fromEntries(FALLBACK.map((row) => [row.slug, row.note]));
        setCenters(data.centers.map((row) => ({ ...row, note: notes[row.slug] || "" })));
      })
      .catch(() => undefined);
  }, []);
  return (
    <AppShell title="Life guidance">
      <p className="max-w-2xl text-slate-600">
        Personality is one source of information, not destiny. These centers use your scores when you have them
        and your own answers for everything else.
      </p>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {centers.map((center) => (
          <Link key={center.slug} href={center.href} className="card block">
            <h2 className="font-display text-2xl">{center.name}</h2>
            <p className="mt-2 text-slate-600">{center.note}</p>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
