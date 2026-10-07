"""Illuminator's Sleeve Garters: a fine full-sleeved shirt gathered by garters above the elbow, gold leaf on the cuffs and a brush roll."""
from kit import body, neckline, sleeves
from kit_male import blk, embroider, flecks, sleeve_shapes
from paint import line

META = {
    "name": "Illuminator's Sleeve Garters",
    "gender": "male",
    "description": "A manuscript illuminator's fine shirt, its full sleeves gathered by garters above the elbow, gold leaf on the cuffs and a brush roll.",
    "tags": ["casual", "scholarly"],
    "tucked": True,
}


def build(g):
    b = body(g, "S", "weave", 9801, base=3)
    neckline(b.front, "laced", "S", base=3)
    embroider(b.front, 1, "vine", "A2", "A3", x0=0, x1=7)
    sleeves(g, "S", "weave", 9802, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for x in range(arm.strip.w):
            if x % 2:
                arm.strip.set(x, 3, "S2")                                # fullness puffing over the garter
        flecks(arm.strip, "M4", 9803, .3, rows=range(9, 11))             # gold leaf on the cuffs
    for ring in sleeve_shapes(g, "sleeve_garter", "A", 2.4, (5, 1, 5), "plain", 9804, inflate=.1):
        ring.front.set(2, 0, "M3")
    jf = g.part("jacket").front
    line(jf, 1, 0, 3, 3, "K3"), line(jf, 6, 0, 4, 3, "K3")
    roll = blk(g, "brush_roll", (0, 3.6, -2.65), (3, 2, 1), "L", 2, "leather", 9806)
    roll.front.set(0, 0, "A3"), roll.front.set(1, 0, "M3"), roll.front.set(2, 0, "P3")
