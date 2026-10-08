"""Alchemist's Scorched Skirt: a calf-length work skirt whose hem is charred black and uneven, a few
small burn holes ringed with singed cloth where sparks landed, over tall cuffed boots."""
from kit_female import leg_ring_fold, shoes, skirt
from paint import rnd

META = {
    "name": "Alchemist's Scorched Skirt",
    "gender": "female",
    "description": "A calf-length work skirt with a charred, uneven hem and small singed burn holes, over tall cuffed boots.",
    "tags": ["work", "rugged", "skirt"],
}


def charred(face, seed):
    """An uneven burnt hem: black at the edge, brown singeing above, the odd ember still glowing."""
    for x in range(face.w):
        depth = 1 + (rnd(x, 1, seed) > .45) + (rnd(x, 2, seed) > .8)
        for d in range(depth):
            face.set(x, face.h - 1 - d, "K0" if d == 0 else "K1")
        face.set(x, face.h - 1 - depth, "L1")
        if rnd(x, 3, seed) > .85:
            face.set(x, face.h - 1 - depth, "A3")


def burn(face, x, y):
    """A small burn hole: a black centre ringed with scorched brown."""
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        face.set(x + dx, y + dy, "K0")
    for dx, dy in ((-1, 0), (2, 1), (0, -1), (1, 2)):
        if face.inside(x + dx, y + dy):
            face.set(x + dx, y + dy, "L1")


def build(g):
    s = skirt(g, "P", "weave", 55341, base=2, top=9.8, length=9, back_length=9, flare=5, folds=True, gather=True)
    for i, face in enumerate(s.faces):
        charred(face, 55342 + i)
    burn(s.front.front, 2, 4)
    burn(s.front.front, 7, 6)
    burn(s.back.back, 5, 3)
    shoes(g, "boot", "L", 2, top=6)
    leg_ring_fold(g, "boot_cuff", 5.4, "L", 2)
