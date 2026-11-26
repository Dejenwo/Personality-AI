"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CareerDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [item, setItem] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/careers/${slug}`).then(setItem);
  }, [slug]);
  if (!item) return <AppShell title="Career"><p>Loading…</p></AppShell>;
  return (
    <AppShell title={item.title}>
      <p>{item.summary}</p>
      <h2 className="mt-6 font-semibold">Skills to explore</h2>
      <ul className="list-disc pl-5">{item.skills_to_explore?.map((s: string) => <li key={s}>{s}</li>)}</ul>
      <h2 className="mt-6 font-semibold">Learning experiments</h2>
      <ul className="list-disc pl-5">{item.learning?.map((s: string) => <li key={s}>{s}</li>)}</ul>
    </AppShell>
  );
}
