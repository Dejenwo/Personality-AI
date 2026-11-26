"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

export default function PublicHelp() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api<any[]>("/api/v1/help").then(setItems).catch(() => setItems([]));
  }, []);
  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <Link href="/" className="text-indigo">Home</Link>
      <h1 className="font-display mt-4 text-4xl">Help center</h1>
      <div className="mt-8 space-y-4">
        {items.map((item) => (
          <article key={item.slug} className="card">
            <h2 className="font-display text-2xl">{item.title}</h2>
            <p className="mt-2">{item.body}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
