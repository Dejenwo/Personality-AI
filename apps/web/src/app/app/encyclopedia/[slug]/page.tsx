"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Section = { id: number; part: string; part_title: string; title: string; content: any; limitations: string; reflection_questions: string[] };

export default function EncyclopediaProfilePage() {
  const { slug } = useParams<{ slug: string }>();
  const [entry, setEntry] = useState<any>(null);
  const [open, setOpen] = useState<number | null>(1);
  const [error, setError] = useState("");
  useEffect(() => {
    api(`/api/v1/life/encyclopedia/${slug}`)
      .then(setEntry)
      .catch((err) => setError(err.message));
  }, [slug]);
  if (error) return <AppShell title="Encyclopedia"><ErrorState message={error} /></AppShell>;
  if (!entry) return <AppShell title="Encyclopedia"><Loading /></AppShell>;
  const parts = entry.parts as { id: string; title: string }[];
  return (
    <AppShell title={`${entry.preference_code} · ${entry.title}`}>
      <p className="text-slate-500">{entry.original_archetype_name}</p>
      <p className="mt-4 max-w-3xl">{entry.overview}</p>
      <p className="mt-4 max-w-3xl text-sm text-slate-600">{entry.disclaimer}</p>
      {parts.map((part) => (
        <section key={part.id} className="mt-8">
          <h2 className="font-display text-2xl">Part {part.id} · {part.title}</h2>
          <div className="mt-3 space-y-2">
            {(entry.sections as Section[])
              .filter((section) => section.part === part.id)
              .map((section) => (
                <article key={section.id} className="card">
                  <button className="w-full text-left" onClick={() => setOpen(open === section.id ? null : section.id)}>
                    <h3 className="font-display text-xl">{section.id}. {section.title}</h3>
                  </button>
                  {open === section.id ? (
                    <div className="mt-3 space-y-2 text-sm text-slate-700">
                      {section.content?.explanation ? <p>{section.content.explanation}</p> : null}
                      {Array.isArray(section.content?.items) ? (
                        <ul className="list-disc pl-5">
                          {section.content.items.slice(0, 12).map((item: any, index: number) => (
                            <li key={index}>{typeof item === "string" ? item : item.name || item.title || item.prompt}</li>
                          ))}
                        </ul>
                      ) : null}
                      <p className="text-slate-500">{section.limitations}</p>
                    </div>
                  ) : null}
                </article>
              ))}
          </div>
        </section>
      ))}
    </AppShell>
  );
}
