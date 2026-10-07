"""Houppelande Bodice: a high-waisted velvet houppelande with a standing fur collar and vast fur-trimmed funnel sleeves."""
from kit import body, sleeves
from kit_female import arm_rings, fur_box, pleats
from paint import solid

META = {
    "name": "Houppelande Bodice",
    "gender": "female",
    "description": "A high-waisted velvet houppelande, belted under the bust, with a fur collar and vast fur-edged funnel sleeves.",
    "tags": ["fancy", "gown", "robe"],
    "locked_to": "bf053_houppelande_skirt",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 15301)
    for face in b.sides:
        pleats(face, "P", 2, 2, y0=6, lit=False)
    b.front.clear(3, 0), b.front.clear(4, 0)
    sleeves(g, "P", "velvet", 15302, rows=(0, 11))
    belt = g.piece("high_belt", "TORSO", (-4.6, 4.4, -2.6), (9, 2, 5), inflate=.06)
    solid(belt, "A", "plain", 15303, 2, edge=False)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "M3")
    belt.front.set(4, 1, "M4")
    collar = g.piece("fur_collar", "TORSO", (-4.6, -1.8, -2.7), (9, 3, 5), inflate=.08)
    fur_box(collar, "S", 15304, 3)
    for box in arm_rings(g, "funnel_sleeve", 1.5, 8, 7, inflate=.05):
        solid(box, "P", "velvet", 15305, 2)
        for face in box.sides:
            pleats(face, "P", 2, 2, y0=1, lit=False)
        box.bottom.fill("A1")
    for box in arm_rings(g, "funnel_fur", 9.5, 2, 7, inflate=.15):
        fur_box(box, "S", 15306, 3)
