"""Quilted Sleeveless Vest: a channel-quilted vest with bound edges and cloth ties over a shirt, a kitchen cloth tucked at the hip."""
from kit import SIDES, body, sleeves
from kit_m10 import channels, tie
from kit_male import blk, check
from paint import k

META = {
    "name": "Quilted Sleeveless Vest",
    "gender": "male",
    "description": "A warm sleeveless vest quilted in level channels, every edge bound in a contrast tape and closed with cloth ties, over a shirt with its sleeves pushed up, a checked cloth tucked at the hip.",
    "tags": ["casual", "simple", "work"],
}


def build(g):
    shirt = body(g, "S", "weave", 40180, base=3)
    shirt.front.vline(4, 1, 3, "S2")
    vest = g.part("jacket")
    for face in vest.sides:
        channels(face, "P", 2, period=3, rows=range(0, 12))
    channels(vest.top, "P", 3, period=3, vertical=True)
    vest.bottom.fill("P1")
    f, bk = vest.front, vest.back
    # Round neck and the edge-to-edge front, both bound in tape.
    for x, y in ((2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1)):
        f.clear(x, y)
    for x, y in ((1, 0), (2, 1), (6, 0), (5, 1)):
        f.set(x, y, "A2")
    f.vline(3, 2, 11, "A2"), f.vline(4, 2, 11, "A1")
    bk.hline(1, 6, 0, "A2")
    for face in vest.sides:
        face.hline(0, face.w - 1, 11, "A1")                               # bound hem
    for face in (vest.right, vest.left):
        face.vline(1 if face is vest.right else 2, 0, 3, "A2")            # bound armhole
    # Shirt sleeves pushed up to the elbow, gathered at the push.
    sleeves(g, "S", "weave", 40181, base=3, rows=(0, 5))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for x in range(arm.strip.w):
            arm.strip.set(x, 5, "S2" if x % 2 else "S4")
    # Cloth ties at the chest and waist.
    for i, (y, rz) in enumerate(((3.2, 10), (6.6, -8))):
        tie(g, f"vest_tie_{i}", "TORSO", (.1, y, -2.6), "A", 2, 2, 40182 + i, rotation=(0, 0, rz))
        blk(g, f"vest_knot_{i}", (0, y - .4, -2.6), (1, 1, 1), "A", 3, "plain", 40184 + i, edge=False)
    # A checked kitchen cloth tucked into the vest at the left hip.
    cloth = blk(g, "kitchen_cloth", (2.7, 9.4, -2.55), (2, 4, 1), "S", 3, "plain", 40186, motion="sway",
                rotation=(0, 0, -6))
    for face in cloth.sides:
        check(face, "S4", "A2", 1)
    cloth.top.fill("S3"), cloth.bottom.fill("A1")
    for face in (cloth.front, cloth.back):
        face.hline(0, face.w - 1, 0, k("S", 2))
