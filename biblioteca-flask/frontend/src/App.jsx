import { useCallback, useEffect, useState } from "react";
import {
  createBook,
  deleteBook,
  fetchBooks,
  updateBook,
} from "./api.js";

const emptyForm = {
  title: "",
  author: "",
  year: "",
  isbn: "",
};

export default function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      const data = await fetchBooks();
      setBooks(data);
    } catch (e) {
      setError(e.message || "Erro ao carregar livros.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage(null);
    const payload = {
      title: form.title,
      author: form.author,
      year: form.year === "" ? null : Number(form.year),
      isbn: form.isbn || null,
    };
    try {
      if (editingId != null) {
        await updateBook(editingId, payload);
        setMessage("Livro atualizado.");
      } else {
        await createBook(payload);
        setMessage("Livro cadastrado.");
      }
      setForm(emptyForm);
      setEditingId(null);
      await load();
    } catch (err) {
      setMessage(err.message || "Erro ao salvar.");
    }
  }

  function startEdit(book) {
    setEditingId(book.id);
    setForm({
      title: book.title,
      author: book.author,
      year: String(book.year),
      isbn: book.isbn || "",
    });
    setMessage(null);
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function handleDelete(id) {
    if (!window.confirm("Remover este livro?")) return;
    setMessage(null);
    try {
      await deleteBook(id);
      setMessage("Livro removido.");
      if (editingId === id) cancelEdit();
      await load();
    } catch (err) {
      setMessage(err.message || "Erro ao remover.");
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Biblioteca</h1>
        <p className="subtitle">CRUD de livros — Flask + React</p>
      </header>

      {error && <div className="banner error">{error}</div>}
      {message && <div className="banner ok">{message}</div>}

      <section className="card">
        <h2>{editingId != null ? "Editar livro" : "Novo livro"}</h2>
        <form onSubmit={handleSubmit} className="form">
          <label>
            Título *
            <input
              name="title"
              value={form.title}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Autor *
            <input
              name="author"
              value={form.author}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Ano *
            <input
              name="year"
              type="number"
              value={form.year}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            ISBN (opcional)
            <input name="isbn" value={form.isbn} onChange={handleChange} />
          </label>
          <div className="actions">
            <button type="submit">
              {editingId != null ? "Salvar alterações" : "Cadastrar"}
            </button>
            {editingId != null && (
              <button type="button" className="secondary" onClick={cancelEdit}>
                Cancelar edição
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="card">
        <h2>Acervo</h2>
        {loading ? (
          <p>Carregando…</p>
        ) : books.length === 0 ? (
          <p className="muted">Nenhum livro cadastrado.</p>
        ) : (
          <ul className="book-list">
            {books.map((b) => (
              <li key={b.id} className="book-item">
                <div>
                  <strong>{b.title}</strong>
                  <span className="meta">
                    {b.author} · {b.year}
                    {b.isbn ? ` · ISBN ${b.isbn}` : ""}
                  </span>
                </div>
                <div className="row-actions">
                  <button type="button" onClick={() => startEdit(b)}>
                    Editar
                  </button>
                  <button
                    type="button"
                    className="danger"
                    onClick={() => handleDelete(b.id)}
                  >
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
