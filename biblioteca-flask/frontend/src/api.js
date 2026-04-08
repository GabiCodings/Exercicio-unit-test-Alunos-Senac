/**
 * Chamadas à API Flask (em dev, o Vite encaminha /api para o backend).
 * Base relativa: funciona com o proxy do Vite.
 */

const BASE = "/api/books";

export async function fetchBooks() {
  const r = await fetch(BASE);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function fetchBook(id) {
  const r = await fetch(`${BASE}/${id}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createBook(payload) {
  const r = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

export async function updateBook(id, payload) {
  const r = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

export async function deleteBook(id) {
  const r = await fetch(`${BASE}/${id}`, { method: "DELETE" });
  if (!r.ok) {
    const data = await r.json().catch(() => ({}));
    throw new Error(data.error || r.statusText);
  }
}
