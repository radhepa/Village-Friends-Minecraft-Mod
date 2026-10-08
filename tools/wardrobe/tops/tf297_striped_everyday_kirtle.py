"""Striped Everyday Kirtle: a kirtle of cheap striped ticking cut with the stripes running down, a plain yoke and plain cuffs."""
from kit import SIDES, body
from kit_female import neck
from paint import k

META = {
    "name": "Striped Everyday Kirtle",
    "gender": "female",
    "description": "A kirtle of cheap striped ticking with the stripes running straight down, finished with a plain contrasting yoke, plain cuffs and one button at the throat.",
    "tags": ["casual", "simple"],
}


def ticking(face, x0=0, y0=0, y1=None, offset=0):
    """Narrow light stripes on the ground cloth, every third thread a stripe, edges shaded."""
    y1 = face.h - 1 if y1 is None else y1
    for y in range(y0, y1 + 1):
        for x in range(x0, face.w):
            col = (x + face.x0 + offset) % 3
            face.set(x, y, "S3" if col == 1 else k("P", 2 if col else 1))


def build(g):
    b = body(g, "P", "weave", 60440)
    for face in b.sides:
        ticking(face, y0=2)
    for face in b.sides:
        face.hline(0, face.w - 1, 0, "A2"), face.hline(0, face.w - 1, 1, "A1")   # the plain yoke
    neck(b.front, "round", "A", 2)
    b.front.set(4, 1, "M3")                                            # one button at the throat
    b.front.hline(0, 7, 2, "A1")
    for face in b.sides:
        face.hline(0, face.w - 1, 2, "A1")
    b.top.fill("A3")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            ticking(face, y0=0, y1=9, offset=1)
        arm.top.fill("A3")
        arm.strip.hline(0, 15, 0, "A2")
        arm.strip.hline(0, 15, 10, "A2"), arm.strip.hline(0, 15, 11, "A1")
