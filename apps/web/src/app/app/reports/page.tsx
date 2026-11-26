"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api, apiBase, getToken } from "@/lib/api";

export default function ReportsPage() {
  const [rows, setRows] = useState<any[]>([]);
  async function load() {
    setRows(await api("/api/v1/reports"));
  }
  useEffect(() => {
    load();
  }, []);
  async function create(type: string) {
    await api("/api/v1/reports", { method: "POST", body: JSON.stringify({ report_type: type }) });
    load();
  }
  return (
    <AppShell title="Report library">
      <div className="flex flex-wrap gap-2">
        {["comprehensive", "big-five", "career", "relationship", "leadership"].map((type) => (
          <button key={type} className="btn-secondary" onClick={() => create(type)}>
            Generate {type}
          </button>
        ))}
      </div>
      <ul className="mt-6 space-y-3">
        {rows.map((row) => (
          <li key={row.id} className="card flex justify-between">
            <span>{row.title}</span>
            <span className="flex gap-3">
              <Link href={`/app/reports/${row.id}`}>Preview</Link>
              <a href={`${apiBase()}/api/v1/reports/${row.id}/pdf`} onClick={(e) => {
                e.preventDefault();
                fetch(`${apiBase()}/api/v1/reports/${row.id}/pdf`, { headers: { Authorization: `Bearer ${getToken()}` } })
                  .then((r) => r.blob())
                  .then((blob) => {
                    const url = URL.createObjectURL(blob);
                    window.open(url, "_blank");
                  });
              }}>PDF</a>
            </span>
          </li>
        ))}
      </ul>
    </AppShell>
  );
}
