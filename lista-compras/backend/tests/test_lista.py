import pytest

from unittest.mock import patch

from app.models.item import ShoppingItem
from app.routes.items import list_items


@patch("app.routes.items.items_service")
class TestItems:
    def test_pegar_item_lista(self, mock_svc, client):
        mock_svc.list_items.return_value = [
            ShoppingItem(id=1, name="Gabi", quantity=2, purchased=True),        
            ]
        resp = client.get("/api/items")
        assert resp.status_code == 200

        assert resp.get_json() == [
            {'id': 1, "name": "Gabi", "quantity": 2, "purchased": True},
        ]

        mock_svc.list_items.assert_called_once()