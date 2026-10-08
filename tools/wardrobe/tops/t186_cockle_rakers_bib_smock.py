"""Cockle Raker's Bib Smock: a short smock with a square canvas bib stitched across the chest, sleeves pushed up,
a short-toothed cockle rake hung at the hip and a dripping net bag of cockles slung on the back."""
from kit import belt, body, flaps, neckline, roll, sleeves
from kit_male import blk
from paint import fabric, line

META = {
    "name": "Cockle Raker's Bib Smock",
    "gender": "male",
    "description": "A short smock with a square canvas bib stitched across the chest, sleeves pushed up, a short-toothed "
                   "cockle rake hung at the hip and a dripping net bag of cockles slung on the back.",
    "tags": ["work", "sea", "simple"],
    "covers_waist": True,
}

RAKE = (2.5, 9.6, -3.4)      # the rake's handle loops over the belt here; handle, head and teeth share the hinge
BAG = (-1.2, 4.0, 2.9)


def build(g):
    b = body(g, "P", "weave", 33600)
    neckline(b.front, "round", "P")
    # The bib: a square of stiff canvas across the chest, zigzag-stitched round its edge.
    f = b.front
    fabric(f, "S", "twill", 33601, 3, 1, 1, 6, 6)
    f.hline(1, 6, 1, "S4")
    for x in range(1, 7):
        f.set(x, 6, "S1" if x % 2 else "S2")
    for y in range(1, 7):
        f.set(1, y, "S2" if y % 2 else "S1"), f.set(6, y, "S2" if y % 2 else "S1")
    f.clear(3, 0), f.clear(4, 0), f.set(3, 1, "S1"), f.set(4, 1, "S1")
    sleeves(g, "P", "weave", 33602, rows=(0, 5))
    roll(g, "P", 3.4, base=3)
    # The bag's strap, from the left shoulder across the chest to the right hip and back up to the bag.
    line(f, 7, 0, 7, 0, "L2")
    jacket = g.part("jacket")
    line(jacket.back, 1, 0, 4, 4, "L2"), jacket.top.vline(6, 0, 3, "L2")
    belt(g, "belt", 9.4, height=1)
    # The cockle rake: a short ash handle hooked over the belt, a cross-head and a comb of short iron teeth.
    handle = blk(g, "cockle_rake_handle", RAKE, (1, 4, 1), "L", 3, "plain", 33603, origin=(-.5, 0, -.5),
                 motion="flap_front")
    handle.strip.hline(0, handle.strip.w - 1, 0, "L1")
    head = blk(g, "cockle_rake_head", RAKE, (4, 1, 1), "L", 2, "plain", 33604, origin=(-2.0, 4.0, -.5),
               motion="flap_front", edge=False)
    head.front.set(0, 0, "L3"), head.front.set(3, 0, "L1")
    teeth = blk(g, "cockle_rake_teeth", RAKE, (4, 2, 1), "M", 2, "smooth", 33605, origin=(-2.0, 5.0, -.5),
                motion="flap_front", edge=False)
    for face in (teeth.front, teeth.back):
        for x in range(4):
            face.set(x, 0, "M3" if x % 2 == 0 else "M1")
            face.set(x, 1, "M3" if x % 2 == 0 else "K1")
    # The net bag of cockles on the back: pale ribbed shells behind a cord mesh, wet at the bottom.
    bag = blk(g, "cockle_bag", BAG, (4, 5, 2), "S", 3, "plain", 33606, origin=(-2, 0, 0))
    for face in bag.faces:
        for y in range(face.h):
            for x in range(face.w):
                if (x + y) % 3 == 0:
                    face.set(x, y, "L2")                                     # cord mesh
                else:
                    face.set(x, y, "S4" if (x * 2 + y) % 5 == 1 else "S3" if y < face.h - 1 else "S1")
    neck = blk(g, "cockle_bag_neck", BAG, (2, 1, 1), "L", 2, "plain", 33607, origin=(-1, -1.0, .5), edge=False)
    neck.top.fill("L3")
    for face in flaps(g, "smock_hem", 3, "P", "weave", 33608, top=11.0):
        face.hline(0, 8, 2, "P1")
        for x in (2, 6):
            face.vline(x, 0, 1, "P1")
