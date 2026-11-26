"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ArchetypePage() {
  const { slug } = useParams<{ slug: string }>();
  const [item, setItem] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/personality/archetypes/${slug}`).then(setItem);
  }, [slug]);
  if (!item) return <AppShell title="Archetype"><p>Loading…</p></AppShell>;
  return (
    <AppShell title={item.name}>
      <p className="text-teal">{item.tagline}</p>
      <p className="mt-4 max-w-3xl">{item.description}</p>
      <p className="mt-4 text-sm text-slate-500">Descriptive product construct. Not a scientifically established category. Not a Myers-Briggs type.</p>
    </AppShell>
  );
}
