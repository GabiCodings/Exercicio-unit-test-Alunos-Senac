"""Regras de negócio e persistência em memória."""

from __future__ import annotations

from app.models.item import ShoppingItem


class ItemValidationError(Exception):
    def __init__(self, message: str, code: str = "validation_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


def validate_item_payload(
    name: str | None,
    quantity: int | None,
    purchased: bool | None = None,
) -> None:
    if name is None or not str(name).strip():
        raise ItemValidationError("O nome do item é obrigatório.", code="name_required")
    if quantity is None:
        raise ItemValidationError("A quantidade é obrigatória.", code="quantity_required")
    q = int(quantity)
    if q < 1:
        raise ItemValidationError("A quantidade deve ser pelo menos 1.", code="quantity_invalid")
    if purchased is not None and not isinstance(purchased, bool):
        raise ItemValidationError("O campo purchased deve ser true ou false.", code="purchased_invalid")


class ItemService:
    def __init__(self) -> None:
        self._next_id = 1
        self._items: dict[int, ShoppingItem] = {}

    def list_items(self) -> list[ShoppingItem]:
        return list(self._items.values())

    def get_item(self, item_id: int) -> ShoppingItem | None:
        return self._items.get(item_id)

    def create_item(self, name: str, quantity: int, purchased: bool = False) -> ShoppingItem:
        validate_item_payload(name, quantity, purchased)
        iid = self._next_id
        self._next_id += 1
        item = ShoppingItem(
            id=iid,
            name=str(name).strip(),
            quantity=int(quantity),
            purchased=bool(purchased),
        )
        self._items[iid] = item
        return item

    def update_item(
        self,
        item_id: int,
        name: str,
        quantity: int,
        purchased: bool = False,
    ) -> ShoppingItem | None:
        if item_id not in self._items:
            return None
        validate_item_payload(name, quantity, purchased)
        item = ShoppingItem(
            id=item_id,
            name=str(name).strip(),
            quantity=int(quantity),
            purchased=bool(purchased),
        )
        self._items[item_id] = item
        return item

    def delete_item(self, item_id: int) -> bool:
        if item_id not in self._items:
            return False
        del self._items[item_id]
        return True

    def reset(self) -> None:
        self._next_id = 1
        self._items.clear()


item_service = ItemService()
