import Link from "next/link";

const steps = [
  { title: "Measure", body: "Answer public-domain Big Five items. Scoring is deterministic." },
  { title: "Interpret", body: "See traits, an original archetype, strengths, and growth edges." },
  { title: "Practice", body: "Coach, programs, journal, and habits — with privacy controls." },
];

export default function IntroPage() {
  return (
    <div className="mx-auto max-w-2xl px-4 py-16">
      <h1 className="font-display text-4xl">Product introduction</h1>
      <div className="mt-8 space-y-4">
        {steps.map((step) => (
          <article key={step.title} className="card">
            <h2 className="font-display text-2xl">{step.title}</h2>
            <p className="mt-2 text-slate-600">{step.body}</p>
          </article>
        ))}
      </div>
      <Link className="btn-primary mt-8" href="/register">
        Continue to registration
      </Link>
    </div>
  );
}
