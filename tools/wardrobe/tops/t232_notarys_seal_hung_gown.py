"""Notary's Seal-Hung Gown: a sober hook-fronted gown with slit oversleeves, a signet on a chain, and a folded charter at the girdle trailing its wax seals on ribbons."""
from kit import belt, body, collar, flaps, sleeves
from paint import solid

META = {
    "name": "Notary's Seal-Hung Gown",
    "gender": "male",
    "description": "A notary's sober calf-length gown hooked down the front, slit oversleeves showing the lining, his signet on a chain, and a folded charter tucked at the girdle trailing three ribbons, each weighted with a round wax seal.",
    "tags": ["scholarly", "tailored", "robe"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 35440, base=1)
    f = b.front
    f.vline(3, 0, 11, "P0"), f.vline(4, 0, 11, "P2")                     # the hooked closure
    for y in range(1, 11, 2):
        f.set(4, y, "M3")
    for face in (b.front, b.back):
        face.hline(0, 7, 2, "P2")                                        # yoke seam
    jacket = g.part("jacket")
    for x, y in ((1, 0), (2, 1), (2, 2), (3, 3), (5, 3), (5, 2), (6, 1), (6, 0)):
        jacket.front.set(x, y, "M2")                                     # the signet's chain
    jacket.back.hline(1, 6, 0, "M2")
    signet = g.piece("signet", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(.5, 3.6, -2.6))
    solid(signet, "M", "smooth", 35441, 3, edge=False)
    signet.front.set(0, 0, "M4"), signet.front.set(1, 1, "M1")
    stand = collar(g, "stand_collar", "P", "velvet", base=1, height=1, y=-.6)
    stand.front.set(4, 0, "P3")
    sleeves(g, "S", "weave", 35442, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):                                        # slit oversleeves to the wrist
        over = g.part(f"{side}_sleeve")
        for face in over.sides:
            for y in range(10):
                for x in range(face.w):
                    face.set(x, y, "P1" if (x + face.x0) % 5 == 0 else "P2")
            face.hline(0, face.w - 1, 9, "P0")
        over.front.vline(1, 2, 8, "S3"), over.front.vline(2, 2, 8, "S2")
        over.front.set(1, 1, "M3"), over.front.set(2, 1, "M3")
        over.top.fill("P3")
    belt(g, "girdle", 9.6, role="L", base=1, height=1)
    # The charter: folded parchment at the right hip, three seal tags hanging below it.
    piv = (-1.6, 10.2, -3.0)
    charter = g.piece("charter", "TORSO", (-2.5, 0, -.5), (5, 2, 1), pivot=piv, motion="flap_front")
    solid(charter, "S", "plain", 35443, 4, edge=False)
    charter.front.hline(0, 4, 0, "S3"), charter.front.set(1, 1, "K2"), charter.front.set(3, 1, "K2")
    for i, (ox, n) in enumerate(((-2, 2), (0, 3), (2, 2))):
        tag = g.piece(f"seal_ribbon_{i}", "TORSO", (ox - .5, 2, -.5), (1, n, 1), pivot=piv, motion="flap_front")
        solid(tag, "A", "plain", 35444 + i, 2, edge=False)
        seal = g.piece(f"wax_seal_{i}", "TORSO", (ox - 1, 2 + n, -.6), (2, 2, 1), pivot=piv, motion="flap_front")
        solid(seal, "A", "smooth", 35447 + i, 1, edge=False)
        seal.front.set(0, 0, "A2"), seal.front.set(1, 1, "A0"), seal.front.set(1, 0, "A3")
    front, back = flaps(g, "gown", 9, "P", "velvet", 35450, base=1, top=10.6, hem="P0")
    front.vline(3, 0, 8, "P0"), front.vline(4, 0, 8, "P2")
    for face in (front, back):
        face.vline(1, 2, 7, "P0"), face.vline(7, 2, 7, "P2")
