"""Rus Billow Trousers & Winingas: trousers ballooning at the knee, bound below in herringbone leg wraps hooked at the top."""
from kit import SIDES, footwear, legs, waistband
from kit_male import herringbone, leg_rings

META = {
    "name": "Rus Billow Trousers & Winingas",
    "gender": "male",
    "description": "Deep-pleated trousers ballooning over the knee, the shins bound in herringbone winingas hooked at the top, and turnshoes.",
    "tags": ["casual", "rugged"],
}


def build(g):
    legs(g, "P", "weave", 8211, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 8212)
    footwear(g, "turnshoe", top=10, base=2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        herringbone(leg.strip, "S", 2, rows=range(5, 10))
        leg.strip.hline(0, leg.strip.w - 1, 5, "S3")
        leg.front.set(1, 5, "M3"), leg.front.set(2, 5, "M3")              # garter hooks
    for i, ring in enumerate(leg_rings(g, "knee_billow", 1.6, "P", (5, 4, 5), 2, "weave", 8213, inflate=.16)):
        for face in ring.sides:
            for x in range(face.w):
                if x % 2:
                    face.vline(x, 1, 2, "P1")                            # the pleats
            face.hline(0, face.w - 1, 0, "P3"), face.hline(0, face.w - 1, 3, "P1")
        ring.bottom.fill("P0")
