"""Half-Shaved Drape: the wearer's right side shaved close, the long top parted at its edge and draped
over the crown to hang down the left side to the jaw."""
from anime import cel_face
from anime_male import chain, shave, taper
from paint import hair_face, k

META = {"name": "Half-Shaved Drape", "gender": "male",
        "description": "One side shaved close, the long top draped over to hang down the other side."}

# (z, thickness, length down the left side)
DRAPE = [(-3.2, 2, 6), (-1.4, 1, 7), (.4, 1, 7), (2.2, 1, 6), (3.7, 1, 5)]


def build(g):
    head, hat = g.part("head"), g.part("hat")
    hair_face(head.top, 6801, 2)
    hair_face(head.left, 6802, 2)
    hair_face(head.back, 6803, 2, rows=range(7))
    shave(head.right, 6804, range(8))
    shave(head.back, 6805, range(7), cols=range(5, 8))
    shave(head.top, 6806, range(8), cols=[0])
    shave(head.front, 6807, [0], cols=[0, 1])
    head.front.hline(2, 7, 0, "H1")
    for y in range(8):
        for x in range(1, 8):
            hat.top.set(x, y, k("H", 3 - (1 if x == 1 or (x + y) % 4 == 0 else 0)))
    for face, rows in ((hat.left, 8), (hat.back, 7)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w if face is hat.left else 5, rows, face.name)
        cel_face(sub, 6808 + face.x0, 2, 1, tip_dark=False)
    hat.front.hline(2, 7, 0, "H2")
    # Locks from the part across the crown, then down the left side, ending in points at the jaw.
    for i, (z, thick, length) in enumerate(DRAPE):
        y = -8.85 - (thick - 1) * .4 - (.15 if i % 2 else 0)
        chain(g, f"drape_{i}", (-2.9, y, z), [(thick, 7, 2, (0, 0, -86)), (1, length, 2, (0, 0, -6 - i)), (1, 2, 1, (0, 0, -2))],
              seed=6810 + i * 7, ring=1, overlap=.45)
    # A lock from the part over the brow, lifting off it toward the left.
    taper(g, "brow", (-2.6, -8.9, -4.35), (-6, 0, -74), ((2, 5, 1), (1, 1, 1)), seed=6850, ring=0)
    for i, (x, rz) in enumerate(((-.4, -14), (2.0, -20))):
        taper(g, f"back_{i}", (x, -7.6, 4.5), (6, 0, rz), ((2, 6, 1), (1, 2, 1)), seed=6860 + i * 3, ring=1)
