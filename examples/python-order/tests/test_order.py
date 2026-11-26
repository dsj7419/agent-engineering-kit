"""Behavior and integration checks for the example order context."""
import unittest
from order.application import place_order
from order.domain import Line, subtotal
from order.infrastructure import MemoryOrderStore


class OrderTests(unittest.TestCase):
    def test_integer_totals(self):
        self.assertEqual(subtotal((Line(199, 3), Line(50, 2))), 697)
        self.assertEqual(subtotal(()), 0)

    def test_invalid_line(self):
        for price, quantity in ((-1, 1), (10, 0), (1.5, 1), (True, 1), (1, True)):
            with self.subTest(price=price, quantity=quantity), self.assertRaises(ValueError):
                Line(price, quantity)

    def test_persisted_total(self):
        store = MemoryOrderStore()
        self.assertEqual(place_order('a', (Line(350, 2),), store), 700)
        self.assertEqual(store.read('a'), 700)

    def test_invalid_order(self):
        store = MemoryOrderStore()
        with self.assertRaises(ValueError):
            place_order('a', (), store)
        with self.assertRaises(KeyError):
            store.read('a')

    def test_duplicate_does_not_overwrite(self):
        store = MemoryOrderStore()
        place_order('a', (Line(100, 1),), store)
        with self.assertRaises(ValueError):
            place_order('a', (Line(200, 1),), store)
        self.assertEqual(store.read('a'), 100)
