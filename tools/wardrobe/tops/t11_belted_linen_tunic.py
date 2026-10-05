"""Belted Linen Tunic: a long-sleeved tunic with an embroidered neckband, belted over a thigh-length hem."""
from kit import belt, body, flaps, neckline, sleeves
from paint import grid

META = {
    "name": "Belted Linen Tunic",
    "description": "The everyday village tunic: embroidered neckband and cuffs, a belt, and a hem to mid-thigh.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 1101)
    neckline(b.front, "round", "P")
    # Embroidered neckband: a band of accent stitching around the collar.
    for face in (b.front, b.back):
        for x in range(1, 7):
            face.set(x, 1 if face is b.front else 0, "A2" if x % 2 else "A3")
    b.front.set(2, 0, "A2"), b.front.set(5, 0, "A2")
    b.front.vline(3, 1, 3, "P1")
    sleeves(g, "P", "weave", 1102, rows=(0, 10), cuff="A2")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 9, "A3")
    belt(g, "belt", 9.4, height=1)
    end = g.piece("belt_end", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(1.6, 10.4, -2.75))
    from paint import solid
    solid(end, "L", "leather", 1103, 2)
    end.front.set(0, 2, "M3")
    front, back = flaps(g, "hem", 4, "P", "weave", 1104, hem="A2", top=10.2)
    for face in (front, back):
        face.hline(0, 8, 2, "A1")
