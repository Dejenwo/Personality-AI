"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { AuthFrame } from "@/components/AuthFrame";
import { ErrorState } from "@/components/State";
import { api, setTokens } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    try {
      const result = await api<{ access_token: string; refresh_token: string }>("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email: form.get("email"),
          password: form.get("password"),
          display_name: form.get("display_name"),
          consent_privacy: form.get("consent_privacy") === "on",
          consent_research: form.get("consent_research") === "on",
        }),
      });
      setTokens(result.access_token, result.refresh_token);
      router.push("/consent");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to register");
    }
  }

  return (
    <AuthFrame title="Create your account" subtitle="Adults 18 and older. Educational use, not a clinical service.">
      {error ? <ErrorState message={error} /> : null}
      <form className="mt-6 space-y-4" onSubmit={onSubmit}>
        <label className="block text-sm">
          Name
          <input className="input mt-1" name="display_name" required />
        </label>
        <label className="block text-sm">
          Email
          <input className="input mt-1" name="email" type="email" required />
        </label>
        <label className="block text-sm">
          Password (10+ characters)
          <input className="input mt-1" name="password" type="password" minLength={10} required />
        </label>
        <label className="flex gap-2 text-sm">
          <input name="consent_privacy" type="checkbox" required />
          I agree to the privacy notice and that this is not therapy or a hiring tool.
        </label>
        <label className="flex gap-2 text-sm">
          <input name="consent_research" type="checkbox" />
          Optional: allow de-identified research use of assessment scores (never journals).
        </label>
        <button className="btn-primary w-full">Create account</button>
      </form>
      <p className="mt-4 text-sm">
        Already have an account? <Link href="/login">Log in</Link>
      </p>
    </AuthFrame>
  );
}
