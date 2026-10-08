"""Quilted Knee Breeches: box-quilted breeches buttoned at the knee over knitted stockings and low strapped shoes."""
from kit import SIDES, footwear, leg_bone, stockings, waistband
from kit_m10 import leg_ring, outer
from paint import fabric, k, solid


META = {
    "name": "Quilted Knee Breeches",
    "gender": "male",
    "description": "Warm breeches stitched in a square box quilt, closed at the knee by a band with three bone buttons, over plain knitted stockings and low strapped shoes.",
    "tags": ["casual", "simple"],
}


def box_quilt(face, role="P", base=2, rows=None, ox=0):
    """Square quilting: stitched rows and columns every three texels, a puffed lit centre in each box."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            gx, gy = (x + ox) % 3, y % 3
            face.set(x, y, k(role, base - 1) if gx == 0 or gy == 0 else k(role, base + 1) if (gx, gy) == (1, 1)
                     else k(role, base))


def build(g):
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        box_quilt(leg.strip, rows=range(0, 6), ox=i)
        fabric(leg.top, "P", "plain", 40200, 2)
        outer(leg, side).vline(2, 0, 5, "P0")
        band = leg_ring(g, f"{side}_knee_band", side, 5.4, (5, 1, 5), "P", 1, "plain", 40201 + i, open_bottom=False)
        for face in band.sides:
            face.hline(0, face.w - 1, 0, "P1")
        o = outer(band, side)
        o.set(1, 0, "S4"), o.set(3, 0, "S4")
        for y in (4.0, 3.0):
            btn = g.piece(f"{side}_knee_button_{int(y)}", leg_bone(side), (-.5, -.5, -.5), (1, 1, 1),
                          pivot=(-2.15 if side == "right" else 2.15, y + .4, .2))
            solid(btn, "S", "plain", 40203 + i, 4, edge=False)
    stockings(g, "S", (6, 9), base=3)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for x in range(0, leg.strip.w, 3):
            leg.strip.vline(x, 6, 9, "S2")                               # knitted ribs
    body = waistband(g, "P", "plain", 40205)
    for face in body.sides:
        box_quilt(face, rows=range(10, 12))
    footwear(g, "shoe", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "L1")                                # instep strap
        pants.front.set(2 if side == "right" else 1, 10, "M3")
