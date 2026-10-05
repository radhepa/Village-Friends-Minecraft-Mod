"""Pinstripe Trousers: pressed pinstripes, a buttoned waistband and polished buckled shoes."""
from paint import fabric, k, rnd, strip_fabric

META = {
    "name": "Pinstripe Trousers",
    "description": "Pressed pinstriped trousers with a buttoned waistband and polished buckle shoes.",
    "tags": ["tailored", "fancy"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip = leg.strip
        for y in range(10):
            for x in range(strip.w):
                s = 2 if x % 3 else 3
                if rnd(x, y, 111) < .03:
                    s -= 1
                strip.set(x, y, k("P", s))
        fabric(leg.top, "P", "plain", 112, 2)
        crease = 1 if side == "right" else 2
        leg.front.vline(crease, 0, 9, "P4")
        leg.strip.hline(0, strip.w - 1, 9, "P1")
        leg.front.set(0 if side == "right" else 3, 3, "P1")
        # Polished shoes: dark leather, a bright toe glint and a metal buckle.
        strip_fabric(leg, "L", "smooth", 113, 1, 10, 11)
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L1")
            face.hline(0, face.w - 1, 11, "L0")
        pants.front.hline(0, 3, 11, "L1")
        pants.front.set(2 if side == "right" else 1, 11, "L4")
        pants.front.set(1 if side == "right" else 2, 10, "M3")
        pants.front.set(2 if side == "right" else 1, 10, "M2")
        leg.bottom.fill("K0"), pants.bottom.fill("K0")

    body = g.part("body")
    strip_fabric(body, "P", "plain", 114, 2, 9, 11)
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "P3")
    body.front.set(4, 10, "M3")
    fabric(body.bottom, "P", "plain", 115, 1)
