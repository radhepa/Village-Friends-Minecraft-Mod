"""Box-Pleated Skirt: a crisp wool skirt laid in box pleats, a coin purse on a chain and buckled shoes."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Box-Pleated Skirt",
    "gender": "female",
    "description": "A crisp ankle-length wool skirt laid in deep box pleats, a coin purse on a chain and buckled shoes.",
    "tags": ["tailored", "skirt", "long_skirt"],
}


def box_pleats(face):
    for x in range(face.w):
        phase = x % 4
        key = "P1" if phase == 0 else "P3" if phase == 1 else None
        if key:
            face.vline(x, 2, face.h - 2, key)


def build(g):
    s = skirt(g, "P", "weave", 12311, top=9.6, length=12, folds=False, gather=False)
    s.paint(box_pleats)
    s.hem("P0")
    chain = g.piece("waist_purse_chain", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(5.7, 9.6, -1.0))
    solid(chain, "M", "smooth", 12312, 3)
    purse = g.piece("waist_purse", "TORSO", (-.5, 0, -1), (1, 2, 2), pivot=(5.7, 12.4, -1.0))
    solid(purse, "A", "velvet", 12313, 2)
    purse.left.set(0, 0, "M3"), purse.left.set(1, 0, "M3")
    shoes(g, "shoe", "K", 2)
    for side in ("right", "left"):
        g.part(f"{side}_pants").front.hline(1, 2, 10, "M3")
