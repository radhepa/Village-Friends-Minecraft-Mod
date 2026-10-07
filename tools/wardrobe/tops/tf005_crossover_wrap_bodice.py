"""Crossover Wrap Bodice: a spinner's wrap bodice crossed over the chest and tied in a bow at the side."""
from kit import sleeves
from kit_female import chemise, hanging
from paint import fabric, line, solid, strip_fabric

META = {
    "name": "Crossover Wrap Bodice",
    "gender": "female",
    "description": "A spinner's wrap bodice crossed left over right, tied with a bow at the side, over chemise frills.",
    "tags": ["casual", "relaxed"],
}


def build(g):
    chemise(g, "S", 3, "weave", 10501, neckline="scoop", sleeve_rows=(0, 11))
    j = g.part("jacket")
    strip_fabric(j, "P", "weave", 10502, 2, 0, 9)
    fabric(j.top, "P", "weave", 10502, 3)
    f = j.front
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (5, 1), (4, 2), (5, 2), (5, 3)]:
        f.clear(x, y)                                      # the V where the wrap opens over the chemise
    line(f, 6, 0, 1, 9, "A2")                              # the bound edge of the upper wrap
    line(f, 7, 0, 2, 9, "A1")
    line(f, 2, 0, 4, 3, "A2")                              # the under wrap's edge
    f.hline(0, 7, 9, "P1")
    for face in (j.right, j.left, j.back):
        face.hline(0, face.w - 1, 9, "P1")
    j.back.vline(3, 1, 8, "P1")
    sleeves(g, "P", "weave", 10503, rows=(0, 7), layer="sleeve")
    for side in ("right", "left"):
        g.part(f"{side}_sleeve").strip.hline(0, 15, 7, "P1")
        arm = g.part(f"{side}_arm")
        for x in range(0, 16, 2):
            arm.strip.set(x, 8, "S4")                      # the chemise frill below the cuff
        arm.strip.hline(0, 15, 11, "S2")
    knot = g.piece("bow_knot", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.8, 8.0, -2.85))
    solid(knot, "P", "weave", 10504, 2)
    for side, rot in (("right", 25), ("left", -25)):
        loop = g.piece(f"bow_loop_{side}", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.8 + (-1.4 if side == "right" else 1.4), 7.7, -2.8),
                       rotation=(0, 0, rot))
        solid(loop, "P", "weave", 10505, 3)
    for i, (x, length) in enumerate(((-3.2, 5), (-2.4, 4))):
        hanging(g, f"bow_tail_{i}", x, length, role="P", base=2, top=8.8, end="P1", texture="weave")
