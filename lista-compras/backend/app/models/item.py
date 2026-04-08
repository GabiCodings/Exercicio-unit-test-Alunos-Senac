"""Modelo de domínio: item da lista de compras."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ShoppingItem:
    id: int
    name: str
    quantity: int
    purchased: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "purchased": self.purchased,
        }
