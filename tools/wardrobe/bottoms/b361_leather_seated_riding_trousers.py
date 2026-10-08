"""Leather-Seated Riding Trousers: twill riding trousers faced with leather on the seat and inner legs, buttoned at the calf, in ankle boots."""
from kit import SIDES
from kit_casual import leather_belt, shoes, trousers
from kit_m10 import inner, outer

META = {
    "name": "Leather-Seated Riding Trousers",
    "gender": "male",
    "description": "Close twill riding trousers faced with smooth leather over the seat and all down the inner legs where they grip the saddle, buttoned up the outside of the calf, in plain ankle boots.",
    "tags": ["casual", "sturdy", "rugged"],
}


def build(g):
    legs, body = trousers(g, "P", 2, "twill", 40720, end=8)
    for side, leg in zip(SIDES, legs):
        # Leather facing down the inner leg, wrapping a column onto the front and back.
        inn = inner(leg, side)
        for y in range(0, 9):
            for x in range(inn.w):
                inn.set(x, y, "L2" if (x + y) % 5 else "L3")
        col = 2 if side == "right" else 1
        for face in (leg.front, leg.back):
            c = col if face is leg.front else 3 - col
            face.vline(c + (1 if side == "right" else -1) * (1 if face is leg.front else -1), 0, 8, "L2")
            face.vline(c, 0, 8, "L1")
        # Leather seat across the back of the thighs.
        for y in range(0, 3):
            leg.back.hline(0, 3, y, "L2" if y else "L3")
        # Buttoned slit up the outer calf.
        o = outer(leg, side)
        o.vline(1, 5, 8, "P1")
        for y in (5, 7):
            o.set(2, y, "M3")
    shoes(g, "boot", top=10)
    for side in SIDES:
        g.part(f"{side}_pants").strip.hline(0, 15, 8, "L3")              # boot tops
    leather_belt(g)
