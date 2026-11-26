"""An in-memory adapter for local demonstrations, not production persistence."""


class MemoryOrderStore:
    def __init__(self):
        self._totals = {}

    def save(self, order_id, total_cents):
        if order_id in self._totals:
            raise ValueError('duplicate order')
        self._totals[order_id] = total_cents

    def read(self, order_id):
        return self._totals[order_id]
