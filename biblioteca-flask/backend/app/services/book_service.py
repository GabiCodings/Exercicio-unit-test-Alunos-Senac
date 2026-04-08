"""
Regras de negócio e persistência em memória (didático).

Em um projeto real, a persistência viria de um repositório/ORM;
aqui mantemos tudo explícito para os testes de regras serem puros.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.models.book import Book


def _current_year() -> int:
    return datetime.now().year


class BookValidationError(Exception):
    """Erro de validação de dados de livro."""

    def __init__(self, message: str, code: str = "validation_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


def validate_book_payload(
    title: str | None,
    author: str | None,
    year: int | None,
    isbn: str | None = None,
) -> None:
    """
    Regras de negócio para criação/atualização de livros.

    Levanta BookValidationError se alguma regra for violada.
    """
    if title is None or not str(title).strip(): #Verifica se o título é nulo ou vazio
        raise BookValidationError("O título é obrigatório.", code="title_required")
    if author is None or not str(author).strip():
        raise BookValidationError("O autor é obrigatório.", code="author_required")
    if year is None:
        raise BookValidationError("O ano é obrigatório.", code="year_required")

    y = int(year)
    min_year = 1000
    max_year = _current_year() + 1
    if y < min_year or y > max_year:
        raise BookValidationError(
            f"O ano deve estar entre {min_year} e {max_year}.",
            code="year_out_of_range",
        )

    if isbn is not None and str(isbn).strip():
        digits = "".join(c for c in str(isbn) if c.isdigit() or c == "X")
        if len(digits) not in (10, 13):
            raise BookValidationError(
                "ISBN deve ter 10 ou 13 dígitos (hífens são ignorados).",
                code="isbn_invalid_length",
            )


class BookService:
    """Serviço de livros com armazenamento em memória."""

    def __init__(self) -> None:
        self._next_id = 1
        self._books: dict[int, Book] = {}

    def list_books(self) -> list[Book]:
        return list(self._books.values())

    def get_book(self, book_id: int) -> Book | None:
        return self._books.get(book_id)

    def create_book(
        self,
        title: str,
        author: str,
        year: int,
        isbn: str | None = None,
    ) -> Book:
        validate_book_payload(title, author, year, isbn)
        bid = self._next_id
        self._next_id += 1
        book = Book(
            id=bid,
            title=str(title).strip(),
            author=str(author).strip(),
            year=int(year),
            isbn=str(isbn).strip() if isbn and str(isbn).strip() else None,
        )
        self._books[bid] = book
        return book

    def update_book(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        isbn: str | None = None,
    ) -> Book | None:
        if book_id not in self._books:
            return None
        validate_book_payload(title, author, year, isbn)
        book = Book(
            id=book_id,
            title=str(title).strip(),
            author=str(author).strip(),
            year=int(year),
            isbn=str(isbn).strip() if isbn and str(isbn).strip() else None,
        )
        self._books[book_id] = book
        return book

    def delete_book(self, book_id: int) -> bool:
        if book_id not in self._books:
            return False
        del self._books[book_id]
        return True

    # Útil em testes: reinicia o estado sem subir outro processo
    def reset(self) -> None:
        self._next_id = 1
        self._books.clear()


# Instância usada pela aplicação (rotas importam este objeto)
book_service = BookService()
