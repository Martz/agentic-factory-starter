"""Group lunch orders: who ordered what, and who owes how much."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP

PENNY = Decimal("0.01")


def money(value: Decimal | str | int | float) -> Decimal:
    """Convert to Decimal pounds rounded to the penny (half-up)."""
    return Decimal(str(value)).quantize(PENNY, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Item:
    person: str
    name: str
    price: Decimal
    tags: frozenset[str] = frozenset()


@dataclass
class Order:
    items: list[Item] = field(default_factory=list)

    def add(self, person: str, name: str, price: Decimal | str, tags: tuple[str, ...] = ()) -> Item:
        item = Item(person=person.strip(), name=name.strip(), price=money(price), tags=frozenset(t.strip().lower() for t in tags if t.strip()))
        self.items.append(item)
        return item

    def people(self) -> list[str]:
        return sorted({i.person for i in self.items})

    def subtotal(self) -> Decimal:
        return sum((i.price for i in self.items), Decimal("0.00"))

    def total(self) -> Decimal:
        return self.subtotal()

    def split_evenly(self) -> dict[str, Decimal]:
        """Equal shares; leftover pennies go one each to people in alphabetical order."""
        people = self.people()
        if not people:
            return {}
        pennies = int(self.total() / PENNY)
        base, extra = divmod(pennies, len(people))
        return {p: money(Decimal(base + (1 if n < extra else 0)) / 100) for n, p in enumerate(people)}

    def per_person(self) -> dict[str, Decimal]:
        """Each person pays for their own items."""
        owed = {p: Decimal("0.00") for p in self.people()}
        for i in self.items:
            owed[i.person] += i.price
        return owed
