import Link from "next/link";
export default function Page() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-sm text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">Big Five personality assessment</h1>
      <p className="mt-4 text-lg text-slate-600">IPIP Big-Five Factor Markers (50 items). Goldberg 1992. Public domain. Alphas reported by IPIP, not by our sample.</p>
      <Link className="btn-primary mt-8" href="/register">Take the Big Five</Link>
    </div>
  );
}
