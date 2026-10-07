"""Assayer's Chain Tunic: a velvet tunic hung with fine chains, leather wristlets, a loupe and a little balance at the belt."""
from kit import belt, body, neckline, sleeves
from kit_male import blk
from paint import fabric, line

META = {
    "name": "Assayer's Chain Tunic",
    "gender": "male",
    "description": "A goldsmith-assayer's velvet tunic draped with fine chains, leather wristlets, a loupe on a cord and a small balance.",
    "tags": ["fancy", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 6501)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "velvet", 6502, rows=(0, 10))
    for side in ("right", "left"):
        cuff = g.part(f"{side}_sleeve")
        fabric(cuff.strip, "L", "leather", 6503, 2, 0, 8, cuff.strip.w, 3)
        cuff.strip.hline(0, cuff.strip.w - 1, 8, "L3")
    jf = g.part("jacket").front
    for i, (y0, y1) in enumerate(((1, 4), (2, 6), (3, 8))):
        for x0, x1 in ((0, 3), (7, 4)):
            line(jf, x0, y0 - 1, x1, y1, "M3" if i % 2 == 0 else "M2")      # swags of chain
    jf.set(3, 8, "A3"), jf.set(4, 8, "A3")
    belt(g, "belt", 9.4, height=1)
    blk(g, "loupe", (-1.2, 7.6, -2.65), (1, 1, 1), "M", 3, "smooth", 6504, edge=False).front.fill("K3")
    beam = blk(g, "balance_beam", (2.6, 10.6, -2.8), (3, 1, 1), "M", 3, "smooth", 6505, edge=False)
    beam.front.set(1, 0, "M4")
    for i, x in enumerate((1.6, 3.6)):
        pan = blk(g, f"balance_pan_{i}", (x, 11.8, -2.8), (1, 1, 1), "M", 2, "smooth", 6506 + i, edge=False)
        pan.top.fill("M4")
