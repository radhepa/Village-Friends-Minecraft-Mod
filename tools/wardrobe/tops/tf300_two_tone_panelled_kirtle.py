"""Two-Tone Panelled Kirtle: a kirtle pieced from a broad centre panel in one color and side panels in another, piped at every seam."""
from kit import SIDES, body
from kit_female import neck
from paint import fabric, strip_fabric

META = {
    "name": "Two-Tone Panelled Kirtle",
    "gender": "female",
    "description": "A kirtle pieced from a broad centre panel in one color and side panels in another, every seam piped in a bright cord, with sleeves in the side color and cuffs in the centre color.",
    "tags": ["casual", "tailored"],
}


def build(g):
    b = body(g, "S", "weave", 60560, base=2)
    for face in (b.front, b.back):
        fabric(face, "P", "weave", 60561 + (face is b.back), 2, 2, 0, 4, 12)   # the centre panel
        face.vline(1, 0, 11, "A2"), face.vline(6, 0, 11, "A2")              # piped seams
        face.vline(2, 1, 11, "P3"), face.vline(5, 1, 11, "P1")
    neck(b.front, "round", "P", 2, edge="P3")
    b.front.hline(2, 5, 11, "P1")
    for face in (b.right, b.left):
        face.vline(0, 2, 11, "S1"), face.vline(3, 2, 11, "S1")
    b.top.hline(0, 7, 3, "S3")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 60563 + (side == "left"), 2, 0, 9)
        fabric(arm.top, "S", "weave", 60565, 3)
        strip_fabric(arm, "P", "weave", 60566, 2, 10, 11)                    # cuffs in the centre color
        arm.strip.hline(0, 15, 9, "A2")
        outer = arm.right if side == "right" else arm.left
        outer.vline(2, 0, 8, "S1")
