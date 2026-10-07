"""Pearl-Netted Bodice: a velvet bodice veiled in a lattice of pearls, over full linen sleeves banded with pearl strings."""
from kit_female import bodice, chemise
from paint import solid

META = {
    "name": "Pearl-Netted Bodice",
    "gender": "female",
    "description": "A velvet bodice veiled in a lattice of pearls, a pearl choker and full linen sleeves banded with pearls.",
    "tags": ["fancy"],
}


def build(g):
    body, arms = chemise(g, "S", 4, "weave", 15901, neckline="wide", sleeve_rows=(0, 11))
    for arm in arms:
        for y in (3, 7):
            arm.strip.hline(0, 15, y, "M4")
            for x in range(1, 16, 2):
                arm.strip.set(x, y, "S2")
        for x in range(1, 16, 3):
            arm.strip.vline(x, 0, 2, "S3"), arm.strip.vline(x, 4, 6, "S3"), arm.strip.vline(x, 8, 10, "S3")
        arm.strip.hline(0, 15, 11, "S2")
    b = bodice(g, "P", "velvet", 15902, rows=(2, 10), neckline="square", point=True, edge="M3")
    for face in (b.front, b.back):
        for y in range(3, 11):
            for x in range(face.w):
                if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                    face.set(x, y, "S4" if (x + y) % 8 == 0 else "M3")
    choker = g.piece("pearl_choker", "TORSO", (-4.5, -.9, -2.55), (9, 1, 5), inflate=.06)
    solid(choker, "S", "plain", 15903, 4, edge=False)
    for face in choker.sides:
        for x in range(1, face.w, 2):
            face.set(x, 0, "M3")
    drop = g.piece("pearl_drop", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(0, .2, -2.65), inflate=.05)
    solid(drop, "S", "plain", 15904, 4, edge=False)
    drop.front.set(0, 1, "A2")
