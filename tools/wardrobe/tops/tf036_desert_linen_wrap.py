"""Desert Linen Wrap: layered white linen wrapped across the body, a long fringed scarf over one shoulder and bangles."""
from kit_female import arm_rings, bells, chemise, trim
from paint import line, solid

META = {
    "name": "Desert Linen Wrap",
    "gender": "female",
    "description": "Layered white linen wrapped across the body, an embroidered neckline, a fringed shoulder scarf and bangles.",
    "tags": ["relaxed", "casual"],
}


def build(g):
    body, arms = chemise(g, "S", 4, "weave", 13601, neckline="slit", sleeve_rows=(0, 5), gather=False)
    trim(body.front, 1, "cross", "A2", "M3", x0=1, x1=6)
    line(body.front, 7, 2, 1, 11, "S2")                              # the wrap's diagonal edge
    line(body.front, 7, 3, 2, 11, "S3")
    bells(g, "S", "weave", 13602, base=4, y=1.6, h=3, size=6, lining="S2")
    for box in arm_rings(g, "bangle", 8.4, 1, 5, inflate=.08):
        solid(box, "M", "smooth", 13603, 3, edge=False)
    scarf = g.piece("scarf_front", "TORSO", (-1, 0, 0), (2, 10, 1), pivot=(2.8, -.6, -2.8), rotation=(0, 0, -6))
    solid(scarf, "A", "weave", 13604, 2)
    over = g.piece("scarf_shoulder", "TORSO", (-1.2, -.6, -2.8), (3, 1, 6), pivot=(2.8, 0, 0), inflate=.05)
    solid(over, "A", "weave", 13605, 2, edge=False)
    back = g.piece("scarf_back", "TORSO", (-1, 0, 0), (2, 9, 1), pivot=(2.8, -.6, 2.4), rotation=(4, 0, -4))
    solid(back, "A", "weave", 13606, 2)
    for box in (scarf, back):
        face = box.front if box is scarf else box.back
        face.hline(0, 1, 2, "M3")
        for x in range(2):
            face.set(x, face.h - 1, "S3" if x % 2 else "A1")         # fringe
