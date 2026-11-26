export function Loading({ label = "Loading" }: { label?: string }) {
  return (
    <div className="card animate-pulse" role="status" aria-live="polite">
      <p className="text-slate-500">{label}…</p>
    </div>
  );
}

export function Empty({ title, body, action }: { title: string; body: string; action?: React.ReactNode }) {
  return (
    <div className="card text-center">
      <h2 className="font-display text-2xl">{title}</h2>
      <p className="mt-2 text-slate-600 dark:text-slate-300">{body}</p>
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="card border-rose-200 bg-rose-50 text-rose-900" role="alert">
      {message}
    </div>
  );
}

export function Success({ message }: { message: string }) {
  return (
    <div className="card border-teal/40 bg-teal/10 text-teal" role="status">
      {message}
    </div>
  );
}
