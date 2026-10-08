"""Simple Wrapped Trousers: roomy wrap-over trousers whose front panels cross on each thigh, tied at the hip and gathered at the ankle."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_m10 import leg_ring, outer, tie
from paint import fabric, k, strip_fabric

META = {
    "name": "Simple Wrapped Trousers",
    "gender": "male",
    "description": "Roomy wool trousers cut to wrap over, the front panels crossing each thigh in a long diagonal fold, knotted at the hip and gathered into a tied band at the ankle above soft turnshoes.",
    "tags": ["casual", "simple", "relaxed"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "weave", 40320 + i, 2, 0, 9)
        fabric(leg.top, "P", "weave", 40320, 2)
        strip_fabric(pants, "P", "weave", 40322 + i, 2, 0, 7)            # the wrap stands off the leg
        pants.strip.hline(0, pants.strip.w - 1, 7, "P1")
        # The overlap: a fold running from the outer hip down to the inner knee.
        f = pants.front
        for y in range(0, 7):
            x = y * 3 // 6 if side == "right" else 3 - y * 3 // 6
            f.set(x, y, "P3")
            nx = x + 1 if side == "right" else x - 1
            if 0 <= nx <= 3:
                f.set(nx, y, "P1")
        o = outer(pants, side)
        for y in range(1, 7, 2):
            o.set(1, y, "P1")                                             # loose folds at the side
        # Ankle gathered into a tied band.
        cuff = leg_ring(g, f"{side}_ankle_band", side, 8.2, (5, 2, 5), "P", 2, "weave", 40324 + i)
        for face in cuff.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 2 else "P2")
                face.set(x, 1, "S2")
        tie(g, f"{side}_ankle_tie", leg_bone(side), (-2.6 if side == "right" else 2.6, 9.2, -.6), "S", 2, 2, 40326 + i)
    body = waistband(g, "P", "weave", 40328)
    body.front.vline(2, 9, 11, "P1"), body.front.vline(3, 9, 11, "P3")
    # The wrap's tie knotted at the front of the right hip (hidden under long tops).
    knot = g.piece("waist_wrap_knot", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.4, 10.4, -2.7))
    strip_fabric(knot, "S", "plain", 40329, 3)
    fabric(knot.top, "S", "plain", 40329, 4), fabric(knot.bottom, "S", "plain", 40329, 1)
    knot.front.set(0, 1, "S1")
    for j, rz in enumerate((14, -6)):
        tail = g.piece(f"waist_wrap_tail_{j}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-2.9 + j * .8, 11.0, -2.75),
                       rotation=(0, 0, rz), motion="sway")
        strip_fabric(tail, "S", "plain", 40330 + j, 3)
        fabric(tail.top, "S", "plain", 40330, 3), fabric(tail.bottom, "S", "plain", 40330, 1)
        tail.strip.hline(0, tail.strip.w - 1, 2, k("S", 2))
    footwear(g, "turnshoe", top=10, base=2)
