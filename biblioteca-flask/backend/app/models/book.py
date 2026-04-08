"""Modelo de domínio: Livro."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Book:
    """Representa um livro no acervo."""

    id: int
    title: str
    author: str
    year: int
    isbn: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Book":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            author=str(data["author"]),
            year=int(data["year"]),
            isbn=data.get("isbn"),
        )
