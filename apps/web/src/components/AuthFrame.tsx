import Link from "next/link";

export function AuthFrame({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4">
      <Link href="/" className="font-display mb-8 text-2xl">
        PersonalityDNA AI
      </Link>
      <div className="card">
        <h1 className="font-display text-3xl">{title}</h1>
        <p className="mt-2 text-slate-600">{subtitle}</p>
        {children}
      </div>
    </div>
  );
}
