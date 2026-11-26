"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { AppShell } from "@/components/AppShell";
import { Loading, Success } from "@/components/State";

function CompleteInner() {
  const search = useSearchParams();
  const result = search.get("result");
  return (
    <AppShell title="Assessment complete">
      <Success message="Your responses were scored by the deterministic engine. AI did not invent these numbers." />
      <div className="mt-6 flex gap-3">
        <Link className="btn-primary" href={result ? `/app/results/${result}` : "/app"}>
          View personality results
        </Link>
        <Link className="btn-secondary" href="/app/discover">
          More assessments
        </Link>
      </div>
    </AppShell>
  );
}

export default function CompletePage() {
  return (
    <Suspense fallback={<AppShell title="Assessment complete"><Loading /></AppShell>}>
      <CompleteInner />
    </Suspense>
  );
}
