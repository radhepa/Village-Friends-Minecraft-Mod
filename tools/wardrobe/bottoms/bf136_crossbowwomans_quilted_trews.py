"""Crossbowwoman's Quilted Trews: diamond-quilted trews with padded knee rolls, tied garters and laced ankle boots."""
from kit import SIDES, legs, waistband
from kit_female import leg_rings, shoes, waist_belt
from paint import fabric, solid

META = {
    "name": "Crossbowwoman's Quilted Trews",
    "gender": "female",
    "description": "Diamond-quilted wool trews with padded knee rolls and tied garters, over laced leather ankle boots.",
    "tags": ["martial", "sturdy"],
}


def build(g):
    legs(g, "P", "quilt", 54021, rows=(0, 9), crease=False)
    body = waistband(g, "P", "quilt", 54022)
    body.front.vline(3, 9, 11, "P1"), body.front.set(4, 10, "M3")   # buttoned fly flap
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, 15, 9, "P1")
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            fabric(face, "P", "quilt", 54023, 2, 0, 0, face.w, 3)
            face.hline(0, face.w - 1, 2, "P1")                        # quilted thigh overlay, stitched hem
        outer = pants.left if side == "left" else pants.right
        outer.vline(1, 0, 2, "P3")
    for ring in leg_rings(g, "knee_roll", 4.0, 2, 5, .08):
        solid(ring, "P", "quilt", 54024, 2, edge=False)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P3")
            for x in range(0, face.w, 2):
                face.set(x, 1, "P1")                                  # padded tucks
    for ring in leg_rings(g, "garter", 6.4, 1, 5, .06):
        solid(ring, "A", "plain", 54025, 2, edge=False)
        ring.front.set(1, 0, "A4"), ring.front.set(2, 0, "A1")        # the tied knot
    shoes(g, "ankle", "L", 2, top=9, accent="S3")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 9, "S3"), pants.front.set(2, 9, "S3")      # lacing up the instep
    waist_belt(g, "waist_belt", 9.4, height=1)
