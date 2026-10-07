"""Afro Puff: coily hair smoothed up into one big round puff at the crown, a slim cloth band at the hairline."""
from anime import ring_shell
from anime_female import coil_face, paint, SIDES
from paint import k, scalp, solid

META = {"name": "Afro Puff", "gender": "female",
        "description": "Coily hair gathered into a big round puff on the crown, with a slim cloth band at the hairline."}

# The puff: a wide middle tier, narrower tiers above and below, and swells that round it off.
# (size, centre relative to the puff's centre); all share one pivot so the puff tilts as one.
PUFF_CENTRE = (0, -10.9, 1.6)
PUFF = [((7, 4, 7), (0, 0, 0)), ((5, 1, 5), (0, -2.5, 0)), ((3, 1, 3), (0, -3.5, 0)), ((5, 1, 5), (0, 2.5, 0)),
        ((1, 3, 5), (-4.0, 0, 0)), ((1, 3, 5), (4.0, 0, 0)), ((5, 3, 1), (0, 0, -4.0)), ((5, 3, 1), (0, 0, 4.0))]


def build(g):
    scalp(g, 7801, side_rows=7, back_rows=8, sideburn=1)
    head = g.part("head")
    for face in (head.top, head.back, head.right, head.left):
        rows = 8 if face in (head.top, head.back) else 7
        coil_face(type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name), 7802 + face.x0, 2)
    ring_shell(g, 7803, side_rows=3, back_rows=5)
    for i, (size, (cx, cy, cz)) in enumerate(PUFF):
        w, h, d = size
        puff = g.piece(f"puff_{i}", "HEAD", (cx - w / 2, cy - h / 2, cz - d / 2), size, pivot=PUFF_CENTRE, rotation=(-18, 0, 0))
        paint(puff, "coil", 7810 + i * 3, 2 + (1 if i in (1, 2) else 0), top_delta=1)
    # A slim band from ear to ear just behind the hairline.
    band = g.piece("band", "HEAD", (-4.5, -.5, -1), (9, 1, 2), pivot=(0, -8.55, -2.6), inflate=.1)
    solid(band, "A", "plain", 7830, 2, edge=False)
    band.front.hline(0, 8, 0, k("A", 3))
    for side, sign in SIDES:
        drop = g.piece(f"{side}_band", "HEAD", (-.5, 0, -1), (1, 2, 2), pivot=(4.6 * sign, -8.6, -2.6), inflate=.1)
        solid(drop, "A", "plain", 7831, 2, edge=False)
        edge = g.piece(f"{side}_edge", "HEAD", (-.5, 0, -.5), (1, 2, 1), pivot=(4.2 * sign, -6.4, -3.8), rotation=(0, 0, -20 * sign))
        paint(edge, "coil", 7835 + (sign > 0), 2)
