"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ReportPreview() {
  const { id } = useParams<{ id: string }>();
  const [row, setRow] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/reports/${id}`).then(setRow);
  }, [id]);
  if (!row) return <AppShell title="Report"><p>Loading…</p></AppShell>;
  const p = row.payload;
  return (
    <AppShell title={row.title}>
      <article className="card prose">
        <h2>{p.archetype?.name}</h2>
        <p>{p.archetype?.description}</p>
        <h3 className="mt-6 font-semibold">Methodology</h3>
        <p>{p.methodology}</p>
        <h3 className="mt-4 font-semibold">Limitations</h3>
        <p>{p.limitations}</p>
      </article>
    </AppShell>
  );
}
