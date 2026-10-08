"""Breton Bragou Braz: very wide, finely pleated breeches to the knee under a broad buckled belt, with buttoned gaiters and buckled shoes."""
from kit import SIDES, belt, waistband
from kit_male import leg_blk
from kit_m08 import pleats
from paint import fabric

META = {
    "name": "Breton Bragou Braz",
    "gender": "male",
    "description": "Very wide bragou braz falling in fine pleats to a band at the knee, a broad leather belt with a big buckle, pale gaiters buttoned up the outer calf and buckled shoes.",
    "tags": ["relaxed", "casual"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        pleats(leg.strip, "P", 2, rows=range(0, 6), ox=i)
        fabric(leg.top, "P", "weave", 38301, 2)
        fabric(leg.strip, "S", "weave", 38302 + i, 3, 0, 6, leg.strip.w, 4)     # gaiters
        for face in pants.sides:
            fabric(face, "S", "weave", 38304, 3, 0, 6, face.w, 4)
            face.hline(0, face.w - 1, 6, "S4")
        outer = pants.right if side == "right" else pants.left
        for y in (7, 8, 9):
            outer.set(1 if side == "right" else 2, y, "M3")                  # buttoned up the outer calf
        fabric(leg.strip, "K", "smooth", 38305, 2, 0, 10, leg.strip.w, 2)
        for face in pants.sides:
            fabric(face, "K", "smooth", 38306, 2, 0, 10, face.w, 2)
            face.hline(0, face.w - 1, 11, "K0")
        pants.front.set(1, 10, "M4"), pants.front.set(2, 10, "M3")           # shoe buckles
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
        bragou = leg_blk(g, f"{side}_bragou", side, -.2, (5, 7, 5), "P", 2, "weave", 38307 + i,
                         dx=-.5 if side == "right" else .5, inflate=.1)
        for face in bragou.sides:
            pleats(face, "P", 2, rows=range(0, 6), ox=i)
            face.hline(0, face.w - 1, 6, "A2")                              # the knee band
        bragou.bottom.fill("P0")
    waistband(g, "P", "weave", 38309)
    wide = belt(g, "waist_belt", 9.3, role="L", height=2, buckle="M")
    wide.front.set(4, 1, "L0")
