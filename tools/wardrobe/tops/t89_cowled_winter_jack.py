"""Cowled Winter Jack: a jack quilted in thick horizontal rolls, a knitted cowl wound about the neck and mittens on a string."""
from kit import body, sleeves
from kit_male import arm_blk, blk, ribbing

META = {
    "name": "Cowled Winter Jack",
    "gender": "male",
    "description": "A deep-winter jack quilted in thick horizontal rolls, a knitted cowl wound about the neck with a trailing end, and mittens.",
    "tags": ["casual", "rugged"],
}


def rolls(face, role="P"):
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, f"{role}3" if y % 3 == 0 else f"{role}1" if y % 3 == 2 else f"{role}2")


def build(g):
    b = body(g, "P", "quilt", 8901)
    for face in b.sides:
        rolls(face)
    b.front.vline(4, 0, 11, "P0")
    sleeves(g, "P", "quilt", 8902, rows=(0, 9))
    for side in ("right", "left"):
        rolls(g.part(f"{side}_arm").strip)
    cowl = g.piece("knit_cowl", "TORSO", (-4.8, -1.4, -2.9), (10, 3, 6), inflate=.08)
    for face in cowl.faces:
        ribbing(face, "A", 2)
    for face in cowl.sides:
        face.hline(0, face.w - 1, 0, "A3")
    tail = blk(g, "cowl_end", (-2.4, 1.4, -3.1), (2, 6, 1), "A", 2, "knit", 8903, motion="sway")
    ribbing(tail.front, "A", 2)
    tail.front.hline(0, 1, 5, "S3")
    for i, side in enumerate(("right", "left")):
        mitt = arm_blk(g, f"{side}_mitten", side, 7.8, (5, 3, 5), "S", 3, "knit", 8904 + i, inflate=.12)
        for face in mitt.sides:
            ribbing(face, "S", 3, rows=range(0, 1))
            face.hline(0, face.w - 1, 0, "S2")
