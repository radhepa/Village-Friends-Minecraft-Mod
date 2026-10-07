"""Nomad's Sirwal: deep-cut sirwal trousers billowing to the shin and gathered in embroidered cuffs, with leather sandals."""
from kit import SIDES, legs, waistband
from kit_male import embroider, leg_rings

META = {
    "name": "Nomad's Sirwal",
    "gender": "male",
    "description": "Deep-cut sirwal trousers billowing loose to the shin and gathered in embroidered cuffs at the ankle, with leather sandals.",
    "tags": ["robe", "relaxed"],
    "locked_to": "t86_desert_nomads_layered_robe",
}


def build(g):
    legs(g, "S", "weave", 8611, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 8612, base=3)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 9, "A2")
        embroider(leg.strip, 8, "dots", "A3")                             # embroidered ankle cuff
        pants.strip.hline(0, pants.strip.w - 1, 11, "L2")                 # sandal sole
        pants.front.set(1, 10, "L3"), pants.front.set(2, 10, "L3")
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
    for ring in leg_rings(g, "sirwal_billow", 3.2, "S", (5, 5, 5), 3, "weave", 8613, inflate=.18):
        for face in ring.sides:
            for x in range(face.w):
                if x % 2 == 0:
                    face.vline(x, 1, 3, "S2")
            face.hline(0, face.w - 1, 4, "S1")
        ring.bottom.fill("S1")
