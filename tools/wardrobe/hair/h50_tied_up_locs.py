"""Tied-Up Locs: locs drawn up from every side and bound high at the crown with a cloth wrap, their
ends spilling out of the top like a fountain; two short locs left loose at the temples."""
from anime_male import SIDES, chain, loc_face, taper, tie
from paint import k

META = {"name": "Tied-Up Locs", "gender": "male",
        "description": "Locs drawn up and bound high at the crown with a cloth wrap, the ends spilling over."}

# The ends spilling out of the wrap: (heading round the crown, tilt from hanging straight down)
SPILL = [(0, 62), (60, 54), (120, 66), (180, 58), (240, 50), (300, 64)]


def pulled_up(face, base=2, rows=8):
    """Locs drawn up toward the crown: vertical ridges with the sections between them."""
    for y in range(rows):
        for x in range(face.w):
            face.set(x, y, k("H", base - (1 if x % 3 == 2 else 0) + (1 if x % 3 == 0 and y % 3 == 0 else 0)))


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face in (head.top, head.back):
        pulled_up(face)
    for face in (head.right, head.left):
        pulled_up(face, rows=6)
    head.front.hline(0, 7, 0, "H1")
    for face, rows in ((hat.top, 8), (hat.back, 6), (hat.right, 4), (hat.left, 4)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name)
        pulled_up(sub, 2 + (face is hat.top))
    hat.front.hline(0, 7, 0, "H2")
    # The bundle rising from the crown, bound with a cloth wrap.
    for i, (x, z) in enumerate(((-1.0, -.4), (1.0, -.4), (0, 1.2))):
        taper(g, f"bundle_{i}", (x, -8.3, z + .4), (0, 0, x * 4), ((2, 3, 2),), seed=5010 + i * 3, up=True, painter=loc_face)
    tie(g, "wrap", (0, -10.0, .6), (4, 2, 4), role="A", inflate=.15, seed=5020)
    # The loc ends spilling out over the wrap.
    for i, (heading, tilt) in enumerate(SPILL):
        chain(g, f"spill_{i}", (0, -11.0, .6), [(2, 2, 2, (180, heading, 0)), (2, 4, 2, (tilt + 14, heading, 0))],
              seed=5030 + i * 7, painter=loc_face, overlap=.6)
    # Two locs left loose at the temples.
    for side, sign in SIDES:
        taper(g, f"{side}_loose", (4.35 * sign, -7.9, -3.2), (0, 0, -5 * sign), ((2, 6, 2),), seed=5060 + (sign > 0), painter=loc_face)
