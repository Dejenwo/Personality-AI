"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Language settings">
      <div className="card max-w-3xl">
        <p>English is the first release. Additional languages require reviewed localization. Translating items does not automatically preserve validity.</p>
        
      </div>
    </AppShell>
  );
}
