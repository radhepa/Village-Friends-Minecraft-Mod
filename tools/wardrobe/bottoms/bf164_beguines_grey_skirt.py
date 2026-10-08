"""Beguine's Grey Skirt: a long skirt of undyed grey tiretaine woven with a quiet hairline stripe, a
black bound hem and wooden pattens strapped over the shoes for the town's muddy lanes."""
from kit_female import shoes, skirt

META = {
    "name": "Beguine's Grey Skirt",
    "gender": "female",
    "description": "A long skirt of undyed grey wool woven with hairline stripes, a black bound hem and wooden pattens for the mud.",
    "tags": ["holy", "simple", "skirt", "long_skirt"],
}


def tiretaine(face):
    """Undyed grey cloth with a hairline stripe every third thread, the stripe darker below the knee crease."""
    for y in range(face.h):
        for x in range(face.w):
            key = "S2" if x % 3 == 1 else "S1"
            if x % 3 == 1 and y % 4 == 3:
                key = "S3"
            face.set(x, y, key)


def build(g):
    s = skirt(g, "S", "plain", 55141, base=1, top=9.8, length=12, back_length=12, flare=4, folds=False, gather=False)
    s.paint(tiretaine)
    for face in s.faces:
        face.hline(0, face.w - 1, 0, "S3")
        face.hline(0, face.w - 1, 1, "S0")
    s.hem("K2", rows=1)
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 2, "K3")
    for side in ("right", "left"):
        g.part(f"{side}_leg").strip.hline(0, 15, 10, "S0")
    shoes(g, "patten", "K", 2)
