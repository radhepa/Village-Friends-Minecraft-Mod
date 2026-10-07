"""Heraldic Gown Skirt: the mi-parti skirt of a lady's arms, one side sown with stars, the other barred."""
from kit_female import motif, shoes, skirt

META = {
    "name": "Heraldic Gown Skirt",
    "gender": "female",
    "description": "The floor-length mi-parti skirt of a lady's arms: one side sown with gilt stars, the other barred.",
    "tags": ["fancy", "gown", "skirt", "long_skirt"],
    "locked_to": "tf057_heraldic_gown_bodice",
}


def halves(face, right_first):
    for y in range(face.h):
        for x in range(face.w):
            right = (x < face.w // 2) == right_first
            face.set(x, y, "P2" if right else ("S3" if (y // 2) % 2 else "A2"))


def build(g):
    s = skirt(g, "P", "velvet", 15711, top=9.8, length=12, folds=False, gather=False)
    halves(s.front.front, True)
    halves(s.back.back, False)
    for y in range(s.left.left.h):
        s.left.left.hline(0, 4, y, "S3" if (y // 2) % 2 else "A2")
    for face in (s.front.front,):
        for x, y in ((0, 2), (2, 6), (0, 9)):
            motif(face, x, y, "star", a="M3", b="M4")
    motif(s.back.back, 6, 3, "star", a="M3", b="M4"), motif(s.back.back, 7, 8, "star", a="M3", b="M4")
    motif(s.right.right, 1, 5, "star", a="M3", b="M4")
    shoes(g, "pointed", "K", 2)
