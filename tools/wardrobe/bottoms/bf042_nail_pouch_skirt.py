"""Nail-Pouch Skirt: a sawdust-flecked twill skirt with a leather nail pouch tied over the front and laced ankle boots."""
from kit_female import shoes, skirt
from paint import rnd, solid

META = {
    "name": "Nail-Pouch Skirt",
    "gender": "female",
    "description": "A sawdust-flecked twill skirt with a leather nail pouch tied over the front and laced ankle boots.",
    "tags": ["work", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 14211, top=9.8, length=11)

    def sawdust(face):
        for y in range(face.h - 5, face.h):
            for x in range(face.w):
                if rnd(x + face.x0, y, 14212) < .12:
                    face.set(x, y, "S4")
    s.paint(sawdust)
    s.hem("P1")
    pouch = g.piece("nail_pouch", "TORSO", (0, 0, 0), (4, 4, 1), pivot=(-4.0, 9.4, -3.05), motion="flap_front")
    solid(pouch, "L", "leather", 14213, 2)
    f = pouch.front
    f.hline(0, 3, 0, "L3"), f.hline(0, 3, 1, "L1")
    for x, y in ((1, 0), (2, 0)):
        f.set(x, y, "M3")                                            # nail heads peeking out
    f.vline(2, 2, 3, "L1")
    tie = g.piece("waist_pouch_tie", "TORSO", (-5.5, 0, -3.05), (11, 1, 6), pivot=(0, 9.2, 0), inflate=.05)
    solid(tie, "L", "leather", 14214, 1, edge=False)
    shoes(g, "ankle", "L", 2)
