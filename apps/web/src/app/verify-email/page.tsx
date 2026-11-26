"use client";

import { useState } from "react";
import { AuthFrame } from "@/components/AuthFrame";
import { Success, ErrorState } from "@/components/State";
import { api } from "@/lib/api";

export default function VerifyEmailPage() {
  const [ok, setOk] = useState(false);
  const [error, setError] = useState("");
  async function verify() {
    try {
      await api("/api/v1/auth/verify-email", { method: "POST" });
      setOk(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not verify");
    }
  }
  return (
    <AuthFrame title="Email verification" subtitle="Local development marks the current session verified.">
      {error ? <ErrorState message={error} /> : null}
      {ok ? <Success message="Email marked verified." /> : <button className="btn-primary mt-6" onClick={verify}>Verify now</button>}
    </AuthFrame>
  );
}
