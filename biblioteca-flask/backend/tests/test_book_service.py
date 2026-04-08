"""
Testes unitários das regras de negócio (serviço de livros).

Aqui NÃO subimos servidor HTTP e NÃO mockamos o serviço:
testamos `validate_book_payload` e `BookService` de forma direta.
"""

from unittest.mock import patch

import pytest

from app.models.book import Book
from app.services.book_service import (
    BookService,
    BookValidationError,
    validate_book_payload,
)


class TestValidateBookPayload:
    """Regras puras: fácil de testar sem Flask nem banco."""

    def test_titulo_obrigatorio(self):
        # Vai obrigatoriamente levantar uma exceção BookValidationError
        with pytest.raises(BookValidationError) as exc:
            validate_book_payload("", "Autor", 2020)
        assert exc.value.code == "title_required"
        assert exc.value.message == "O título é obrigatório."

    def test_autor_obrigatorio(self):
        with pytest.raises(BookValidationError) as exc:
            validate_book_payload("Título", None, 2020)
        assert exc.value.code == "author_required"

    def test_ano_obrigatorio(self):
        with pytest.raises(BookValidationError) as exc:
            validate_book_payload("Título", "Autor", None)
        assert exc.value.code == "year_required"
 
    def test_isbn_tamanho_invalido(self):
        with pytest.raises(BookValidationError) as exc:
            validate_book_payload("Título", "Autor", 2020, isbn="123")
        assert exc.value.code == "isbn_invalid_length"


class TestBookServiceCrud:
    """Operações do serviço com armazenamento em memória isolado por teste."""

    @pytest.fixture
    def svc(self):
        s = BookService()
        return s

    def test_criar_e_listar(self, svc):
        b = svc.create_book("Dom Casmurro", "Machado de Assis", 1899)
        b2 = svc.create_book("Dom Casmurro 2", "Machado de Assis", 1899)

        assert b.id == 1
        assert len(svc.list_books()) == 2

    def test_buscar_inexistente_retorna_none(self, svc):
        b = svc.create_book("Dom Casmurro", "Machado de Assis", 1899)
        assert svc.get_book(99) is None

    def test_atualizar_inexistente_retorna_none(self, svc):
        assert (
            svc.update_book(1, "X", "Y", 2000) is None
        )

    def test_remover_inexistente_retorna_false(self, svc):
        assert svc.delete_book(1) is False

    def test_fluxo_completo(self, svc):
        b = svc.create_book("Livro", "Autor", 2020, isbn="9783161484100")
        got = svc.get_book(b.id)
        assert got is not None
        assert got.title == "Livro"

        upd = svc.update_book(b.id, "Novo título", "Autor", 2021)
        assert upd is not None
        assert upd.title == "Novo título"

        assert svc.delete_book(b.id) is True
        assert svc.get_book(b.id) is None
