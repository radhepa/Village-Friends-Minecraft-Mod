"""Summer Trousers & Strap Sandals: light trousers rolled to mid-calf, bare ankles and strapped sandals."""
from kit import SIDES, leg_ring, legs, waistband
from paint import strip_fabric

META = {
    "name": "Summer Trousers & Sandals",
    "description": "Light trousers rolled to mid-calf, bare ankles and leather strap sandals.",
    "tags": ["casual", "relaxed", "simple"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "weave", 2501, base=3, rows=(0, 7))
    waistband(g, "S", "weave", 2502, base=3)
    for ring in leg_ring(g, "roll", 6.4, "S", base=3, size=(5, 2, 5)):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "S4"), face.hline(0, face.w - 1, 1, "S2")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 11, "L1")
            face.set(1, 10, "L2"), face.set(2, 9, "L2")
        leg.strip.hline(0, leg.strip.w - 1, 11, "L1")
        leg.bottom.fill("L0"), pants.bottom.fill("L0")
