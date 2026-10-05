"""Pouch-Belt Work Trousers: hard-wearing trousers with a wide belt of pouches and a coiled rope."""
from kit import belt, footwear, legs, pouch, waistband
from paint import solid

META = {
    "name": "Pouch-Belt Trousers",
    "description": "Hard-wearing trousers, a wide belt hung with pouches, and a coil of rope at the hip.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    for leg in legs(g, "P", "twill", 2301, base=1, rows=(0, 8)):
        leg.front.hline(0, 3, 5, "P0")
    waistband(g, "P", "twill", 2302, base=1)
    belt(g, "waist_belt", 9.4, height=2)
    pouch(g, "waist_pouch_left", (3.6, 10.6, -2.4), size=(2, 3, 2), flap="M3")
    pouch(g, "waist_pouch_back", (-1.4, 10.4, 2.8), size=(3, 2, 2))
    rope = g.piece("waist_rope_coil", "TORSO", (-1, 0, -1.5), (2, 3, 3), pivot=(-4.9, 10.2, .4), inflate=.05)
    for face in rope.faces:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "S3" if (x + y) % 2 else "S1")
    footwear(g, "boot", top=8)
