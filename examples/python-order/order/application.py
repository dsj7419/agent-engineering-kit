"""Use case and consumer-owned persistence contract."""
from typing import Protocol
from .domain import Line, subtotal


class OrderStore(Protocol):
    def save(self, order_id: str, total_cents: int) -> None: ...


def place_order(order_id: str, lines: tuple[Line, ...], store: OrderStore) -> int:
    """Validate the request, compute the subtotal, and persist it."""
    if not order_id or not lines:
        raise ValueError('order requires an ID and at least one line')
    total = subtotal(lines)
    store.save(order_id, total)
    return total
