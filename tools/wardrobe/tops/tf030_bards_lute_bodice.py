"""Bard's Lute Bodice: a ribbon-sashed bodice with slashed puff sleeves and a lute slung across her back."""
from kit_female import bodice, chemise, lacing, puffs
from paint import fabric, line, solid

META = {
    "name": "Bard's Lute Bodice",
    "gender": "female",
    "description": "A laced bodice with slashed puff sleeves, a ribbon sash with a rosette and a lute slung across the back.",
    "tags": ["whimsical", "fancy"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 13001, neckline="scoop", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 10, "A2")
    puffs(g, "P", "velvet", 13002, base=2, y=-2.4, h=4, slash="S4", band_key="A2")
    b = bodice(g, "P", "velvet", 13003, rows=(2, 9), neckline="square", edge="A2")
    lacing(b.front, 3, 3, 8, "x", lace="A3", under="S3", eyelet="M3")
    j = g.part("jacket")
    for dx in (0, 1):
        line(j.front, 7 - dx, 1, 0, 8 - dx, "A2" if dx else "A3")   # the ribbon sash
    line(j.back, 0, 1, 7, 8, "A2")
    rosette = g.piece("rosette", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.4, 6.8, -2.75))
    solid(rosette, "A", "plain", 13004, 3, edge=False)
    rosette.front.set(0, 0, "M3")
    lute = g.piece("lute_body", "TORSO", (-2.5, -3, -1), (5, 6, 2), pivot=(-1.2, 7.0, 3.6), rotation=(0, 0, -35))
    solid(lute, "L", "smooth", 13005, 3)
    lute.back.set(1, 2, "K1"), lute.back.set(3, 2, "K1"), lute.back.set(1, 3, "K1"), lute.back.set(3, 3, "K1")
    lute.back.vline(2, 0, 5, "S4")                                   # strings over the carved rose
    lute.back.hline(1, 3, 5, "L1")                                   # the bridge
    neck_ = g.piece("lute_neck", "TORSO", (-.5, -9, -.5), (1, 6, 1), pivot=(-1.2, 7.0, 3.6), rotation=(0, 0, -35))
    solid(neck_, "L", "smooth", 13006, 2)
    peg = g.piece("lute_pegbox", "TORSO", (-1, -10, -.5), (2, 1, 1), pivot=(-1.2, 7.0, 3.6), rotation=(0, 0, -35))
    solid(peg, "L", "smooth", 13007, 1, edge=False)
