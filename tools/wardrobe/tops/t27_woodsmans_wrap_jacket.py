"""Woodsman's Wrap Jacket: a wrap-front jacket tied with a cord, a leather shoulder patch for the axe."""
from kit import body, neckline, roll, sleeves
from paint import k, line, solid

META = {
    "name": "Woodsman's Wrap Jacket",
    "gender": "male",
    "description": "A wrap-front wool jacket tied at the waist, sleeves turned back, a leather patch on the shoulder.",
    "tags": ["casual", "rugged", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 2701, base=3)
    jacket = body(g, "P", "twill", 2702, layer="jacket")
    jf = jacket.front
    # The overlap: the wearer's left panel crosses to the right hip, edged in accent.
    for y in range(12):
        edge = max(0, 5 - y // 2)
        for x in range(edge):
            if y < 6:
                jf.set(x, y, None)
        if y < 6:
            jf.set(edge, y, "A2")
    for y in range(3):
        jf.set(0, y, "P2")
    line(jf, 5, 0, 1, 7, "P3")
    sleeves(g, "P", "twill", 2703, rows=(0, 7))
    roll(g, "P", 4.6, base=3)
    patch = g.piece("shoulder_patch", "RIGHT_ARM", (-3.25, -2.25, -2.3), (4, 3, 5), inflate=.05)
    solid(patch, "L", "leather", 2704, 2)
    for face in patch.sides:
        face.hline(0, face.w - 1, 2, "L1")
    cord = g.piece("tie_cord", "TORSO", (-4.6, 9.2, -2.6), (9, 1, 5), inflate=.06)
    solid(cord, "L", "leather", 2705, 3, edge=False)
    for i, rz in enumerate((10, -6)):
        end = g.piece(f"tie_end_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(2.0 + i * .9, 9.8, -2.85), rotation=(0, 0, rz), motion="sway")
        solid(end, "L", "leather", 2706 + i, 3)
