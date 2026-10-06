"""Short Locs: chunky jaw-length locs falling from a sectioned crown, a few short ones tipping over
the brow and two framing the temples."""
from anime_male import SIDES, chain, loc_face, taper
from paint import k

META = {"name": "Short Locs", "gender": "male",
        "description": "Chunky jaw-length locs falling from a sectioned crown, two framing the temples."}


def sections(face, base=2, rows=8):
    for y in range(rows):
        for x in range(face.w):
            face.set(x, y, k("H", base - (1 if x % 4 == 3 or y % 4 == 3 else 0)))


def build(g):
    head, hat = g.part("head"), g.part("hat")
    sections(head.top)
    for face in (head.right, head.left):
        sections(face, rows=6)
    sections(head.back)
    head.front.hline(0, 7, 0, "H1")
    sections(hat.top, 3)
    for face in (hat.right, hat.left, hat.back):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, 3, face.name)
        sections(sub, rows=3)
    hat.front.hline(0, 7, 0, "H2")
    # Locs lying out from the crown before they fall.
    for i, (x, z, rx, rz) in enumerate(((-1.6, -1.2, -78, 8), (1.6, -1.2, -78, -8), (-1.8, 1.4, 80, 10), (1.8, 1.4, 80, -10))):
        chain(g, f"crown_loc_{i}", (x, -9.1, z), [(2, 3, 2, (rx, 0, rz))], seed=4610 + i * 5, painter=loc_face)
    # Short locs tipping over the brow.
    for i, (x, rz) in enumerate(((-2.4, 6), (0, -2), (2.4, -8))):
        taper(g, f"brow_{i}", (x, -8.6, -4.35), (-14, 0, rz), ((2, 3, 1),), seed=4630 + i * 3, painter=loc_face)
    for side, sign in SIDES:
        taper(g, f"{side}_temple", (4.35 * sign, -7.9, -3.4), (0, 0, -4 * sign), ((2, 7, 2),), seed=4640 + (sign > 0), painter=loc_face)
        for j, (z, length) in enumerate(((-1.2, 7), (1.2, 8), (3.2, 7))):
            taper(g, f"{side}_loc_{j}", (4.5 * sign, -7.8, z), ((j - 1) * 6, 0, -(5 + j * 2) * sign), ((2, length, 2),),
                  seed=4650 + j * 3 + (sign > 0) * 11, painter=loc_face)
    for i, x in enumerate((-3.2, -1.1, 1.1, 3.2)):
        taper(g, f"back_loc_{i}", (x, -7.6, 4.5), (8 + (i % 2) * 6, 0, -x * 2.5), ((2, 8 + (i % 2), 2),), seed=4690 + i * 3,
              painter=loc_face)
