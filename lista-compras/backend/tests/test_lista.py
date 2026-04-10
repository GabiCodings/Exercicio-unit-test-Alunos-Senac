import pytest

from unittest.mock import patch

from app.models.item import ShoppingItem


@patch("app.routes.items.item_service")
class TestRotaGetItems:
    """GET /api/items → função `list_items` em items.py (no client: getItems / buscar todos)."""

    def test_get_items_retorna_json_do_mock(self, mock_svc, client):
        mock_svc.list_items.return_value = [
            ShoppingItem(id=1, name="Leite", quantity=2, purchased=False),
            ShoppingItem(id=2, name="Pão", quantity=1, purchased=True),
        ]
        resp = client.get("/api/items")
        assert resp.status_code == 200

        assert resp.get_json() == [
            {"id": 1, "name": "Leite", "quantity": 2, "purchased": False },
            {"id": 2, "name": "Pão", "quantity": 1, "purchased": True },
        ]
    
        mock_svc.list_items.assert_called_once()
    
    def test_get_id_item_encontrado(self, mock_svc, client):
        mock_svc.get_item.return_value = ShoppingItem (
            id=2, name="Leite", quantity=2, purchased=False
        )
        resp = client.get("api/items/2")
        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Leite"
        mock_svc.get_item.assert_called_once_with(2)

    def test_get_id_item_nao_encontrado(self, mock_svc, client):
        mock_svc.get_item.return_value = None
        resp = client.get("api/items/999")
        assert resp.status_code == 404
        body = resp.get_json()
        assert body["code"] == "not_found"

@patch("app.routes.items.item_service")
class TestRotasCriacao:
    def test_item_criado(self, mock_svc, client):
        mock_svc.create_item.return_value = ShoppingItem(
            id=6, name="Batata", quantity=3, purchased=True
        )
        resp = client.post (
            "/api/items",
            json={
                "id": 6,
                "name": "Batata",
                "quantity": 3,
                "purchased": True,
            },
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["id"] == 6
        mock_svc.create_item.assert_called_once()

    def test_item_erro_400(self, mock_svc, client):
        mock_svc.create_item.side_effect = ItemValidationError(
            
        )
