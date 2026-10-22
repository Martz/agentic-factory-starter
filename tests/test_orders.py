import unittest
from decimal import Decimal

from lunchbox import Order, money


class MoneyTest(unittest.TestCase):
    def test_rounds_half_up_to_the_penny(self):
        self.assertEqual(money("2.345"), Decimal("2.35"))
        self.assertEqual(money(3), Decimal("3.00"))


class OrderTest(unittest.TestCase):
    def setUp(self):
        self.order = Order()
        self.order.add("Ada", "Falafel wrap", "7.50", ("vegan",))
        self.order.add("Grace", "Chicken katsu", "9.95")
        self.order.add("Ada", "Lemonade", "2.20", ("vegan", "gf"))

    def test_total_is_sum_of_items(self):
        self.assertEqual(self.order.total(), Decimal("19.65"))

    def test_each_person_pays_for_their_own_items(self):
        self.assertEqual(self.order.per_person(), {"Ada": Decimal("9.70"), "Grace": Decimal("9.95")})

    def test_tags_are_normalised(self):
        self.assertEqual(self.order.items[2].tags, frozenset({"vegan", "gf"}))

    def test_people_are_sorted(self):
        self.assertEqual(self.order.people(), ["Ada", "Grace"])


class SplitEvenlyTest(unittest.TestCase):
    def make(self, prices):
        o = Order()
        for name, price in prices:
            o.add(name, "x", price)
        return o

    def test_exact_split(self):
        o = self.make([("Ann", "10.00"), ("Bob", "20.00"), ("Cy", "0.00")])
        self.assertEqual(o.split_evenly(), {"Ann": Decimal("10.00"), "Bob": Decimal("10.00"), "Cy": Decimal("10.00")})

    def test_leftover_pennies_alphabetical(self):
        o = self.make([("Cy", "10.00"), ("Ann", "0.00"), ("Bob", "0.00")])
        r = o.split_evenly()
        self.assertEqual(list(r.items()), [("Ann", Decimal("3.34")), ("Bob", Decimal("3.33")), ("Cy", Decimal("3.33"))])
        o = self.make([("Ann", "0.02"), ("Bob", "0.00"), ("Cy", "0.00")])
        self.assertEqual(list(o.split_evenly().values()), [Decimal("0.01"), Decimal("0.01"), Decimal("0.00")])

    def test_sums_to_total_and_decimal(self):
        for total in ("0.01", "7.00", "19.65", "100.03"):
            o = self.make([("A", total), ("B", "0.00"), ("C", "0.00"), ("D", "0.00"), ("E", "0.00"), ("F", "0.00"), ("G", "0.00")])
            r = o.split_evenly()
            self.assertEqual(sum(r.values()), o.total())
            self.assertEqual(len(r), 7)
            self.assertTrue(all(isinstance(v, Decimal) for v in r.values()))

    def test_empty_order(self):
        self.assertEqual(Order().split_evenly(), {})


if __name__ == "__main__":
    unittest.main()
