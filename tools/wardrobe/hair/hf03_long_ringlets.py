"""Long Ringlets: a soft curly crown and long spiral ringlets down the back and over the shoulders."""
from anime import ring_shell
from anime_female import fall, fringe, paint, strand, SIDES
from paint import curls_face, scalp

META = {"name": "Long Ringlets", "gender": "female",
        "description": "Long hair in bouncing spiral ringlets, with a curly crown and short curled bangs."}


def ringlet(sign, n):
    """Segments that step side to side, so each ringlet coils in silhouette."""
    if n == 3:
        return (2, 5, 0), (2, 5, .5 * sign), (1, 3, -.3 * sign)
    return (2, 5, 0), (2, 4, .5 * sign), (2, 4, -.4 * sign), (1, 3, .2 * sign)


def build(g):
    scalp(g, 5301, side_rows=7, back_rows=8, sideburn=0)
    hat = ring_shell(g, 5302, side_rows=7, back_rows=8)
    curls_face(hat.top, 5303, 3)
    for i, (x, z, rz) in enumerate(((-2.2, -1.6, 10), (2.2, -1.4, -10), (0, 1.4, 0))):
        crown = g.piece(f"crown_curl_{i}", "HEAD", (-1.5, -1.5, -1.5), (3, 2, 3), pivot=(x, -8.2, z), rotation=(-8, 0, rz))
        paint(crown, "curl", 5305 + i, 2, top_delta=1)
    fringe(g, "bang", [(-2.4, ((2, 2),), 12), (-.4, ((2, 2),), 2), (1.6, ((2, 2),), -8), (3.3, ((2, 2),), -14)], 5310, texture="curl")
    for side, sign in SIDES:
        strand(g, f"{side}_ringlet", (4.4 * sign, -7.4, -3.3), (0, 0, -4 * sign), ringlet(sign, 3), 2, 5320 + (sign > 0),
               texture="ringlet")
        cover = g.piece(f"{side}_cover", "HEAD", (-.5, 0, -2), (1, 7, 4), pivot=(4.45 * sign, -7.8, .8), rotation=(0, 0, -5 * sign))
        paint(cover, "curl", 5328 + (sign > 0), 2)
    fall(g, "back", [(-3.6, -7.4, 4.4, ringlet(-1, 3), 4, 6), (-2.1, -7.6, 4.95, ringlet(1, 3), 6, 3),
                     (-.7, -7.5, 4.4, ringlet(-1, 4), 3, 1), (.8, -7.6, 4.95, ringlet(1, 4), 6, -1),
                     (2.2, -7.5, 4.4, ringlet(-1, 3), 4, -3), (3.6, -7.4, 4.95, ringlet(1, 3), 6, -6)],
         5340, motion="sway", texture="ringlet", depth=2)
