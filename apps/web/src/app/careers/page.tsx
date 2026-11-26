import Link from "next/link";
export default function Page() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-sm text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">Career interests</h1>
      <p className="mt-4 text-lg text-slate-600">RIASEC-inspired original items. Interests are not skills. Not for hiring.</p>
      <Link className="btn-primary mt-8" href="/register">Explore careers</Link>
    </div>
  );
}
