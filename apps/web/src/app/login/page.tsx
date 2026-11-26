"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { AuthFrame } from "@/components/AuthFrame";
import { ErrorState } from "@/components/State";
import { api, setTokens } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);
    const form = new FormData(event.currentTarget);
    try {
      const result = await api<{ access_token: string; refresh_token: string }>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email: form.get("email"), password: form.get("password") }),
      });
      setTokens(result.access_token, result.refresh_token);
      router.push("/app");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to log in");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthFrame title="Welcome back" subtitle="Log in to continue your development practice.">
      {error ? <ErrorState message={error} /> : null}
      <form className="mt-6 space-y-4" onSubmit={onSubmit}>
        <label className="block text-sm">
          Email
          <input className="input mt-1" name="email" type="email" autoComplete="email" required defaultValue="demo@personalitydna.ai" />
        </label>
        <label className="block text-sm">
          Password
          <input className="input mt-1" name="password" type="password" autoComplete="current-password" required defaultValue="DemoPass123!" />
        </label>
        <button className="btn-primary w-full" disabled={loading}>
          {loading ? "Signing in…" : "Log in"}
        </button>
      </form>
      <p className="mt-4 text-sm text-slate-500">
        Demo account is pre-filled for local development. Social login is not enabled until OAuth credentials exist.
      </p>
      <div className="mt-4 flex justify-between text-sm">
        <Link href="/forgot-password">Forgot password</Link>
        <Link href="/register">Create an account</Link>
      </div>
    </AuthFrame>
  );
}
