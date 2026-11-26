"use client";

import { useRouter } from "next/navigation";
import { FormEvent } from "react";
import { api } from "@/lib/api";

export default function PreferencesOnboarding() {
  const router = useRouter();
  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await api("/api/v1/users/me/preferences", {
      method: "PATCH",
      body: JSON.stringify({
        theme: form.get("theme"),
        daily_insights: form.get("daily_insights") === "on",
        coach_may_use_assessments: true,
      }),
    });
    router.push("/app");
  }
  return (
    <div className="mx-auto max-w-lg px-4 py-16">
      <h1 className="font-display text-4xl">Your preferences</h1>
      <form className="card mt-6 space-y-4" onSubmit={onSubmit}>
        <label className="block text-sm">
          Theme
          <select className="input mt-1" name="theme" defaultValue="system">
            <option value="system">System</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label className="flex gap-2 text-sm">
          <input type="checkbox" name="daily_insights" defaultChecked /> Daily insights
        </label>
        <button className="btn-primary">Save and enter</button>
      </form>
    </div>
  );
}
