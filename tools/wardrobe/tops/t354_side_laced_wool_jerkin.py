"""Side-Laced Wool Jerkin: a sleeveless wool jerkin closed at the front and laced up both sides with leather thongs over a full shirt."""
from kit import SIDES, body, collar, flaps, sleeves
from kit_m10 import tie
from paint import dark_seams

META = {
    "name": "Side-Laced Wool Jerkin",
    "gender": "male",
    "description": "A sleeveless wool jerkin with a plain closed front and a leather-bound neck, laced down both sides with thongs that let the shirt show between, over full linen sleeves.",
    "tags": ["casual", "simple", "rugged"],
}


def side_lacing(face, x_gap, x_edge, rows):
    """Lacing across a gap at one edge of a panel: thong crossings on even rows, shirt showing between."""
    for y in rows:
        if y % 2 == 0:
            face.set(x_gap, y, "L3")
        else:
            face.clear(x_gap, y)
        face.set(x_edge, y, "L1" if y % 2 else "P1")                     # eyelets along the panel edge


def build(g):
    shirt = body(g, "S", "weave", 40420, base=3)
    jerkin = body(g, "P", "weave", 40421, layer="jacket")
    f, bk = jerkin.front, jerkin.back
    f.clear(3, 0), f.clear(4, 0)
    for face in (f, bk):
        side_lacing(face, 0, 1, range(2, 11))
        side_lacing(face, 7, 6, range(2, 11))
        face.hline(1, 6, 11, "L2")                                        # leather-bound hem
    f.set(2, 0, "L2"), f.set(5, 0, "L2")
    f.vline(4, 2, 10, "P1")                                               # centre seam
    bk.vline(3, 1, 10, "P1")
    dark_seams(jerkin, faces=("right", "left"))
    collar(g, "jerkin_collar", "L", "leather", base=2, height=1, y=-.4)
    sleeves(g, "S", "weave", 40422, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for x in range(arm.strip.w):
            arm.strip.set(x, 9, "S2" if x % 2 else "S3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S4")
        arm.strip.hline(0, arm.strip.w - 1, 0, "L2")                      # leather-bound armhole
    # Lace tags hanging from the foot of each side lacing, and a short skirt.
    for i, x in enumerate((-3.6, 3.6)):
        tie(g, f"lace_tag_{i}", "TORSO", (x, 10.6, -2.45), "L", 2, 3, 40423 + i)
    for face in flaps(g, "jerkin_skirt", 2, "P", "weave", 40425, top=11.2):
        face.hline(0, 8, 1, "L2")
