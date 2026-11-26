export type Plan = "free" | "premium" | "enterprise" | "staff";

export type TraitKey =
  | "openness"
  | "conscientiousness"
  | "extraversion"
  | "agreeableness"
  | "emotional_stability"
  | "negative_emotionality";

export interface TraitScore {
  trait: string;
  name: string;
  raw_sum: number;
  mean: number;
  scaled_0_100: number;
  explanation: string;
}

export interface ArchetypeSummary {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  mixed?: boolean;
  palette?: { primary: string; accent: string };
}
