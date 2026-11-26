"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CareerPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api<any[]>("/api/v1/careers").then(setItems);
  }, []);
  return (
    <AppShell title="Career exploration">
      <p className="mb-4 text-sm text-slate-600">
        Interests are not competence. PersonalityDNA will not determine hiring eligibility.
      </p>
      <Link className="btn-secondary mb-6" href="/app/assessments/career-interests">
        Take career interest assessment
      </Link>
      <div className="grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <Link key={item.slug} href={`/app/career/${item.slug}`} className="card block">
            <h2 className="font-display text-xl">{item.title}</h2>
            <p className="mt-2 text-slate-600">{item.summary}</p>
          </Link>
        ))}
      </div>
    </AppShell>
  );
}
