"""Mountain Herder's Goat-Hair Vest: an open vest of long shaggy goat hair with a ragged hem, over a
shirt with embroidered cuffs, and a cow-horn signal horn on a baldric at the hip."""
from kit_f07 import front_hung
from kit_female import chemise, trim
from paint import k, rnd, solid
from wardrobe import shade

META = {
    "name": "Mountain Herder's Goat-Hair Vest",
    "gender": "female",
    "description": "An open vest of long shaggy goat hair with a ragged hem, over a linen shirt with embroidered "
                   "cuffs, and a cow-horn signal horn hung on a baldric at the hip.",
    "tags": ["rugged", "casual"],
}


def shag(face, role="P", base=2, seed=0, x0=0, x1=None):
    """Long goat hair: vertical locks with lit crowns and shaded partings, waving every few rows."""
    x1 = face.w - 1 if x1 is None else x1
    for y in range(face.h):
        for x in range(x0, x1 + 1):
            lock = (x + face.x0 + y // 4) % 3
            s = base + (1 if lock == 0 else -1 if lock == 2 else 0)
            if lock == 1 and rnd(x + face.x0, y // 3, seed) > .8:
                s += 1
            face.set(x, y, k(role, s))


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 58001, neckline="slit", sleeve_rows=(0, 11))
    for arm in arms:
        trim(arm.strip, 8, "double", "A2")
        arm.strip.hline(0, 15, 11, "S2")
    j = g.part("jacket")
    for face in (j.right, j.left, j.back):
        shag(face, "P", 2, 58002)
    shag(j.front, "P", 2, 58003, 0, 2), shag(j.front, "P", 2, 58003, 5, 7)
    for x in (2, 5):
        for y in range(12):
            j.front.set(x, y, shade(j.front.get(x, y), 1 if x == 2 else -1))   # the open edges
    shag(j.top, "P", 3, 58004)
    for x in range(3, 5):
        j.top.vline(x, 0, j.top.h - 1, None)
    for face in j.sides:
        for x in range(face.w):
            if face.get(x, 11) and (x + face.x0) % 3 == 1:
                face.clear(x, 11)                                    # ragged ends of the hair
    # The shaggy hem hanging past the waist: two front panels and the back.
    for name, x, w, z, motion in (("right", -3.0, 3, -2.85, "flap_front"), ("left", 3.0, 3, -2.85, "flap_front"),
                                  ("back", 0.0, 9, 1.85, "flap_back")):
        flap = g.piece(f"vest_hem_{name}", "TORSO", (-w / 2, 0, 0), (w, 3, 1), pivot=(x, 11.2, z), motion=motion)
        solid(flap, "P", "plain", 58005, 2)
        face = flap.back if name == "back" else flap.front
        shag(face, "P", 2, 58006)
        for xx in range(w):
            face.set(xx, 2, "P1" if xx % 2 else face.get(xx, 2))
    # A baldric from the right shoulder to the horn at the left hip.
    for y in range(0, 9):
        x = min(7, y)
        if x not in (3, 4):
            j.front.set(x, y, "L2")
    for y in range(0, 8):
        j.back.set(7 - y, y, "L1")
    mid = front_hung(g, "signal_horn", 3.2, (-.5, 0, -1.5), (1, 2, 1), role="L", seed=58007, base=3, top=8.4)
    mid.front.set(0, 0, "L4")
    bell = front_hung(g, "signal_horn_bell", 3.2, (-1, 2, -2), (2, 2, 2), role="L", seed=58008, base=3, top=8.4)
    bell.bottom.fill("L0"), bell.bottom.set(0, 0, "L1")              # the open bell
    for face in bell.sides:
        face.hline(0, face.w - 1, 0, "M3")                          # a brass ring at the bell
        face.set(0, 1, "L4")
    tip = front_hung(g, "signal_horn_tip", 3.2, (-1.5, -1, -1.5), (1, 1, 1), role="L", seed=58009, base=2, top=8.4)
    tip.top.fill("L1")
