import Link from "next/link";
export default function Page() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-sm text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">Personality archetypes</h1>
      <p className="mt-4 text-lg text-slate-600">Sixteen original descriptive patterns mapped from Big Five means. Not MBTI. Not independently validated categories.</p>
      <Link className="btn-primary mt-8" href="/register">See your pattern</Link>
    </div>
  );
}
