"""Miller's Sack-Pad Tunic: a dusty tunic with a quilted sack pad on one shoulder and a knotted neckerchief."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import arm_blk, blk, flecks, lozenge

META = {
    "name": "Miller's Sack-Pad Tunic",
    "gender": "male",
    "description": "A flour-dusted work tunic with a quilted pad on the shoulder for hauling sacks, a neckerchief and a rope belt.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 3201)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 3202, rows=(0, 10), cuff="P1")
    for face in b.sides:
        flecks(face, "P3", 3203, .08, rows=range(6, 12))          # flour settles low
    for side in ("right", "left"):
        flecks(g.part(f"{side}_arm").strip, "P3", 3204, .06, rows=range(5, 11))
    # The quilted sack pad rides the right shoulder.
    pad = arm_blk(g, "sack_pad", "right", -2.6, (5, 2, 6), "S", 2, "quilt", 3205, inflate=.12)
    for face in pad.sides:
        lozenge(face, "S", 2, step=3)
        face.hline(0, face.w - 1, 0, "S3")
    lozenge(pad.top, "S", 3, step=3)
    # Neckerchief knotted at the throat.
    ker = blk(g, "kerchief", (0, .2, -2.65), (3, 2, 1), "A", 2, seed=3206, edge=False)
    ker.front.hline(0, 2, 0, "A3"), ker.front.set(0, 1, "A1"), ker.front.set(2, 1, "A1")
    blk(g, "kerchief_knot", (0, -.3, -3.1), (1, 1, 1), "A", 3, seed=3207, edge=False)
    # Rope belt with a hanging end.
    rope = belt(g, "rope_belt", 9.4, role="S", base=1, height=1, buckle=None)
    for face in rope.sides:
        for x in range(face.w):
            face.set(x, 0, "S3" if x % 2 else "S1")
    end = blk(g, "rope_end", (-2.2, 10.0, -2.85), (1, 3, 1), "S", 2, seed=3208, motion="sway")
    end.strip.hline(0, end.strip.w - 1, 2, "S3")
    for face in flaps(g, "hem", 3, "P", "weave", 3209, top=10.4):
        flecks(face, "S2", 3210, .14, rows=range(1, 3))
        face.hline(0, 8, 2, "P1")
