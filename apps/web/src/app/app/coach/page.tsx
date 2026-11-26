"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { ErrorState, Loading } from "@/components/State";
import { api } from "@/lib/api";

type Message = { role: string; content: string; grounding?: Record<string, unknown> };

export default function CoachPage() {
  const [history, setHistory] = useState<{ id: string; title: string }[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api<{ id: string; title: string }[]>("/api/v1/coach/conversations")
      .then(setHistory)
      .catch((err) => setError(err.message));
  }, []);

  async function openConversation(id: string) {
    const data = await api<{ messages: Message[] }>(`/api/v1/coach/conversations/${id}`);
    setConversationId(id);
    setMessages(data.messages);
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const input = form.elements.namedItem("message") as HTMLInputElement;
    const text = input.value.trim();
    if (!text) return;
    setBusy(true);
    setError("");
    try {
      const path = conversationId
        ? `/api/v1/coach/conversations/${conversationId}/messages`
        : "/api/v1/coach/conversations";
      const result = await api<{ conversation_id: string; content: string; grounding?: Record<string, unknown>; agent: string }>(path, {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });
      setConversationId(result.conversation_id);
      setMessages((current) => [
        ...current,
        { role: "user", content: text },
        { role: "assistant", content: result.content, grounding: result.grounding },
      ]);
      setHistory(await api<{ id: string; title: string }[]>("/api/v1/coach/conversations"));
      input.value = "";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Coach unavailable");
    } finally {
      setBusy(false);
    }
  }

  return (
    <AppShell title="PersonalityDNA Coach">
      <p className="mb-4 max-w-2xl text-sm text-slate-600">
        Educational guidance only. Not a psychologist, therapist, or medical professional. Does not diagnose.
        If you are in crisis, contact emergency services or 988 (US) / IASP resources.
      </p>
      {error ? <ErrorState message={error} /> : null}
      <div className="grid gap-6 md:grid-cols-[240px_1fr]">
        <aside className="card h-fit">
          <h2 className="font-semibold">History</h2>
          <ul className="mt-3 space-y-2 text-sm">
            {history.map((item) => (
              <li key={item.id}>
                <button className="text-left text-indigo" onClick={() => openConversation(item.id)}>
                  {item.title}
                </button>
              </li>
            ))}
            {history.length === 0 ? <li className="text-slate-500">No conversations yet.</li> : null}
          </ul>
        </aside>
        <div className="card min-h-[420px] flex flex-col">
          <div className="flex-1 space-y-3 overflow-y-auto">
            {messages.length === 0 ? (
              <p className="text-slate-500">Ask about your profile, a conversation, a career experiment, or a habit.</p>
            ) : (
              messages.map((message, index) => (
                <div key={index} className={message.role === "user" ? "text-right" : ""}>
                  <div className={`inline-block max-w-[90%] rounded-2xl px-4 py-3 ${message.role === "user" ? "bg-indigo text-white" : "bg-lavender text-navy"}`}>
                    {message.content}
                  </div>
                </div>
              ))
            )}
          </div>
          <form className="mt-4 flex gap-2" onSubmit={onSubmit}>
            <input className="input" name="message" placeholder="Write to the coach" disabled={busy} />
            <button className="btn-primary" disabled={busy}>
              {busy ? "…" : "Send"}
            </button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
