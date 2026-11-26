import Link from "next/link";

export default function SplashPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <p className="text-sm uppercase tracking-[0.3em] text-teal">PersonalityDNA AI</p>
      <h1 className="font-display mt-4 text-5xl">Know the pattern. Keep becoming.</h1>
      <Link className="btn-primary mt-10" href="/welcome">
        Enter
      </Link>
    </div>
  );
}
