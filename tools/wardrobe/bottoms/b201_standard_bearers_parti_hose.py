"""Standard Bearer's Parti Hose: counterchanged hose, each leg switching colour at a dagged knee garter, and cuffed ankle boots."""
from kit import SIDES, footwear, leg_ring, waistband
from paint import fabric, strip_fabric

META = {
    "name": "Standard Bearer's Parti Hose",
    "gender": "male",
    "description": "Counterchanged hose: the right leg is the house colour above the knee and the accent below, the left "
                   "the other way about, parted by dagged garters, over soft ankle boots with turned-down cuffs.",
    "tags": ["fancy", "slim"],
}

S = 34220


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        upper, lower = ("P", "A") if side == "right" else ("A", "P")
        strip_fabric(leg, upper, "velvet", S + (side == "left"), 2, 0, 5)
        strip_fabric(leg, lower, "velvet", S + 2 + (side == "left"), 2, 6, 9)
        fabric(leg.top, upper, "velvet", S, 2)
        leg.front.vline(1 if side == "right" else 2, 1, 4, f"{upper}3")
        leg.strip.hline(0, leg.strip.w - 1, 5, f"{upper}1")
    body = waistband(g, "P", "velvet", S + 4)
    accent_cols = {"front": range(4, 8), "back": range(0, 4), "left": range(0, 4), "right": range(0)}
    for face in body.sides:                                                # the waist is parted too
        for x in accent_cols[face.name]:
            face.vline(x, 10, 11, "A2")
            face.set(x, 9, "A3")
    footwear(g, "boot", top=9, base=1)
    for i, ring in enumerate(leg_ring(g, "garter", 5.6, "S", base=3, size=(5, 1, 5), inflate=.08)):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S4" if x % 2 == 0 else "S2")               # dagged edge
    for ring in leg_ring(g, "boot_cuff", 8.4, "L", base=3, size=(5, 1, 5), texture="leather", inflate=.12):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
            face.set(2, 0, "L1")
