import Link from "next/link";
export default function Page() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-sm text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">Leadership preferences</h1>
      <p className="mt-4 text-lg text-slate-600">Educational inventory of how you like to lead. Not a competency score.</p>
      <Link className="btn-primary mt-8" href="/register">Open leadership</Link>
    </div>
  );
}
