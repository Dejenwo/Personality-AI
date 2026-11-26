import Link from "next/link";
export default function Page() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-sm text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">AI personality coaching</h1>
      <p className="mt-4 text-lg text-slate-600">Grounded in authorized results. Crisis protocol. Not a therapist.</p>
      <Link className="btn-primary mt-8" href="/register">Meet the coach</Link>
    </div>
  );
}
