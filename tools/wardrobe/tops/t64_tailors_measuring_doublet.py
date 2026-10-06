"""Tailor's Measuring Doublet: a neat doublet with a marked measuring tape about the neck, a pincushion wristlet and shears."""
from kit import body, sleeves
from kit_male import arm_blk, blk, buttons

META = {
    "name": "Tailor's Measuring Doublet",
    "gender": "male",
    "description": "A tailor's neat doublet with a marked measuring tape hung about the neck, a pincushion on the wrist and shears at the hip.",
    "tags": ["tailored", "work"],
}


def tape(box):
    for face in box.faces:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "K2" if (y if face.h > 1 else x) % 3 == 0 else "S4")


def build(g):
    b = body(g, "P", "smooth", 6401)
    b.front.clear(3, 0), b.front.clear(4, 0)
    b.front.vline(4, 1, 11, "P0")
    buttons(b.front, 3, 1, 10, 2, "M3")
    for face in b.sides:
        face.hline(0, face.w - 1, 10, "P3"), face.hline(0, face.w - 1, 11, "P1")
    sleeves(g, "P", "smooth", 6402, rows=(0, 10), cuff="P1")
    for name, x in (("tape_right", -1.6), ("tape_left", 1.6)):
        end = blk(g, name, (x, -.4, -2.65), (1, 7, 1), "S", 4, "plain", 6403)
        tape(end)
    neck = blk(g, "tape_neck", (0, -.3, 0), (5, 1, 6), "S", 4, "plain", 6404, origin=(-2.5, 0, -3.1))
    tape(neck)
    cushion = arm_blk(g, "pincushion", "left", 6.8, (5, 1, 5), "A", 2, "plain", 6405, inflate=.12)
    for x in range(0, cushion.top.w, 2):
        cushion.top.set(x, 2, "M4")                                      # pin heads
    cushion.top.set(1, 1, "M4"), cushion.top.set(3, 3, "M4")
    shears = blk(g, "shears", (-3.1, 9.2, -2.75), (1, 4, 1), "M", 3, "smooth", 6406, rotation=(0, 0, -8))
    shears.strip.hline(0, shears.strip.w - 1, 0, "M1"), shears.strip.hline(0, shears.strip.w - 1, 3, "M4")
