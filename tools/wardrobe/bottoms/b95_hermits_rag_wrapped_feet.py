"""Hermit's Rag-Wrapped Feet: the sackcloth robe's ragged lower skirts over bare shins and feet bound in strips of rag."""
from kit import SIDES, waistband
from kit_male import skirt_panels, wraps

META = {
    "name": "Hermit's Rag-Wrapped Feet",
    "gender": "male",
    "description": "The sackcloth robe's ragged lower skirts falling to the shin, over bare legs and feet bound round with strips of rag.",
    "tags": ["holy", "simple"],
    "locked_to": "t95_hermits_sackcloth",
}


def sacking(face, rows=None):
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            face.set(x, y, "S1" if (x + y) % 2 == 0 and (x // 2 + y // 2) % 2 else "S2")


def build(g):
    body = waistband(g, "S", "tweed", 9511)
    for face in body.sides:
        sacking(face, rows=range(9, 12))
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        sacking(leg.strip, rows=range(0, 4))
        sacking(leg.top)
        wraps(pants.strip, "S", range(8, 12), base=3, period=3)          # rag-bound feet
        wraps(leg.strip, "S", range(9, 12), base=3, period=3)
        leg.bottom.fill("S1"), pants.bottom.fill("S1")
    front, back, sides = skirt_panels(g, "sack_skirt", 9, "S", "tweed", 9512, top=10.6, side_len=8)
    for face in (front, back):
        sacking(face)
        for x in range(face.w):
            if x % 3 == 1:
                face.set(x, 8, "S0")                                     # ragged hem
    for box in sides:
        for face in box.sides:
            sacking(face)
