"""Butcher's Gaitered Breeches: sturdy breeches with buttoned canvas gaiters to the knee and heavy shoes."""
from kit import SIDES, legs, waistband
from kit_female import shoes, waist_belt
from paint import fabric

META = {
    "name": "Butcher's Gaitered Breeches",
    "gender": "female",
    "description": "Sturdy twill breeches with buttoned canvas gaiters to the knee and heavy hobnailed shoes.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 14011, rows=(0, 5), crease=False)
    waistband(g, "P", "twill", 14012)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            fabric(face, "S", "twill", 14013, 2, 0, 4, face.w, 6)
            face.hline(0, face.w - 1, 4, "S3")
        outer = pants.right if side == "right" else pants.left
        for y in (5, 7, 9):
            outer.set(2 if side == "right" else 1, y, "M3")
        fabric(leg.strip, "S", "twill", 14014, 1, 0, 4, 16, 6)
    shoes(g, "shoe", "L", 1)
    for side in SIDES:
        g.part(f"{side}_pants").front.hline(0, 3, 11, "M1")
    waist_belt(g, "waist_belt", 9.4, height=1)
