"""External acceptance cases for B001; executed with candidate on PYTHONPATH."""
import unittest
from order.application import place_order
from order.domain import Line
from order.infrastructure import MemoryOrderStore


class DiscountAcceptance(unittest.TestCase):
    def test_discount_rounding_and_persistence(self):
        store = MemoryOrderStore()
        result = place_order('a', (Line(101, 1),), store, discount_percent=25)
        self.assertEqual(result, 76)
        self.assertEqual(store.read('a'), 76)

    def test_endpoints_and_default(self):
        for identifier, kwargs, expected in [('a', {}, 101), ('b', {'discount_percent': 0}, 101),
                                              ('c', {'discount_percent': 100}, 0)]:
            store = MemoryOrderStore()
            self.assertEqual(place_order(identifier, (Line(101, 1),), store, **kwargs), expected)
            self.assertEqual(store.read(identifier), expected)

    def test_invalid_discount_has_no_side_effect(self):
        for discount in (-1, 101, True, False, 1.5, '20', None):
            store = MemoryOrderStore()
            with self.subTest(discount=discount), self.assertRaises(ValueError):
                place_order('a', (Line(101, 1),), store, discount_percent=discount)
            with self.assertRaises(KeyError):
                store.read('a')


if __name__ == '__main__':
    unittest.main()
