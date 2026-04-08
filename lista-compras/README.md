# Lista de compras — API Flask + React

Projeto pronto para uso em aula: **CRUD de itens** na lista de compras. O **pytest** está nas dependências e a pasta `tests/` contém apenas `conftest.py` (fixtures). **Os testes são uma atividade para vocês implementarem.**

---

## Como rodar o projeto

### Backend (porta **5001** — evita conflito com outros Flask na 5000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Abra o endereço indicado pelo Vite (ex.: `http://127.0.0.1:5174`). Deixe o backend rodando; o proxy encaminha `/api` para `http://127.0.0.1:5001`.

---

## Funcionalidades da API (CRUD)

Base URL: **`/api/items`**

| Método | Rota | Descrição |
|--------|------|-----------|
| **GET** | `/api/items` | **Listar** todos os itens da lista. Resposta: JSON array de objetos. |
| **GET** | `/api/items/<id>` | **Buscar** um item pelo `id`. Se não existir: **404** com `code: "not_found"`. |
| **POST** | `/api/items` | **Criar** item. Corpo JSON (ex.): `name`, `quantity`, opcionalmente `purchased` (padrão `false`). Sucesso: **201** + objeto criado. Validação falhou: **400** com `error` e `code`. |
| **PUT** | `/api/items/<id>` | **Atualizar** item. Corpo JSON: `name`, `quantity`, `purchased`. Se o `id` não existir: **404**. Validação: **400**. Sucesso: **200** + objeto. |
| **DELETE** | `/api/items/<id>` | **Remover** item. Sucesso: **204** sem corpo. Se não existir: **404**. |

### Campos de um item

| Campo | Tipo | Regra |
|-------|------|--------|
| `id` | inteiro | Gerado pelo servidor ao criar. |
| `name` | string | Obrigatório; não pode ser vazio nem só espaços. |
| `quantity` | inteiro | Obrigatório; deve ser **≥ 1**. |
| `purchased` | boolean | Se o item já foi comprado (`true` / `false`). |

Os códigos de erro em JSON seguem o padrão `{"error": "...", "code": "..."}` (por exemplo `name_required`, `quantity_invalid`, `not_found`, `invalid_payload`).

O código das rotas está em `backend/app/routes/items.py`. O serviço usado pelas rotas é o objeto **`item_service`** importado nesse mesmo módulo.

---

## Atividade (entrega)

**Objetivo:** escrever **testes unitários das rotas** usando **`unittest.mock.patch`** para substituir o **`item_service`** no módulo das rotas (`app.routes.items`), como visto em aula com o projeto da biblioteca.

**O que fazer**

1. Crie um ou mais arquivos em `backend/tests/`, por exemplo `test_routes_items.py`.
2. Para **cada operação do CRUD** da API (listar, buscar por id, criar, atualizar, remover), escreva testes que:
   - usem o **`client`** da fixture do `conftest.py`;
   - façam **`patch`** em `"app.routes.items.item_service"` (nome usado **no arquivo das rotas**);
   - configure o mock com `return_value` ou `side_effect` conforme o caso;
   - verifiquem **código HTTP** e, quando fizer sentido, o **JSON** retornado ou que o método certo do serviço foi chamado (`assert_called_once_with`, etc.).

**O que não é pedido nesta atividade**

- Testes de integração com servidor real na rede.
- Testes do `ItemService` em separado (foco é **só as rotas** com mock do serviço).
- Testes do frontend.

**Dica:** o `test_client` do Flask executa o fluxo real das rotas **sem** abrir porta; o que você mocka é só a camada **`item_service`**.

---

## Exemplo de teste (modelo)

Use como ponto de partida — **não copie sem adaptar**; complete com os demais casos (404, 400, PUT, DELETE, etc.).

```python
from unittest.mock import patch

from app.models.item import ShoppingItem


@patch("app.routes.items.item_service")
def test_get_lista_retorna_json_do_mock(mock_svc, client):
    mock_svc.list_items.return_value = [
        ShoppingItem(id=1, name="Leite", quantity=2, purchased=False),
    ]
    resp = client.get("/api/items")
    assert resp.status_code == 200
    assert resp.get_json() == [
        {"id": 1, "name": "Leite", "quantity": 2, "purchased": False},
    ]
    mock_svc.list_items.assert_called_once()
```

Para rodar os testes (após criar os arquivos):

```bash
cd backend
source .venv/bin/activate
pytest -v
```

---

## Estrutura do projeto

```
lista-compras/
  README.md                 ← este arquivo
  backend/
    app/
      models/item.py
      services/item_service.py
      routes/items.py
    run.py
    requirements.txt
    pytest.ini
    tests/
      conftest.py           ← fixtures `app` e `client`
  frontend/                 ← React (Vite)
```

Boa prática e bons testes.
