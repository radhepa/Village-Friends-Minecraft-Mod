"""Jester's Motley: a chequered motley tunic with a dagged collar whose points end in bells, and bells at the elbows."""
from kit import body, sleeves
from kit_male import arm_blk, blk, check, shoulder_cape

META = {
    "name": "Jester's Motley",
    "gender": "male",
    "description": "A fool's motley of chequered quarters, a dagged collar whose points each end in a little bell, and bells at both elbows.",
    "tags": ["whimsical", "fancy"],
    "locked_to": "b67_jesters_bell_hose",
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "plain", 6701)
    for face in b.sides:
        check(face, "P2", "A2", size=2, ox=face.x0, oy=0)
    check(b.top, "P2", "A2", size=2)
    sleeves(g, "P", "plain", 6702, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        check(arm.strip, "A2" if side == "right" else "S3", "P2", size=2, rows=range(0, 11))
    cape = shoulder_cape(g, "dagged_collar", "A", "plain", 6703, length=2, width=11)
    for face in cape.sides:
        for x in range(face.w):
            face.set(x, 1, "A2" if x % 2 else "P2")
    for i, (x, z) in enumerate(((-4.0, -3.2), (-1.4, -3.2), (1.4, -3.2), (4.0, -3.2))):
        point = blk(g, f"collar_point_{i}", (x, 1.0, z), (1, 2, 1), "P" if i % 2 else "A", 2, "plain", 6704 + i)
        point.strip.hline(0, point.strip.w - 1, 1, "M3")                  # a bell at every point
    for i, side in enumerate(("right", "left")):
        bell = arm_blk(g, f"{side}_elbow_bell", side, 4.2, (1, 1, 1), "M", 3, "smooth", 6710 + i,
                       dx=-2.3 if side == "right" else 2.3)
        bell.bottom.fill("M1")
