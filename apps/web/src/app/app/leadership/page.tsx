"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function LeadershipPage() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api("/api/v1/leadership/insights").then(setData);
  }, []);
  return (
    <AppShell title="Leadership insights">
      <p className="text-sm text-slate-600">{data?.disclaimer}</p>
      <ul className="mt-4 list-disc pl-5">
        {data?.practices?.map((item: string) => <li key={item}>{item}</li>)}
      </ul>
      <Link className="btn-primary mt-6" href="/app/assessments/leadership">Leadership preferences assessment</Link>
    </AppShell>
  );
}
