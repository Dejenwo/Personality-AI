"use client";

import { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ExportPage() {
  const [payload, setPayload] = useState<any>(null);
  return (
    <AppShell title="Data export">
      <button className="btn-primary" onClick={async () => setPayload(await api("/api/v1/privacy/export"))}>
        Generate export
      </button>
      {payload ? <pre className="card mt-4 overflow-auto text-xs">{JSON.stringify(payload, null, 2)}</pre> : null}
    </AppShell>
  );
}
