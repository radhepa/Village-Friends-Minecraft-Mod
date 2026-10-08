"""Spearmaiden's Leather-Strip Skirt: a short wool underskirt hung all round with separate studded leather strips
(pteruges) that swing apart as she strides, a studded war belt and knee boots."""
from kit import SIDES
from kit_female import hose, shoes, skirt, waist_belt
from paint import solid

META = {
    "name": "Spearmaiden's Leather-Strip Skirt",
    "gender": "female",
    "description": "A short wool underskirt hung all round with separate studded leather strips that fan apart in "
                   "her stride, a studded war belt and knee boots.",
    "tags": ["martial", "sturdy", "skirt"],
}

LENGTH = 8


def paint_strip(box, face, seed):
    solid(box, "L", "leather", seed, 2)
    face.hline(0, 1, 0, "L3")
    face.set(0, 2, "M3"), face.set(1, 2, "M2")                     # stud
    face.vline(1, 3, LENGTH - 3, "L1")                              # the strip's shaded edge
    face.set(0, LENGTH - 3, "M3")
    face.set(0, LENGTH - 1, "A2"), face.set(1, LENGTH - 1, "A1")   # dyed fringe at the tip
    face.set(0, LENGTH - 2, "L3")


def build(g):
    s = skirt(g, "P", "weave", 54061, top=9.6, length=6, flare=6, folds=False)
    s.hem("P1")
    for face in s.wide_faces:
        face.hline(0, face.w - 1, 4, "A2")
    hose(g, "S", rows=(4, 6), base=2, texture="knit", seed=54062)
    shoes(g, "boot", "L", 2, top=6)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(1 if side == "right" else 2, 7, 9, "L3")
    n = 0
    for name, z, motion in (("front", -3.05, "flap_front"), ("back", 2.05, "flap_back")):
        for x in (-3.75, -1.25, 1.25, 3.75):
            box = g.piece(f"strip_{name}_{n}", "TORSO", (-1, 0, 0), (2, LENGTH, 1), pivot=(x, 9.5, z), motion=motion)
            paint_strip(box, box.front if name == "front" else box.back, 54063 + n)
            n += 1
    for side, x, ox, rot in (("right", -5.2, -1, 7), ("left", 5.2, 0, -7)):
        for i, z in enumerate((-1.2, 1.2)):
            box = g.piece(f"strip_{side}_{i}", "TORSO", (ox, 0, -1), (1, LENGTH - 1, 2), pivot=(x, 9.5, z),
                          rotation=(0, 0, rot))
            solid(box, "L", "leather", 54071 + i, 2)
            face = box.right if side == "right" else box.left
            face.hline(0, 1, 0, "L3"), face.set(0, 2, "M3"), face.set(1, 2, "M2")
            face.hline(0, 1, LENGTH - 2, "A2")
    belt = waist_belt(g, "waist_war_belt", 9.0, height=2)
    for face in belt.sides:
        for x in range(0, face.w, 2):
            face.set(x, 1, "M3")                                    # studs along the belt
