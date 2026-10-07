"""Liripipe Hood: a lowered hood with a dagged shoulder cape and a long liripipe tail, over a tunic."""
from kit import belt, body, neckline, sleeves
from paint import fabric, k, solid

META = {
    "name": "Liripipe Hood",
    "gender": "male",
    "description": "A lowered hood whose dagged shoulder cape and long liripipe tail hang over a belted tunic.",
    "tags": ["casual", "whimsical"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 1601, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 1602, base=3, rows=(0, 10), cuff="P2")
    belt(g, "belt", 9.6)
    cape = g.piece("hood_cape", "TORSO", (-6, -.8, -2.9), (12, 3, 6), inflate=.04)
    solid(cape, "P", "weave", 1603, 2)
    fabric(cape.top, "P", "weave", 1603, 3)
    for face in cape.sides:
        for x in range(face.w):
            face.set(x, 2, "A2" if x % 2 else "P1")      # dagged, accent-lined edge
    # Dags: little hanging points around the cape's hem.
    for i, (x, z) in enumerate(((-5.0, -3.2), (-2.4, -3.2), (2.4, -3.2), (5.0, -3.2), (-4, 3.4), (0, 3.4), (4, 3.4))):
        dag = g.piece(f"dag_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, 2.2, z))
        solid(dag, "P", "weave", 1610 + i, 2, edge=False)
        dag.strip.hline(0, dag.strip.w - 1, 1, "A2")
    hood = g.piece("hood", "TORSO", (-3.5, 0, 0), (7, 3, 2), pivot=(0, -1.0, 2.9), rotation=(16, 0, 0))
    solid(hood, "P", "weave", 1620, 2)
    hood.back.hline(0, 6, 0, "P3"), hood.back.vline(3, 1, 2, "P1")
    liripipe = g.piece("liripipe", "TORSO", (-.5, 0, -.5), (1, 9, 1), pivot=(.6, 1.6, 4.3), rotation=(12, 0, -8), motion="sway")
    solid(liripipe, "P", "weave", 1621, 2)
    liripipe.strip.hline(0, liripipe.strip.w - 1, 8, "A2")
