"""Notary's Black Hose: close black hose seamed up the back, a ribbon garter bow below each knee, and black shoes with tall pointed tongues."""
from kit import SIDES, waistband
from kit_male import leg_blk
from kit_m05 import hose, soft_shoes
from paint import solid

META = {
    "name": "Notary's Black Hose",
    "gender": "male",
    "description": "Close black hose seamed up the back, a coloured ribbon garter tied in a bow below each knee, and polished black shoes with tall pointed tongues standing up at the ankle.",
    "tags": ["scholarly", "slim", "tailored"],
}


def build(g):
    hose(g, "K", 2, "smooth", 35460, end=9)
    waistband(g, "K", "smooth", 35461)
    soft_shoes(g, "K", 1, top=10, sole="K0", cuff="K3")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.strip.hline(0, leg.strip.w - 1, 4, "A2")                       # the garter ribbon
        leg.front.vline(2 if side == "right" else 1, 1, 3, "K3")           # a sheen down the shin
        leg.front.vline(2 if side == "right" else 1, 6, 8, "K3")
        outer = -1.6 if side == "right" else 1.6
        bow = leg_blk(g, f"{side}_garter_bow", side, 3.6, (2, 1, 1), "A", 2, "plain", 35462, dx=outer, dz=-1.9)
        bow.front.set(0, 0, "A3"), bow.front.set(1, 0, "A1")
        tail = g.piece(f"{side}_garter_tail", "RIGHT_LEG" if side == "right" else "LEFT_LEG", (-.5, 0, -.5), (1, 2, 1),
                       pivot=(outer, 4.6, -1.9))
        solid(tail, "A", "plain", 35463, 2, edge=False)
        tongue = leg_blk(g, f"{side}_shoe_tongue", side, 8.4, (2, 2, 1), "K", 2, "smooth", 35464, dz=-2.3)
        tongue.front.set(0, 0, "K3"), tongue.front.set(1, 0, "K3"), tongue.front.set(0, 1, "K1")
        tongue.top.fill("K3")
