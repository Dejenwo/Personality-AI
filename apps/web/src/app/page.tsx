import Link from "next/link";

const pillars = [
  { title: "Measured, not invented", body: "Big Five scores come from a deterministic engine. The coach never writes the numbers." },
  { title: "A practice, not a type", body: "Return for coaching, programs, journals, and habits — not a one-time quiz screenshot." },
  { title: "Private by default", body: "Journals and transcripts stay yours. Comparison requires consent from every person." },
];

const modules = [
  "Big Five assessment",
  "16 original archetypes",
  "AI coach with safety rails",
  "Career exploration",
  "Relationship communication",
  "Leadership preferences",
  "Growth academy",
  "Private journal",
];

export default function HomePage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10 md:py-16">
      <header className="flex items-center justify-between">
        <span className="font-display text-2xl">PersonalityDNA AI</span>
        <div className="flex gap-3">
          <Link className="btn-secondary" href="/login">
            Log in
          </Link>
          <Link className="btn-primary" href="/register">
            Begin
          </Link>
        </div>
      </header>

      <section className="mt-16 grid items-center gap-12 md:grid-cols-2">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal">Personality intelligence</p>
          <h1 className="font-display mt-4 text-5xl leading-tight md:text-6xl">
            Discover yourself.
            <br />
            Understand others.
            <br />
            Transform your life.
          </h1>
          <p className="mt-6 max-w-xl text-lg text-slate-600">
            A premium personal-development platform grounded in the public-domain IPIP Big Five, original
            descriptive archetypes, and an educational AI coach. Not therapy. Not a hiring tool. Not a copy of a type test.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link className="btn-primary" href="/register">
              Take the free Big Five
            </Link>
            <Link className="btn-secondary" href="/big-five">
              How we measure
            </Link>
          </div>
        </div>
        <div className="card relative overflow-hidden">
          <Helix />
          <p className="relative z-10 font-display text-2xl">Your profile is a pattern, not a prison.</p>
          <p className="relative z-10 mt-3 text-slate-600">
            Primary and secondary archetypes sit on top of continuous trait scores. Mixed profiles are expected.
          </p>
        </div>
      </section>

      <section className="mt-20 grid gap-6 md:grid-cols-3">
        {pillars.map((item) => (
          <article key={item.title} className="card">
            <h2 className="font-display text-2xl">{item.title}</h2>
            <p className="mt-3 text-slate-600">{item.body}</p>
          </article>
        ))}
      </section>

      <section className="mt-16 card">
        <h2 className="font-display text-3xl">What lives in the platform</h2>
        <ul className="mt-6 grid gap-3 md:grid-cols-2">
          {modules.map((item) => (
            <li key={item} className="rounded-2xl bg-lavender/70 px-4 py-3 dark:bg-slate-800">
              {item}
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-16 grid gap-6 md:grid-cols-3">
        <MarketingCard href="/personality-test" title="Free personality test" body="Quick Discovery and the IPIP-50 Big Five." />
        <MarketingCard href="/archetypes" title="Personality archetypes" body="Sixteen original descriptive patterns." />
        <MarketingCard href="/careers" title="Career interests" body="RIASEC-inspired exploration, not a job verdict." />
        <MarketingCard href="/leadership" title="Leadership preferences" body="How you like to lead — not whether you may." />
        <MarketingCard href="/relationships" title="Relationship communication" body="Consent-based comparison and discussion prompts." />
        <MarketingCard href="/coaching" title="AI personality coaching" body="Grounded guidance with a crisis protocol." />
      </section>

      <footer className="mt-20 flex flex-wrap gap-4 border-t border-slate-200 py-8 text-sm text-slate-500">
        <Link href="/legal/privacy">Privacy</Link>
        <Link href="/legal/terms">Terms</Link>
        <Link href="/legal/ai">Responsible AI</Link>
        <Link href="/help">Help</Link>
        <span>Adults 18+ · Educational use only</span>
      </footer>
    </div>
  );
}

function MarketingCard({ href, title, body }: { href: string; title: string; body: string }) {
  return (
    <Link href={href} className="card block hover:-translate-y-0.5 hover:border-indigo">
      <h3 className="font-display text-xl">{title}</h3>
      <p className="mt-2 text-slate-600">{body}</p>
    </Link>
  );
}

function Helix() {
  return (
    <svg className="absolute -right-8 -top-8 h-56 w-56 opacity-70" viewBox="0 0 200 200" aria-hidden>
      <path d="M40 20 C90 60, 110 80, 160 40" stroke="#6366F1" strokeWidth="6" fill="none" />
      <path d="M40 50 C90 90, 110 110, 160 70" stroke="#14B8A6" strokeWidth="6" fill="none" />
      <path d="M40 80 C90 120, 110 140, 160 100" stroke="#6366F1" strokeWidth="6" fill="none" />
      <path d="M40 110 C90 150, 110 170, 160 130" stroke="#14B8A6" strokeWidth="6" fill="none" />
      {[40, 70, 100, 130].map((y, i) => (
        <line key={y} x1={60 + i * 8} y1={y + 8} x2={140 - i * 6} y2={y + 28} stroke="#EDE9FE" strokeWidth="3" />
      ))}
    </svg>
  );
}
