"""Butcher's Striped Apron: a heavy striped bib apron, leather oversleeves on the forearms and a honing steel at the hip."""
from kit import roll
from kit_female import arm_rings, chemise, hanging, over_panel, stripes, sub
from paint import solid

META = {
    "name": "Butcher's Striped Apron",
    "gender": "female",
    "description": "A heavy striped bib apron over a rolled-sleeve shirt, leather oversleeves and a honing steel at the hip.",
    "tags": ["work", "apron", "sturdy"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 3, "weave", 14001, neckline="slit", sleeve_rows=(0, 5))
    roll(g, "S", 2.8, base=3)
    for box in arm_rings(g, "oversleeve", 5.2, 4, 5, inflate=.08):
        solid(box, "L", "leather", 14002, 2)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L3")
            face.set(1, 2, "M3")
    j = g.part("jacket")
    stripes(sub(j.front, 1, 1, 6, 10), ["P2", "S4"], 1, vertical=True)
    j.front.hline(1, 6, 1, "P1")
    j.top.hline(2, 5, 3, "P2")
    for y in range(0, 2):
        j.front.set(2, y, "P2"), j.front.set(5, y, "P2")              # the neck strap
    j.back.hline(0, 7, 9, "P2")
    for face in (j.right, j.left):
        face.hline(0, 3, 9, "P2")
    face = over_panel(g, "apron", 10, "S", "weave", 14003, base=4, width=8, top=9.0)
    stripes(face, ["P2", "S4"], 1, vertical=True)
    face.hline(0, 7, 0, "P1"), face.hline(0, 7, 9, "P0")
    steel = hanging(g, "honing_steel", -3.4, 6, role="M", base=3, top=9.0)
    steel.front.set(0, 0, "L2"), steel.front.set(0, 1, "L2")
