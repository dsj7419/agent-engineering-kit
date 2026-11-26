"""Composition root and command-line demonstration."""
from .application import place_order
from .domain import Line
from .infrastructure import MemoryOrderStore


def main():
    store = MemoryOrderStore()
    print(place_order('demo', (Line(350, 2),), store))


if __name__ == '__main__':
    main()
