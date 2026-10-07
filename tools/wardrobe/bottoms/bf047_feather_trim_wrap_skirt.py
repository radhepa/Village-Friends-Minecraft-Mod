"""Feather-Trim Wrap Skirt: an ankle-length wrap skirt whose overlapping edge is embroidered with feathers, tied at the hip."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Feather-Trim Wrap Skirt",
    "gender": "female",
    "description": "An ankle-length wrap skirt with feathers embroidered down its overlapping edge, tied at the hip, and soft boots.",
    "tags": ["casual", "rugged", "skirt", "long_skirt"],
}

FEATHER = [".a", "ab", "ab", ".c"]


def build(g):
    s = skirt(g, "P", "weave", 14711, top=9.8, length=11, folds=False)
    f = s.front.front
    f.vline(6, 1, 10, "P0")
    for y in range(1, 10, 4):
        for dy, row in enumerate(FEATHER):
            for dx, ch in enumerate(row):
                if ch != ".":
                    f.set(7 + dx, y + dy, {"a": "S3", "b": "A2", "c": "L2"}[ch])
    s.hem("P1")
    for i, (z, length) in enumerate(((-2.2, 5), (-1.4, 4))):
        tie = g.piece(f"waist_wrap_tie_{i}", "TORSO", (-.5, 0, -.5), (1, length, 1), pivot=(5.6, 9.8, z))
        solid(tie, "P", "weave", 14712, 2)
    shoes(g, "boot", "L", 2, top=9)
