"use client";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";
export default function Page() {
  return (
    <AppShell title="Accessibility settings">
      <div className="card max-w-3xl">
        <p>Target: WCAG 2.2 AA. Use your browser zoom, system text size, and reduced-motion preference. Touch targets are at least 44px in primary actions.</p>
        
      </div>
    </AppShell>
  );
}
