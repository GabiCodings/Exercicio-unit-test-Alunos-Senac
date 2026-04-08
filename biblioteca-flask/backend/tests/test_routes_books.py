"""
Testes unitários das rotas HTTP com MOCK do `book_service`.

Ideia didática:
- As rotas só orquestram: JSON de entrada/saída e códigos HTTP.
- O "cérebro" (regras, banco) está em `BookService`.
- Substituímos `book_service` por um Mock: assim o teste da rota não cria
  livros de verdade nem acerta regras de negócio — isso já foi testado
  em `test_book_service.py`.

Isso NÃO é teste de integração: não há servidor real nem camadas reais
empilhadas; apenas Flask test_client + mock.
"""

from unittest.mock import patch

from app.models.book import Book
from app.services.book_service import BookValidationError


# Substitui app.routes.books.book_service por um objeto falso (MagicMock) só durante
# este teste. Assim a rota HTTP não usa o BookService real: configuramos o retorno
# com .return_value e verificamos status/JSON. Ao terminar o teste, o patch restaura
# o book_service original no módulo das rotas.

@patch("app.routes.books.book_service")
class TestRotasListagemEBusca:
    def test_get_lista_retorna_json_do_mock(self, mock_svc, client):
        """Testa se a rota /api/books retorna um JSON com os livros corretos."""
        mock_svc.list_books.return_value = [
            Book(id=1, title="A", author="B", year=2020, isbn=None),
        ]
        resp = client.get("/api/books")
        assert resp.status_code == 200

        assert resp.get_json() == [
            {"id": 1, "title": "A", "author": "B", "year": 2020, "isbn": None},
        ]
        mock_svc.list_books.assert_called_once()

    def test_get_por_id_encontrado(self, mock_svc, client):
        mock_svc.get_book.return_value = Book(
            id=2, title="X", author="Y", year=2019, isbn=None
        )
        resp = client.get("/api/books/2")
        assert resp.status_code == 200
        assert resp.get_json()["title"] == "X"
        mock_svc.get_book.assert_called_once_with(2)

    def test_get_por_id_nao_encontrado(self, mock_svc, client):
        mock_svc.get_book.return_value = None
        resp = client.get("/api/books/999")
        assert resp.status_code == 404
        body = resp.get_json()
        assert body["code"] == "not_found"


@patch("app.routes.books.book_service")
class TestRotasCriacao:
    def test_post_criado_201(self, mock_svc, client):
        mock_svc.create_book.return_value = Book(
            id=5, title="Novo", author="Autor", year=2024, isbn="9783161484100"
        )
        resp = client.post(
            "/api/books",
            json={
                "title": "Novo",
                "author": "Autor",
                "year": 2024,
                "isbn": "9783161484100",
            },
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["id"] == 5
        mock_svc.create_book.assert_called_once()

    def test_post_validacao_400(self, mock_svc, client):
        mock_svc.create_book.side_effect = BookValidationError(
            "O título é obrigatório.", code="title_required"
        )
        resp = client.post("/api/books", json={})
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "title_required"


@patch("app.routes.books.book_service")
class TestRotasAtualizacao:
    def test_put_atualizado_200(self, mock_svc, client):
        mock_svc.update_book.return_value = Book(
            id=1, title="Editado", author="A", year=2023, isbn=None
        )
        resp = client.put(
            "/api/books/1",
            json={"title": "Editado", "author": "A", "year": 2023},
        )
        assert resp.status_code == 200
        assert resp.get_json()["title"] == "Editado"

    def test_put_nao_encontrado_404(self, mock_svc, client):
        mock_svc.update_book.return_value = None
        resp = client.put(
            "/api/books/1",
            json={"title": "X", "author": "Y", "year": 2020},
        )
        assert resp.status_code == 404


@patch("app.routes.books.book_service")
class TestRotasExclusao:
    def test_delete_sem_conteudo_204(self, mock_svc, client):
        mock_svc.delete_book.return_value = True
        resp = client.delete("/api/books/3")
        assert resp.status_code == 204
        mock_svc.delete_book.assert_called_once_with(3)

    def test_delete_nao_encontrado_404(self, mock_svc, client):
        mock_svc.delete_book.return_value = False
        resp = client.delete("/api/books/99")
        assert resp.status_code == 404


def test_rota_post_payload_invalido_tipo(client):
    """Sem patch: exercita o except TypeError/ValueError da rota."""
    with patch("app.routes.books.book_service") as mock_svc:
        mock_svc.create_book.side_effect = ValueError("ano inválido")
        resp = client.post(
            "/api/books",
            json={"title": "A", "author": "B", "year": "não-numérico"},
        )
        assert resp.status_code == 400
        assert resp.get_json()["code"] == "invalid_payload"
