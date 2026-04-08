import { useCallback, useEffect, useState } from "react";
import { createItem, deleteItem, fetchItems, updateItem } from "./api.js";

const empty = { name: "", quantity: 1, purchased: false };

export default function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState(null);
  const [msg, setMsg] = useState(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      setItems(await fetchItems());
    } catch (e) {
      setError(e.message || "Erro ao carregar.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  function onChange(e) {
    const { name, value, type, checked } = e.target;
    setForm((f) => ({
      ...f,
      [name]: type === "checkbox" ? checked : name === "quantity" ? Number(value) : value,
    }));
  }

  async function onSubmit(e) {
    e.preventDefault();
    setMsg(null);
    const payload = {
      name: form.name,
      quantity: form.quantity,
      purchased: form.purchased,
    };
    try {
      if (editingId != null) {
        await updateItem(editingId, payload);
        setMsg("Item atualizado.");
      } else {
        await createItem(payload);
        setMsg("Item adicionado.");
      }
      setForm(empty);
      setEditingId(null);
      await load();
    } catch (err) {
      setMsg(err.message || "Erro ao salvar.");
    }
  }

  function edit(item) {
    setEditingId(item.id);
    setForm({
      name: item.name,
      quantity: item.quantity,
      purchased: item.purchased,
    });
    setMsg(null);
  }

  function cancel() {
    setEditingId(null);
    setForm(empty);
  }

  async function remove(id) {
    if (!window.confirm("Remover este item?")) return;
    setMsg(null);
    try {
      await deleteItem(id);
      setMsg("Item removido.");
      if (editingId === id) cancel();
      await load();
    } catch (err) {
      setMsg(err.message || "Erro ao remover.");
    }
  }

  async function togglePurchased(item) {
    setMsg(null);
    try {
      await updateItem(item.id, {
        name: item.name,
        quantity: item.quantity,
        purchased: !item.purchased,
      });
      await load();
    } catch (err) {
      setMsg(err.message || "Erro ao atualizar.");
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Lista de compras</h1>
        <p className="sub">Gerencie itens: nome, quantidade e se já foi comprado.</p>
      </header>

      {error && <div className="banner err">{error}</div>}
      {msg && <div className="banner ok">{msg}</div>}

      <section className="card">
        <h2>{editingId != null ? "Editar item" : "Novo item"}</h2>
        <form onSubmit={onSubmit} className="form">
          <label>
            Nome *
            <input name="name" value={form.name} onChange={onChange} required />
          </label>
          <label>
            Quantidade * (mín. 1)
            <input
              name="quantity"
              type="number"
              min={1}
              value={form.quantity}
              onChange={onChange}
              required
            />
          </label>
          <label className="check">
            <input
              type="checkbox"
              name="purchased"
              checked={form.purchased}
              onChange={onChange}
            />
            Já comprado
          </label>
          <div className="row">
            <button type="submit">{editingId != null ? "Salvar" : "Adicionar"}</button>
            {editingId != null && (
              <button type="button" className="sec" onClick={cancel}>
                Cancelar
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="card">
        <h2>Itens</h2>
        {loading ? (
          <p>Carregando…</p>
        ) : items.length === 0 ? (
          <p className="muted">Lista vazia.</p>
        ) : (
          <ul className="list">
            {items.map((it) => (
              <li key={it.id} className={it.purchased ? "done" : ""}>
                <div className="main">
                  <button
                    type="button"
                    className="tick"
                    title="Marcar comprado / pendente"
                    onClick={() => togglePurchased(it)}
                  >
                    {it.purchased ? "✓" : "○"}
                  </button>
                  <div>
                    <strong>{it.name}</strong>
                    <span className="meta">
                      Qtd: {it.quantity}
                      {it.purchased ? " · comprado" : ""}
                    </span>
                  </div>
                </div>
                <div className="acts">
                  <button type="button" onClick={() => edit(it)}>
                    Editar
                  </button>
                  <button type="button" className="danger" onClick={() => remove(it.id)}>
                    Excluir
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
