"""Fur-Trimmed Houppelande: a pleated, belted overgown with a fur collar, bag sleeves and a fur hem."""
from kit import belt, body, flaps, sleeves
from paint import fabric, k, rnd, solid

META = {
    "name": "Fur-Trimmed Houppelande",
    "description": "A townsman's pleated overgown: high fur collar, deep bag sleeves, belt and fur-edged hem.",
    "tags": ["fancy", "robe"],
    "covers_waist": True,
}


def fur(box, seed):
    """Soft fur: secondary tufts with highlights and shaded roots."""
    for face in box.faces:
        for y in range(face.h):
            for x in range(face.w):
                r = rnd(x, y, seed + face.x0)
                face.set(x, y, "S4" if r > .7 else "S2" if r < .25 else "S3")


def build(g):
    b = body(g, "P", "velvet", 1701)
    for face in b.sides:
        for x in range(0, face.w, 2):
            face.vline(x, 3, 11, "P1")                    # pleats
    b.front.vline(4, 0, 11, "P0")
    sleeves(g, "P", "velvet", 1702, rows=(0, 9))
    belt(g, "belt", 7.6, buckle="M")
    collar = g.piece("fur_collar", "TORSO", (-4.6, -1.4, -2.7), (9, 3, 5), inflate=.08)
    fur(collar, 1703)
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        bag = g.piece(f"{side}_bag_sleeve", bone, (ox - .8, 3.6, -2.8), (5, 6, 5), inflate=.15)
        solid(bag, "P", "velvet", 1704, 2)
        for face in bag.sides:
            for x in range(0, face.w, 2):
                face.vline(x, 1, 4, "P1")
            face.hline(0, face.w - 1, 5, "S3")
        bag.bottom.fill("P0")
    front, back = flaps(g, "gown", 7, "P", "velvet", 1705, top=11.2)
    for face in (front, back):
        for x in range(0, 9, 2):
            face.vline(x, 1, 5, "P1")
        for x in range(9):
            face.set(x, 6, "S4" if x % 2 else "S3")
