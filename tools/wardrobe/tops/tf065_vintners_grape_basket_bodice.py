"""Vintner's Grape-Basket Bodice: a vine-embroidered bodice over elbow-rolled sleeves, with a tall wicker
hod of grapes carried on her back by two leather straps."""
from kit import roll
from kit_female import bodice, chemise, motif
from kit_f01 import produce, wicker
from paint import k, solid

META = {
    "name": "Vintner's Grape-Basket Bodice",
    "gender": "female",
    "description": "A bodice embroidered with a grapevine along its neckline, sleeves rolled to the elbow and a tall wicker hod heaped with grapes on her back.",
    "tags": ["work", "casual"],
}


def build(g):
    chemise(g, "S", 3, "weave", 51160, neckline="scoop", sleeve_rows=(0, 6))
    roll(g, "S", 3.6, base=3)
    b = bodice(g, "P", "weave", 51161, rows=(2, 9), neckline="scoop", point=True, edge="P3")
    for x in range(0, 8):
        b.front.set(x, 3 if x in (0, 7) else 2 if x in (1, 6) else 3, "L2")   # the vine stem along the neckline
    for x, y in ((0, 4), (6, 4)):
        motif(b.front, x, y, "berry", a="A1", b="A2", c="L2")          # little grape clusters
    b.front.set(2, 3, "P3"), b.front.set(5, 3, "P3")                   # vine leaves
    for y in range(5, 10):
        b.front.set(3, y, "P1"), b.front.set(4, y, "P3")
    # Two leather straps over the shoulders carrying the hod.
    for face in (b.front, b.back):
        for x in (1, 6):
            face.vline(x, 0, 9 if face is b.back else 2, "L2")
    j = g.part("jacket")
    j.top.vline(1, 0, 3, "L2"), j.top.vline(6, 0, 3, "L2")
    b.back.hline(1, 6, 5, "L1")
    # The hod: a tall wicker basket narrow at the bottom, a rim of bound withies, grapes heaped above it.
    hod = g.piece("hod", "TORSO", (-3.5, 0, 0), (7, 9, 4), pivot=(0, 1.8, 2.6))
    for f in hod.sides:
        wicker(f, "L", 2, offset=f.x0)
    hod.top.fill("L1"), hod.bottom.fill("L1")
    rim = g.piece("hod_rim", "TORSO", (-3.5, 0, 0), (7, 1, 4), pivot=(0, 1.6, 2.6), inflate=.15)
    solid(rim, "L", "smooth", 51162, 3, edge=False)
    for f in rim.sides:
        for x in range(f.w):
            f.set(x, 0, k("L", 3 if x % 2 else 2))
    rim.top.fill("L1")
    foot = g.piece("hod_foot", "TORSO", (-2.5, 0, 0), (5, 1, 3), pivot=(0, 10.8, 3.1))
    solid(foot, "L", "smooth", 51163, 1, edge=False)
    for i, (x, y, z) in enumerate(((-1.8, 1.1, 5.2), (.2, 1.0, 5.0), (2.0, 1.2, 5.4), (-.6, 1.3, 3.8), (1.2, 1.4, 3.6))):
        grapes = produce(g, f"grapes_{i}", "TORSO", (x, y, z), 2, role="A", base=1, stem="L2", seed=51164 + i)
        for f in grapes.sides:
            f.set(1, 0, "A2"), f.set(0, 1, "A0")
    leaf = g.piece("vine_leaf", "TORSO", (-1, -.5, 0), (2, 1, 2), pivot=(2.6, 1.2, 4.2), rotation=(0, 0, -20))
    solid(leaf, "P", "plain", 51170, 2, edge=False)
    leaf.top.fill("P3")
