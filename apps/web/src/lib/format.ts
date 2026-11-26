export function traitColor(trait: string) {
  const map: Record<string, string> = {
    openness: "#6366F1",
    conscientiousness: "#14B8A6",
    extraversion: "#F59E0B",
    agreeableness: "#EC4899",
    emotional_stability: "#0EA5E9",
    negative_emotionality: "#F43F5E",
  };
  return map[trait] || "#6366F1";
}

export function meanLabel(mean: number) {
  if (mean >= 3.5) return "Higher";
  if (mean <= 2.5) return "Lower";
  return "Mid-range";
}
