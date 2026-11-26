"use client";

import Link from "next/link";
import { useState } from "react";
import { api } from "@/lib/api";

export default function ConsentPage() {
  const [done, setDone] = useState(false);
  async function save() {
    await api("/api/v1/users/me/consent", { method: "POST", body: JSON.stringify({ kind: "product_education", granted: true }) });
    setDone(true);
  }
  return (
    <div className="mx-auto max-w-xl px-4 py-16">
      <h1 className="font-display text-4xl">Consent and privacy</h1>
      <ul className="mt-6 list-disc space-y-2 pl-5 text-slate-700">
        <li>Assessments, journals, and coaching are sensitive personal information.</li>
        <li>We do not sell personality data or diagnose conditions.</li>
        <li>You can export or request deletion at any time.</li>
        <li>Journal AI analysis is off unless you enable it.</li>
      </ul>
      <button className="btn-primary mt-8" onClick={save}>
        I understand
      </button>
      {done ? (
        <Link className="btn-secondary ml-3" href="/onboarding/preferences">
          Continue
        </Link>
      ) : null}
    </div>
  );
}
