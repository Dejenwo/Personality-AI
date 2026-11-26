export function apiUrl(path: string, base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") {
  return `${base.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;
}
