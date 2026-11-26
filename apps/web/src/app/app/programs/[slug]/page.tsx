"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function ProgramPage() {
  const { slug } = useParams<{ slug: string }>();
  const [program, setProgram] = useState<any>(null);
  const [enrollment, setEnrollment] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/growth/programs/${slug}`).then(setProgram);
  }, [slug]);
  if (!program) return <AppShell title="Program"><p>Loading…</p></AppShell>;
  return (
    <AppShell title={program.name}>
      <p className="max-w-2xl text-slate-600">{program.summary}</p>
      <ul className="mt-4 list-disc pl-5">
        {(program.objectives || []).map((item: string) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
      <button
        className="btn-primary mt-6"
        onClick={async () => {
          const row = await api(`/api/v1/growth/programs/${slug}/enroll`, { method: "POST" });
          setEnrollment(row);
        }}
      >
        Enroll
      </button>
      {enrollment ? <p className="mt-4">Enrolled · current day {enrollment.current_day}</p> : null}
      <div className="mt-6 space-y-3">
        {(program.days_content || []).map((day: any) => (
          <article key={day.day} className="card">
            <h2 className="font-display text-xl">Day {day.day}: {day.title}</h2>
            <p className="mt-2">{day.exercise}</p>
            <p className="mt-2 text-slate-600">{day.reflection}</p>
          </article>
        ))}
      </div>
    </AppShell>
  );
}
