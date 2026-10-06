"""Fur-Collared Traveling Coat: a warm wool coat with a thick fur collar, toggles, fur cuffs and a belt."""
from kit import belt, body, flaps, sleeves
from paint import rnd, solid

META = {
    "name": "Fur-Collared Coat",
    "gender": "male",
    "description": "A thick wool traveling coat with a heavy fur collar, toggle fastenings and fur-trimmed cuffs.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def fur(box, seed):
    for face in box.faces:
        for y in range(face.h):
            for x in range(face.w):
                r = rnd(x, y, seed + face.x0)
                face.set(x, y, "S4" if r > .72 else "S2" if r < .22 else "S3")


def build(g):
    body(g, "P", "weave", 2301)
    coat = body(g, "P", "weave", 2302, layer="jacket")
    cf = coat.front
    cf.vline(4, 0, 11, "P0"), cf.vline(3, 0, 11, "P3")
    for y in (2, 5, 8):
        cf.set(3, y, "L3"), cf.set(4, y, "L2"), cf.set(5, y, "M3")
    for face in (coat.right, coat.left):
        face.vline(2, 0, 11, "P1")
    sleeves(g, "P", "weave", 2303, rows=(0, 9))
    sleeves(g, "P", "weave", 2304, rows=(0, 7), layer="sleeve")
    collar = g.piece("fur_collar", "TORSO", (-5, -1.6, -3.0), (10, 3, 6), inflate=.05)
    fur(collar, 2305)
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        cuff = g.piece(f"{side}_fur_cuff", bone, (ox - .55, 6.8, -2.55), (5, 2, 5))
        fur(cuff, 2306 + (side == "left"))
    belt(g, "belt", 9.0)
    front, back = flaps(g, "coat_skirt", 5, "P", "weave", 2308, top=11.2)
    front.vline(4, 0, 4, "P0")
    for face in (front, back):
        face.hline(0, 8, 4, "P1")
