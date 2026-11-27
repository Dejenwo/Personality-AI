"use client";

import { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api, apiBase, getToken } from "@/lib/api";

export default function BlueprintPage() {
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState("");
  return (
    <AppShell title="My Life Blueprint">
      <p className="max-w-2xl text-slate-600">
        A personalized report assembled only from information you have provided. Empty sections are omitted instead of
        padded. Proposed price $39.99 is a hypothesis, not a live checkout.
      </p>
      <button
        className="btn-primary mt-4"
        onClick={async () => {
          try {
            setReport(await api("/api/v1/life/blueprint", { method: "POST", body: JSON.stringify({ exclude: [] }) }));
          } catch (err) {
            setError((err as Error).message);
          }
        }}
      >
        Generate from my current data
      </button>
      {error ? <p className="mt-3 text-rose-700">{error}</p> : null}
      {report ? (
        <div className="card mt-6">
          <p>{report.page_estimate_note}</p>
          <ul className="mt-3 list-disc pl-5">
            {(report.sections || []).map((section: any) => (
              <li key={section.key}>{section.key.replaceAll("_", " ")}</li>
            ))}
          </ul>
          {report.id ? (
            <a
              className="btn-secondary mt-4 inline-block"
              href={`${apiBase()}/api/v1/life/blueprint/${report.id}/pdf`}
              onClick={(event) => {
                event.preventDefault();
                fetch(`${apiBase()}/api/v1/life/blueprint/${report.id}/pdf`, {
                  headers: { Authorization: `Bearer ${getToken()}` },
                })
                  .then((res) => res.blob())
                  .then((blob) => {
                    const url = URL.createObjectURL(blob);
                    window.open(url, "_blank");
                  });
              }}
            >
              Download PDF
            </a>
          ) : null}
        </div>
      ) : null}
    </AppShell>
  );
}
