"""Fruit Seller's Ruffled Skirt: a long swinging skirt banded with three narrow gathered ruffles stepped down
its length, the last edged in the accent color, over low shoes tied with ribbon."""
from kit import SIDES
from kit_female import shoes, skirt, tier
from paint import k

META = {
    "name": "Fruit Seller's Ruffled Skirt",
    "gender": "female",
    "description": "A long swinging skirt banded with three narrow gathered ruffles down its length, the last edged in color, over ribbon-tied shoes.",
    "tags": ["whimsical", "casual", "skirt", "long_skirt"],
}

SEED = 53315


def build(g):
    s = skirt(g, "P", "weave", SEED, top=9.8, length=12, flare=6)
    for i, y in enumerate((3, 6, 9)):
        for f in tier(g, s, f"ruffle_{i}", y, 2 if i < 2 else 3, role="P", seed=SEED + 1 + i, grow=2 + i, flare=7 + 2 * i):
            for x in range(f.w):
                f.set(x, 0, k("P", 3 if x % 2 else 1))
                f.set(x, 1, k("P", 2 if x % 2 else 1))
            if f.h > 2:
                for x in range(f.w):
                    f.set(x, 2, "A2" if x % 2 else "A1")
    shoes(g, "shoe", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(1, 2, 10, "A3")
        pants.right.set(3, 10, "A2"), pants.left.set(0, 10, "A2")
