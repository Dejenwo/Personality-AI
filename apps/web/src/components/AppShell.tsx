"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const TABS = [
  { href: "/app", label: "Home", icon: "◎" },
  { href: "/app/discover", label: "Discover", icon: "✦" },
  { href: "/app/guidance", label: "Guidance", icon: "◇" },
  { href: "/app/coach", label: "AI Coach", icon: "◈" },
  { href: "/app/growth", label: "My Growth", icon: "△" },
];

export function AppShell({ children, title }: { children: React.ReactNode; title?: string }) {
  const pathname = usePathname();
  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 pb-24 pt-6 md:pb-10 md:pt-8">
      <header className="mb-6 flex items-center justify-between">
        <Link href="/app" className="font-display text-xl text-navy dark:text-white">
          PersonalityDNA
        </Link>
        <nav className="hidden gap-6 md:flex" aria-label="Primary">
          {TABS.map((tab) => {
            const active = pathname === tab.href || (tab.href !== "/app" && pathname.startsWith(tab.href));
            return (
              <Link key={tab.href} href={tab.href} className={active ? "tab-active font-semibold" : "text-slate-500"}>
                {tab.label}
              </Link>
            );
          })}
        </nav>
      </header>
      {title ? <h1 className="font-display mb-6 text-3xl">{title}</h1> : null}
      <main className="flex-1">{children}</main>
      <nav
        className="fixed bottom-0 left-0 right-0 z-20 grid grid-cols-5 border-t border-slate-200 bg-white/95 px-2 py-2 backdrop-blur md:hidden dark:border-slate-800 dark:bg-slate-950/95"
        aria-label="Mobile"
      >
        {TABS.map((tab) => {
          const active = pathname === tab.href || (tab.href !== "/app" && pathname.startsWith(tab.href));
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={`flex min-h-12 flex-col items-center justify-center text-xs ${active ? "text-indigo" : "text-slate-500"}`}
            >
              <span aria-hidden className="text-base">
                {tab.icon}
              </span>
              {tab.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
