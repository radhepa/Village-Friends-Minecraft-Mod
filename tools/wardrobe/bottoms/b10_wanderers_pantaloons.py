"""Wanderer's Pantaloons: billowing trousers gathered at the ankle, soft boots and a purse on a cord."""
from paint import cap, fabric, k, solid, strip_fabric

META = {
    "name": "Wanderer's Pantaloons",
    "description": "Loose trousers that billow over gathered ankle cuffs, soft boots and a coin purse on a cord.",
    "tags": ["relaxed", "simple"],
}


def build(g):
    for side in ("right", "left"):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 221 if side == "right" else 222, 2, 0, 9)
        fabric(leg.top, "S", "weave", 22, 2)
        leg.front.vline(1 if side == "right" else 2, 1, 6, "S1")   # a soft pleat
        # Gathered cuff and soft boots.
        leg.strip.hline(0, leg.strip.w - 1, 9, "L3")
        strip_fabric(leg, "L", "leather", 223, 1, 10, 11)
        for face in pants.sides:
            fabric(face, "L", "leather", 224, 1, 0, 9, face.w, 3)
            face.hline(0, face.w - 1, 9, "L3")
            face.hline(0, face.w - 1, 11, "K1")
        leg.bottom.fill("K1"), pants.bottom.fill("K1")
        # The billow above the cuff: a soft rounded volume with pleat shading.
        bone = "RIGHT_LEG" if side == "right" else "LEFT_LEG"
        billow = g.piece(f"{side}_billow", bone, (-2.6, 5.4, -2.6), (5, 3, 5), inflate=.1)
        for face in billow.sides:
            for x in range(face.w):
                face.set(x, 0, "S2")
                face.set(x, 1, "S3" if x % 2 else "S2")
                face.set(x, 2, "S1" if x % 2 else "S2")
        fabric(billow.top, "S", "weave", 225, 2)
        billow.bottom.fill("S1")

    body = g.part("body")
    strip_fabric(body, "S", "weave", 226, 2, 9, 11)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "S1" if x % 2 else "S3")   # drawstring gathers
    fabric(body.bottom, "S", "weave", 23, 1)
    cord = g.piece("waist_cord", "TORSO", (-4.55, 9.8, -2.55), (9, 1, 5), inflate=.03)
    solid(cord, "L", "leather", 227, 2, edge=False)
    purse = g.piece("waist_purse", "TORSO", (-1, 0, -1), (2, 3, 2), pivot=(-3.2, 10.9, -2.5), rotation=(0, 0, -6))
    solid(purse, "L", "leather", 228, 2)
    purse.front.hline(0, 1, 0, "A2")
    purse.front.set(1, 1, "M3")
    cap(purse, "L", top_delta=1)
