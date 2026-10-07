"""Painter's Splattered Smock: a loose smock spattered with paint, a soft round collar, a knotted neckerchief and brushes."""
from kit_female import chemise, collar_flat, splotch
from paint import solid

META = {
    "name": "Painter's Splattered Smock",
    "gender": "female",
    "description": "A loose smock spattered in every color, a soft round collar, a knotted neckerchief and brushes in the pocket.",
    "tags": ["casual", "whimsical"],
}


def build(g):
    body, arms = chemise(g, "S", 4, "weave", 14601, neckline="round", sleeve_rows=(0, 11), gather=False)
    for face in (body.front, body.back):
        for x in range(1, 8, 2):
            face.vline(x, 3, 11, "S3")                               # loose folds
    for i, key in enumerate(("A2", "P2", "M3", "A3", "L2")):
        splotch(body.front, key, 14602 + i, count=1, y0=3, y1=10, size=2)
        splotch(body.back, key, 14612 + i, count=1, y0=4, y1=10, size=1)
    for arm in arms:
        arm.strip.hline(0, 15, 10, "S2")
        splotch(arm.strip, "A2", 14620, count=2, y0=5, y1=9, size=1)
        splotch(arm.strip, "P2", 14621, count=2, y0=4, y1=9, size=1)
    body.front.hline(5, 7, 4, "S2"), body.front.vline(5, 4, 6, "S2")  # pocket
    collar_flat(g, "collar", "S", 4, edge="S3")
    knot = g.piece("neckerchief_knot", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(0, 1.0, -2.8))
    solid(knot, "A", "plain", 14622, 2)
    for i, (x, key) in enumerate(((5.4, "A"), (6.0, "P"), (6.6, "M"))):
        brush = g.piece(f"brush_{i}", "TORSO", (-.5, -2.5, -.5), (1, 3, 1), pivot=(x - 3.0, 4.6, -2.6), rotation=(0, 0, -8 + 8 * i))
        solid(brush, "L", "smooth", 14623 + i, 3)
        brush.top.fill(f"{key}3")
