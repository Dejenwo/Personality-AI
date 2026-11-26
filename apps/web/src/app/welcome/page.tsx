import Link from "next/link";

export default function WelcomePage() {
  return (
    <div className="mx-auto flex min-h-screen max-w-lg flex-col justify-center px-4">
      <h1 className="font-display text-4xl">Welcome</h1>
      <p className="mt-4 text-slate-600">
        PersonalityDNA AI is a continuous development practice. You will take assessments, read a
        profile, talk with an educational coach, and return to habits and journals over time.
      </p>
      <div className="mt-8 flex gap-3">
        <Link className="btn-primary" href="/intro">
          How it works
        </Link>
        <Link className="btn-secondary" href="/register">
          Create account
        </Link>
      </div>
    </div>
  );
}
