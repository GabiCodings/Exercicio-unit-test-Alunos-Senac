"""Rotas REST para livros."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.services.book_service import BookValidationError, book_service

bp = Blueprint("books", __name__, url_prefix="/api/books")


def _json_error(message: str, code: str, status: int) -> tuple:
    return jsonify({"error": message, "code": code}), status


@bp.get("")
def list_books():
    books = book_service.list_books()
    return jsonify([b.to_dict() for b in books])


@bp.get("/<int:book_id>")
def get_book(book_id: int):
    book = book_service.get_book(book_id)
    if book is None:
        return _json_error("Livro não encontrado.", "not_found", 404)
    return jsonify(book.to_dict())


@bp.post("")
def create_book():
    data = request.get_json(silent=True) or {}
    try:
        book = book_service.create_book(
            title=data.get("title"),
            author=data.get("author"),
            year=data.get("year"),
            isbn=data.get("isbn"),
        )
    except BookValidationError as e:
        return _json_error(e.message, e.code, 400)
    except (TypeError, ValueError):
        return _json_error("Payload inválido.", "invalid_payload", 400)
    return jsonify(book.to_dict()), 201


@bp.put("/<int:book_id>")
def update_book(book_id: int):
    data = request.get_json(silent=True) or {}
    try:
        book = book_service.update_book(
            book_id,
            title=data.get("title"),
            author=data.get("author"),
            year=data.get("year"),
            isbn=data.get("isbn"),
        )
    except BookValidationError as e:
        return _json_error(e.message, e.code, 400)
    except (TypeError, ValueError):
        return _json_error("Payload inválido.", "invalid_payload", 400)
    if book is None:
        return _json_error("Livro não encontrado.", "not_found", 404)
    return jsonify(book.to_dict())


@bp.delete("/<int:book_id>")
def delete_book(book_id: int):
    ok = book_service.delete_book(book_id)
    if not ok:
        return _json_error("Livro não encontrado.", "not_found", 404)
    return "", 204
