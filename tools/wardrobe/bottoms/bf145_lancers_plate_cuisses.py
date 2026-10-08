"""Lancer's Plate Cuisses: riding hose with lamed steel cuisses over the thighs, fanned poleyns at the knees,
greaves and riding boots with prick spurs at the heels."""
from kit import SIDES, leg_bone
from kit_female import hose, leg_rings, shoes, waist_belt
from kit_f04 import lames
from paint import fabric, solid

META = {
    "name": "Lancer's Plate Cuisses",
    "gender": "female",
    "description": "Riding hose under lamed steel cuisses, fanned poleyns at the knees, greaves and riding boots "
                   "with prick spurs at the heels.",
    "tags": ["armor", "martial", "sturdy"],
    "requires": ["martial", "rugged"],
}


def build(g):
    hose(g, "P", rows=(0, 11), base=2, texture="weave", seed=54381)
    body = g.part("body")
    fabric(body.front, "P", "weave", 54382, 2, 0, 9, 8, 3)
    for face in (body.right, body.back, body.left):
        fabric(face, "P", "weave", 54382, 2, 0, 9, face.w, 3)
    fabric(body.bottom, "P", "weave", 54382, 1)
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "P3")
    shoes(g, "boot", "L", 2, top=9)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:                                     # greaves over the shins
            if face is (pants.left if side == "right" else pants.right):
                continue
            fabric(face, "M", "smooth", 54383, 2, 0, 6, face.w, 3)
            face.hline(0, face.w - 1, 6, "M4"), face.hline(0, face.w - 1, 8, "M1")
        pants.front.vline(1 if side == "right" else 2, 6, 8, "M4")
    # Cuisses: three lames down the front and sides of each thigh, strapped behind.
    for ring in leg_rings(g, "cuisse", .2, 4, 5, inflate=.1):
        solid(ring, "M", "smooth", 54384, 2)
        for face in ring.sides:
            lames(face, "M", 2, step=2, y0=0, y1=3)
        ring.back.vline(1, 0, 3, "L2"), ring.back.vline(3, 0, 3, "L2")
        ring.top.fill("M3")
    for side in SIDES:
        cop = g.piece(f"{side}_poleyn", leg_bone(side), (-2, 0, -1), (4, 3, 2), pivot=(0, 4.2, -1.9))
        solid(cop, "M", "smooth", 54385, 3)
        cop.front.set(1, 1, "M4"), cop.front.set(2, 1, "M4"), cop.front.hline(0, 3, 2, "M1")
        ox = -3.1 if side == "right" else 2.1
        wing = g.piece(f"{side}_poleyn_fan", leg_bone(side), (ox, 0, -1.5), (1, 3, 3), pivot=(0, 4.2, -.2))
        solid(wing, "M", "smooth", 54386, 2, edge=False)
        out = wing.right if side == "right" else wing.left
        out.vline(1, 0, 2, "M4"), out.vline(0, 0, 2, "M3"), out.vline(2, 0, 2, "M1")
        neck = g.piece(f"{side}_spur", leg_bone(side), (-.5, 0, 0), (1, 1, 1), pivot=(0, 10.6, 2.2))
        solid(neck, "M", "smooth", 54387, 3, edge=False)
        prick = g.piece(f"{side}_spur_prick", leg_bone(side), (-.5, -.5, 0), (1, 1, 1), pivot=(0, 11.1, 3.2))
        solid(prick, "M", "smooth", 54388, 4, edge=False)
    waist_belt(g, "waist_belt", 9.4, height=1)
