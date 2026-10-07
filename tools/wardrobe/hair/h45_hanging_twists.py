"""Hanging Twists: many slim two-strand twists falling from a sectioned crown to the ears and nape,
a few short ones tipping over the brow."""
from anime_male import SIDES, taper, twist_face
from paint import k

META = {"name": "Hanging Twists", "gender": "male",
        "description": "Many slim two-strand twists falling to the ears and nape, a few short ones over the brow."}


def sections(face, base=2, rows=8):
    """A sectioned scalp: small square parts with the twists' roots between them."""
    for y in range(rows):
        for x in range(face.w):
            face.set(x, y, k("H", base - (1 if x % 3 == 2 or y % 3 == 2 else 0)))


def strand(face, seed, base=2):
    """A slim twist: the two strands cross every texel, light on alternate sides."""
    twist_face(face, seed, base, period=2)
    for y in range(0, face.h, 4):
        for x in range(face.w):
            face.set(x, y, k("H", base + 1))


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
    # Short twists over the brow.
    for i, (x, rz) in enumerate(((-3.0, 10), (-1.1, 2), (.8, -4), (2.7, -12))):
        taper(g, f"brow_{i}", (x, -8.55, -4.3), (-14, 0, rz), ((1, 3, 1),), seed=4510 + i * 3, painter=strand)
    # Slim twists round the temples, sides and back, each hanging at its own angle.
    for side, sign in SIDES:
        taper(g, f"{side}_temple", (4.4 * sign, -7.9, -3.7), (0, 0, -4 * sign), ((1, 5, 1),), seed=4520 + (sign > 0), painter=strand)
        for j, z in enumerate((-2.4, -1.0, .4, 1.8, 3.2)):
            taper(g, f"{side}_twist_{j}", (4.5 * sign, -7.8, z), ((j - 2) * 4, 0, -(5 + (j % 2) * 5) * sign), ((1, 4 + (j % 2), 1),),
                  seed=4530 + j * 3 + (sign > 0) * 13, painter=strand)
    for i, x in enumerate((-3.5, -2.3, -1.1, 0, 1.1, 2.3, 3.5)):
        taper(g, f"back_twist_{i}", (x, -7.6, 4.5), (8 + (i % 2) * 6, 0, -x * 3), ((1, 5 + (i % 2), 1),), seed=4570 + i * 3,
              painter=strand)
    # Crown twists lying out from the top.
    for i, (x, z, rx, rz) in enumerate(((-1.6, -.8, -72, 6), (1.6, -.8, -72, -6), (-1.6, 1.6, 72, 8), (1.6, 1.6, 72, -8))):
        taper(g, f"crown_twist_{i}", (x, -8.6, z), (rx, 0, rz), ((1, 3, 1),), seed=4590 + i * 3, painter=strand)
