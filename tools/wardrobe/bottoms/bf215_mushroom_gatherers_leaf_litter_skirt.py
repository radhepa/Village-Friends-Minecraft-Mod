"""Mushroom Gatherer's Leaf-Litter Skirt: an ankle-length skirt embroidered with fallen leaves drifting
thicker toward the hem, a forage bag at the hip, wool stockings and wooden clogs."""
from kit import SIDES, footwear
from kit_female import side_pouch, skirt, stockings_row
from paint import grid
from wardrobe import shade

META = {
    "name": "Mushroom Gatherer's Leaf-Litter Skirt",
    "gender": "female",
    "description": "An ankle-length wool skirt embroidered with fallen leaves drifting thicker toward the hem, a "
                   "drawstring forage bag at the hip and wooden clogs.",
    "tags": ["casual", "long_skirt", "skirt"],
}

LEAF = ["..a", ".ab", "ca."]
# Leaves drift down in rows, thicker toward the hem: (x, rows above the hem, color).
LEAVES = [(0, 4, "A2"), (3, 4, "L3"), (6, 4, "A2"), (9, 4, "L3"), (1, 8, "L3"), (5, 8, "A2"), (8, 11, "L3"),
          (3, 12, "A2")]


def leaf(face, x, y, key):
    grid(face, x, y, LEAF, {"a": key, "b": shade(key, 1), "c": "L1"})


def build(g):
    s = skirt(g, "P", "weave", 57521, top=9.8, length=11, side_length=10, flare=5, folds=False)
    s.hem("P1")
    for n, face in enumerate(s.wide_faces):
        for x, y, key in LEAVES:
            leaf(face, (x + 2 * n) % face.w, face.h - 1 - y, key)
    for box in (s.right, s.left):
        face = box.right if box is s.right else box.left
        leaf(face, 1, face.h - 5, "A2")
    stockings_row(g, "S", 9, 9, base=2)
    footwear(g, "clog", top=10, role="L", base=3)
    for side in SIDES:
        g.part(f"{side}_pants").front.hline(0, 3, 10, "L4")
    bag = side_pouch(g, "waist_forage_bag", "right", y=9.6, size=(2, 3, 2), role="L")
    bag.top.fill("S2")
    for face in bag.sides:
        face.hline(0, face.w - 1, 0, "S3")
