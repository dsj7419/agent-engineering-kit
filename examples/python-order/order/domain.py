"""Order pricing rules; independent of storage and presentation."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    unit_cents: int
    quantity: int

    def __post_init__(self):
        if type(self.unit_cents) is not int or self.unit_cents < 0:
            raise ValueError('unit_cents must be a nonnegative integer')
        if type(self.quantity) is not int or self.quantity <= 0:
            raise ValueError('quantity must be a positive integer')

    @property
    def total_cents(self):
        return self.unit_cents * self.quantity


def subtotal(lines):
    """Return the sum of line totals in integer cents."""
    return sum(line.total_cents for line in lines)
