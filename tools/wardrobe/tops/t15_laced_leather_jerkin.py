"""Laced Leather Jerkin: a sleeveless suede jerkin laced up the front over a full-sleeved shirt."""
from kit import body, neckline, sleeves
from paint import fabric, k, solid

META = {
    "name": "Laced Leather Jerkin",
    "gender": "male",
    "description": "Sleeveless dyed-suede jerkin, laced up the front, pointed tabs at the hem, over a full shirt.",
    "tags": ["casual", "rugged"],
}


def build(g):
    b = body(g, "S", "weave", 1501, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 1502, base=3, rows=(0, 10), cuff="S2")
    for side in ("right", "left"):
        for face in g.part(f"{side}_arm").sides:
            face.vline(2, 2, 8, "S2")
    jerkin = body(g, "P", "leather", 1503, layer="jacket", rows=(0, 10))
    jf = jerkin.front
    jf.clear(3, 0), jf.clear(4, 0)
    # Criss-cross lacing over a slim opening.
    for y in range(1, 10):   # ladder lacing across a dark opening
        key = "S3" if y % 2 else "P0"
        jf.set(3, y, key), jf.set(4, y, key)
    jf.vline(2, 1, 9, "P3"), jf.vline(5, 1, 9, "P1")
    for face in jerkin.sides:
        face.hline(0, face.w - 1, 10, "P1")
    jerkin.back.vline(3, 0, 10, "P1"), jerkin.back.vline(4, 0, 10, "P3")
    # Shoulder seams on the jacket top.
    jerkin.top.hline(0, 7, 1, "P1")
    for i, x in enumerate((-3.5, -1.2, 1.2, 3.5)):
        tab = g.piece(f"tab_{i}", "TORSO", (-1, 0, 0), (2, 2, 1), pivot=(x, 10.4, -2.75))
        solid(tab, "P", "leather", 1504 + i, 2)
        tab.front.set(0, 1, "P1"), tab.front.set(1, 1, "P3")
