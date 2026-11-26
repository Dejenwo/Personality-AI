"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function LegalPage() {
  const { slug } = useParams<{ slug: string }>();
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api(`/api/v1/legal/${slug}`).then(setData).catch(() => setData({ body: "Pending legal review before commercial launch." }));
  }, [slug]);
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <h1 className="font-display text-4xl capitalize">{slug}</h1>
      <p className="mt-6 whitespace-pre-wrap text-slate-700">{data?.body}</p>
    </div>
  );
}
