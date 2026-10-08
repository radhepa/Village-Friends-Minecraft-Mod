"""Halberdier's Livery Doublet: a guard's doublet in the house colours, livery-badged, with striped shoulder wings."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_male import arm_blk, buttons
from paint import grid, solid

META = {
    "name": "Halberdier's Livery Doublet",
    "gender": "male",
    "description": "A guard's buttoned doublet in the house colours: body in one, sleeves in the other, a livery rose on the "
                   "breast and back, striped shoulder wings and a tabbed peplum.",
    "tags": ["martial", "fancy"],
    "covers_waist": True,
}

S = 34080

ROSE = [".a.",
        "aba",
        ".a."]
BIG_ROSE = [".aa.",
            "abba",
            "abba",
            ".aa."]


def build(g):
    b = body(g, "P", "velvet", S)
    f = b.front
    f.vline(3, 1, 11, "P1"), f.vline(4, 1, 11, "P3")                     # button stand
    buttons(f, 4, 2, 10, 2, "M3")
    grid(f, 5, 2, ROSE, {"a": "S4", "b": "A2"})
    grid(b.back, 2, 2, BIG_ROSE, {"a": "S4", "b": "A2"})
    for face in b.sides:
        face.hline(0, face.w - 1, 10, "P1")                                # waist seam
    sleeves(g, "A", "velvet", S + 1, rows=(0, 10), cuff="P2")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.front.vline(0, 1, 9, "A1")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3")
    for i, side in enumerate(SIDES):
        wing = arm_blk(g, f"{side}_shoulder_wing", side, -2.2, (5, 2, 5), "P", 2, "velvet", S + 2 + i, inflate=.16)
        for face in wing.sides:
            for x in range(face.w):
                if x % 2:
                    face.vline(x, 0, 1, "A2")
            face.set(0, 1, "P1"), face.set(face.w - 1, 1, "P1")
        wing.top.fill("P3")
    band = collar(g, "falling_collar", "S", "plain", base=3, height=1, y=-.6)
    band.front.set(4, 0, "S1")
    belt = g.piece("belt", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.07)
    solid(belt, "L", "leather", S + 4, 2, edge=False)
    belt.front.set(4, 0, "M3")
    for face in flaps(g, "peplum", 2, "P", "velvet", S + 5, top=10.6):
        for x in (2, 5):
            face.vline(x, 0, 1, "P0")                                      # cut into tabs
        face.hline(0, 8, 1, "A2")
