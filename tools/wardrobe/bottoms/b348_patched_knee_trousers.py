"""Patched-Knee Trousers: worn wool trousers mended with odd patches at both knees and the back of one thigh, frayed over ankle boots."""
from kit import SIDES, belt, footwear, legs, waistband
from kit_m10 import outer

META = {
    "name": "Patched-Knee Trousers",
    "gender": "male",
    "description": "Old wool trousers mended with mismatched cloth patches at both knees and the back of one thigh, frayed hems falling over scuffed ankle boots.",
    "tags": ["casual", "simple", "rugged"],
}


def square_patch(face, x0, y0, w, h, role, cross):
    """A sewn square patch on the trouser overlay: lit top, shaded bottom, a cross-stitch at two corners."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            face.set(x, y, f"{role}{3 if y == y0 else 1 if y == y0 + h - 1 else 2}")
    face.set(x0, y0, cross), face.set(x0 + w - 1, y0 + h - 1, cross)


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "twill", 40120, rows=(0, 8), crease=False)):
        outer(leg, side).vline(2, 1, 8, "P1")                            # side seam
        leg.front.vline(1 if side == "right" else 2, 1, 3, "P1")         # baggy thigh fold
    waistband(g, "P", "twill", 40121)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        if side == "right":
            square_patch(pants.front, 0, 4, 4, 3, "S", "K1")             # broad linen patch
        else:
            square_patch(pants.front, 1, 5, 3, 3, "A", "K1")             # small bright offcut
            square_patch(pants.back, 0, 1, 3, 3, "S", "K1")              # a seat-side mend behind
        # Frayed hem breaking over the boot tops.
        for face in pants.sides:
            for x in range(face.w):
                face.set(x, 9, "P1" if x % 2 else "P2")
                face.set(x, 10, "L2" if x % 2 else "P1")
    belt(g, "waist_belt", 9.4, height=1, buckle="M")
