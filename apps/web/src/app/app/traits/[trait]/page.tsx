"use client";

import { useParams } from "next/navigation";
import { AppShell } from "@/components/AppShell";

const COPY: Record<string, string> = {
  openness: "Curiosity, imagination, and intellectual exploration. IPIP labels this Intellect/Imagination.",
  conscientiousness: "Organization, reliability, planning, and goal orientation.",
  extraversion: "Sociability, assertiveness, social energy, and stimulation preference.",
  agreeableness: "Cooperation, empathy, trust, and interpersonal consideration.",
  emotional_stability: "Evenness of mood. The inverse display is Negative Emotionality. Neither is a diagnosis.",
  negative_emotionality: "Displayed as the inverse of Emotional Stability. Not a clinical neuroticism diagnosis.",
};

export default function TraitPage() {
  const { trait } = useParams<{ trait: string }>();
  return (
    <AppShell title="Individual trait details">
      <div className="card">
        <h2 className="font-display text-2xl capitalize">{trait.replaceAll("_", " ")}</h2>
        <p className="mt-3">{COPY[trait] || "Trait explanation."}</p>
        <p className="mt-4 text-sm text-slate-500">Scores are min-max scaled, not population percentiles.</p>
      </div>
    </AppShell>
  );
}
