"use client";

import { FormEvent, useState } from "react";
import { AuthFrame } from "@/components/AuthFrame";
import { Success } from "@/components/State";
import { api } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [devToken, setDevToken] = useState("");
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const result = await api<{ dev_token?: string }>("/api/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email: form.get("email") }),
    });
    setDevToken(result.dev_token || "If the account exists, check your email (local: token returned).");
  }
  return (
    <AuthFrame title="Password recovery" subtitle="We never confirm whether an email is registered.">
      <form className="mt-6 space-y-4" onSubmit={onSubmit}>
        <input className="input" name="email" type="email" required placeholder="you@example.com" />
        <button className="btn-primary w-full">Send reset</button>
      </form>
      {devToken ? <div className="mt-4"><Success message={devToken} /></div> : null}
    </AuthFrame>
  );
}
