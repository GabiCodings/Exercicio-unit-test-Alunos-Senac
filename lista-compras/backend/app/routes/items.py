"""Rotas REST para itens da lista de compras."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.services.item_service import ItemValidationError, item_service

bp = Blueprint("items", __name__, url_prefix="/api/items")


def _json_error(message: str, code: str, status: int) -> tuple:
    return jsonify({"error": message, "code": code}), status


@bp.get("")
def list_items():
    items = item_service.list_items()
    return jsonify([i.to_dict() for i in items])


@bp.get("/<int:item_id>")
def get_item(item_id: int):
    item = item_service.get_item(item_id)
    if item is None:
        return _json_error("Item não encontrado.", "not_found", 404)
    return jsonify(item.to_dict())


@bp.post("")
def create_item():
    data = request.get_json(silent=True) or {}
    try:
        item = item_service.create_item(
            name=data.get("name"),
            quantity=data.get("quantity"),
            purchased=data.get("purchased", False),
        )
    except ItemValidationError as e:
        return _json_error(e.message, e.code, 400)
    except (TypeError, ValueError):
        return _json_error("Payload inválido.", "invalid_payload", 400)
    return jsonify(item.to_dict()), 201


@bp.put("/<int:item_id>")
def update_item(item_id: int):
    data = request.get_json(silent=True) or {}
    try:
        item = item_service.update_item(
            item_id,
            name=data.get("name"),
            quantity=data.get("quantity"),
            purchased=data.get("purchased", False),
        )
    except ItemValidationError as e:
        return _json_error(e.message, e.code, 400)
    except (TypeError, ValueError):
        return _json_error("Payload inválido.", "invalid_payload", 400)
    if item is None:
        return _json_error("Item não encontrado.", "not_found", 404)
    return jsonify(item.to_dict())


@bp.delete("/<int:item_id>")
def delete_item(item_id: int):
    ok = item_service.delete_item(item_id)
    if not ok:
        return _json_error("Item não encontrado.", "not_found", 404)
    return "", 204
