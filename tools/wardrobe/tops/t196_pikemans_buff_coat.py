"""Pikeman's Buff Coat: a thick buff-leather coat with cloth sleeves, a steel gorget and a field sash."""
from kit import SIDES, body, flaps, sleeves
from kit_male import blk
from kit_m04 import baldric, hanging
from paint import solid, strip_fabric

META = {
    "name": "Pikeman's Buff Coat",
    "gender": "male",
    "description": "A thick coat of pale buff leather hooked shut down the front, with tabbed skirts, colored cloth sleeves, "
                   "a steel gorget at the throat and a field sash knotted at the hip.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}

S = 34000


def build(g):
    b = body(g, "L", "leather", S, base=3)
    f = b.front
    f.vline(3, 1, 11, "L4"), f.vline(4, 1, 11, "L1")                      # the thick lapped front edge
    for y in (2, 4, 6, 8, 10):
        f.set(4, y, "M3")                                                  # hooks and eyes
    for face in b.sides:
        face.hline(0, face.w - 1, 9, "L2")                                 # waist seam
    b.right.vline(1, 0, 11, "L2"), b.left.vline(2, 0, 11, "L2")
    b.back.vline(3, 0, 11, "L2"), b.back.vline(4, 0, 11, "L4")
    sleeves(g, "P", "weave", S + 1, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.front.vline(0, 1, 7, "P1")
        sl = g.part(f"{side}_sleeve")
        strip_fabric(sl, "L", "leather", S + 2, 3, 0, 1)                    # buff shoulder welt
        sl.strip.hline(0, sl.strip.w - 1, 1, "L2")
        strip_fabric(sl, "L", "leather", S + 3, 3, 8, 10)                   # turned-back buff cuffs
        sl.strip.hline(0, sl.strip.w - 1, 8, "L4"), sl.strip.hline(0, sl.strip.w - 1, 10, "L1")
    # Steel gorget with a small breast plate at the throat.
    gorget = g.piece("gorget", "TORSO", (-4.5, -1.2, -2.7), (9, 2, 5), inflate=.08)
    solid(gorget, "M", "smooth", S + 4, 2, edge=False)
    for face in gorget.sides:
        face.hline(0, face.w - 1, 0, "M4"), face.hline(0, face.w - 1, 1, "M2")
    bib = g.piece("gorget_bib", "TORSO", (-3, 0, -1), (6, 2, 1), pivot=(0, .8, -2.35))
    solid(bib, "M", "smooth", S + 5, 2)
    bib.front.hline(0, 5, 0, "M3"), bib.front.hline(1, 4, 1, "M2")
    bib.front.set(0, 1, "M1"), bib.front.set(5, 1, "M1"), bib.front.set(1, 0, "M4"), bib.front.set(4, 0, "M4")
    # Field sash over the right shoulder, knotted at the left hip.
    baldric(g, "right", "A", 2, rows=9)
    knot = blk(g, "sash_knot", (2.7, 8.6, -2.3), (2, 2, 1), "A", 2, "plain", S + 6, origin=(-1, 0, -1))
    knot.front.set(0, 0, "A3"), knot.front.set(1, 1, "A1")
    for i, (x, y, n) in enumerate(((2.3, 10.6, 4), (3.2, 10.6, 3))):
        tail = hanging(g, f"sash_tail_{i}", x, y, (1, n, 1), "A", 2, "plain", S + 7 + i, top=10.8, dz=-.05)
        tail.front.set(0, n - 1, "A1"), tail.front.set(0, 0, "A3")
    # Skirts of buff leather cut into broad tabs.
    for face in flaps(g, "coat_skirt", 4, "L", "leather", S + 9, base=3, top=10.8, slit=True):
        face.vline(2, 1, 3, "L1"), face.vline(6, 1, 3, "L1")
        face.hline(0, 8, 3, "L2")
