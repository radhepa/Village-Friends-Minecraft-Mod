"""Maypole Ribbon Bodice: a white festival bodice with a flower garland at the neckline and ribbons streaming behind."""
from kit_female import bodice, chemise, lacing, motif, puffs
from paint import solid

META = {
    "name": "Maypole Ribbon Bodice",
    "gender": "female",
    "description": "A white festival bodice with a garland of flowers at the neckline, a posy and long ribbons streaming behind.",
    "tags": ["whimsical", "fancy"],
    "locked_to": "bf032_maypole_flower_skirt",
}


def build(g):
    chemise(g, "S", 4, "weave", 13201, neckline="wide", sleeve_rows=(0, 3))
    puffs(g, "S", "weave", 13202, base=4, y=-2.4, h=4, band_key="A2")
    b = bodice(g, "S", "weave", 13203, rows=(2, 9), neckline="square", base=3, point=True)
    lacing(b.front, 3, 4, 8, "ladder", lace="A2", under="S4", eyelet=None)
    for x in range(0, 8):
        b.front.set(x, 2, ["A2", "P3", "A3", "M3"][x % 4])          # a garland of tiny flowers
    for x in range(0, 8):
        b.back.set(x, 2, ["A2", "P3", "A3", "M3"][(x + 1) % 4])
    posy = g.piece("posy", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.2, 3.6, -2.75))
    solid(posy, "A", "plain", 13204, 3, edge=False)
    posy.front.set(0, 0, "M4"), posy.front.set(1, 1, "P3")
    for i, (x, key, length) in enumerate(((-2.2, "A", 12), (-.7, "P", 13), (.8, "M", 12), (2.3, "A", 11))):
        rib = g.piece(f"ribbon_{i}", "TORSO", (-.5, 0, 0), (1, length, 1), pivot=(x, .2, 2.4), rotation=(8, 0, 0), motion="sway")
        solid(rib, key, "plain", 13205 + i, 3 if key != "P" else 2)
