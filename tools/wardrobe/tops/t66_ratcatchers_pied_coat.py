"""Ratcatcher's Pied Coat: a coat split down the middle in two colours, a tame rat on the shoulder, a pipe and a wicker cage."""
from kit import belt, body, flaps, sleeves
from kit_male import arm_blk, blk
from paint import fabric

META = {
    "name": "Ratcatcher's Pied Coat",
    "gender": "male",
    "description": "A ratcatcher's pied coat split down the middle in two colours, a tame rat riding the shoulder, a pipe and a wicker cage.",
    "tags": ["whimsical", "work"],
    "locked_to": "b66_ratcatchers_patched_hose",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 6601)
    for face in b.sides:
        if face.name in ("front", "back"):
            right_half = range(0, 4) if face.name == "front" else range(4, 8)
            fabric(face, "A", "weave", 6602, 2, right_half.start, 0, 4, 12)
        elif face.name == "right":
            fabric(face, "A", "weave", 6602, 2)
    fabric(b.top, "A", "weave", 6602, 3, 0, 0, 4, 4)
    sleeves(g, "P", "weave", 6603, rows=(0, 10), cuff="S3")
    fabric(g.part("right_arm").strip, "A", "weave", 6604, 2, 0, 0, 16, 10)
    belt(g, "belt", 9.4, height=1)
    rat = arm_blk(g, "shoulder_rat", "left", -3.0, (2, 1, 3), "S", 1, "plain", 6605)
    rat.front.set(0, 0, "K2"), rat.top.set(1, 0, "S2")
    tail = arm_blk(g, "shoulder_rat_tail", "left", -2.4, (1, 3, 1), "A", 3, "plain", 6606, dz=2.3)
    tail.strip.hline(0, tail.strip.w - 1, 2, "A4")
    pipe = blk(g, "rat_pipe", (2.6, 9.0, -2.75), (1, 4, 1), "L", 3, "plain", 6607, rotation=(0, 0, -15))
    pipe.front.set(0, 1, "K2"), pipe.front.set(0, 2, "K2")
    cage = blk(g, "wicker_cage", (-1.0, 2.0, 3.6), (3, 3, 3), "L", 3, "plain", 6608)
    for face in cage.sides:
        for x in range(face.w):
            for y in range(face.h):
                if x % 2 == 0:
                    face.set(x, y, "L1")
    for face in flaps(g, "coat_skirt", 4, "P", "weave", 6609, top=10.8):
        half = range(0, 4) if face.name == "front" else range(5, 9)
        for x in half:
            face.vline(x, 0, 3, "A2")
        face.hline(0, 8, 3, "S3")
