"""Trapper's Fur Mantle: a heavy pelt mantle over a wool tunic, fur cuffs, and two brush tails hanging from the belt."""
from kit import belt, body, neckline, sleeves
from kit_male import blk, fur, fur_face, shoulder_cape

META = {
    "name": "Trapper's Fur Mantle",
    "gender": "male",
    "description": "A winter trapper's heavy pelt mantle over a wool tunic, fur at the cuffs and two brush tails hanging from the belt.",
    "tags": ["rugged", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 8101)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 8102, rows=(0, 10))
    for side in ("right", "left"):
        fur_face(g.part(f"{side}_sleeve").strip, "L", 8103, 3, rows=range(8, 11))
    mantle = shoulder_cape(g, "pelt_mantle", "L", "leather", 8104, length=4, width=12, depth=6)
    fur(mantle, "L", 8105, 3)
    for face in mantle.sides:
        for x in range(face.w):
            if x % 3 == 1:
                face.set(x, 3, "L1")                                     # ragged pelt edge
    mantle.front.vline(6, 0, 3, "L0")
    blk(g, "mantle_tie", (0, .6, -3.2), (2, 1, 1), "L", 1, "leather", 8106, edge=False)
    belt(g, "belt", 9.6)
    for i, (x, rz) in enumerate(((-3.0, 8), (3.0, -8))):
        tail = blk(g, f"brush_tail_{i}", (x, 10.4, -2.8), (1, 5, 1), "L", 3, "plain", 8107 + i,
                   rotation=(0, 0, rz), motion="sway")
        fur(tail, "L", 8109 + i, 3)
        tail.strip.hline(0, tail.strip.w - 1, 4, "S4")                   # pale tip
