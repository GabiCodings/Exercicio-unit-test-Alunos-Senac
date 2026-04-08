const BASE = "/api/items";

export async function fetchItems() {
  const r = await fetch(BASE);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function createItem(payload) {
  const r = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

export async function updateItem(id, payload) {
  const r = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}

export async function deleteItem(id) {
  const r = await fetch(`${BASE}/${id}`, { method: "DELETE" });
  if (!r.ok) {
    const data = await r.json().catch(() => ({}));
    throw new Error(data.error || r.statusText);
  }
}
