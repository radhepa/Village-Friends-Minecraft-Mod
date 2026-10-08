"""Mountain Guide's Rope-Coiled Jacket: a channel-padded wool jacket with a knitted neck-wrap, a climbing rope worn across the chest and coiled on the back."""
from kit import SIDES, belt, body, collar, flaps, sleeves
from kit_male import blk, ribbing
from kit_m07 import baldric, coil, rope
from paint import k

META = {
    "name": "Mountain Guide's Rope-Coiled Jacket",
    "gender": "male",
    "description": "A guide's channel-padded wool jacket buttoned high under a thick knitted neck-wrap, a hemp climbing rope worn bandolier-fashion across his chest and coiled round his back, a piton hammer at the belt.",
    "tags": ["sturdy", "rugged", "work"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 37340)
    for face in b.sides:
        for y in range(2, 12, 3):
            face.hline(0, face.w - 1, y, "P1")                           # stitched padding channels
    b.front.vline(4, 1, 11, "P0")                                        # the buttoned front
    for y in (2, 5, 8):
        b.front.set(3, y, "L3")
    sleeves(g, "P", "weave", 37341, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for y in (2, 5):
            arm.strip.hline(0, arm.strip.w - 1, y, "P1")
        ribbing(arm.strip, "S", 2, rows=range(8, 11))                    # knitted wrist warmers
    wrap = collar(g, "neck_wrap", "A", "knit", base=2, height=2, y=-.8, inflate=.12)
    for face in wrap.sides:
        ribbing(face, "A", 2, rows=range(0, 2))
        face.hline(0, face.w - 1, 0, "A3")
    tail = blk(g, "neck_wrap_tail", (-2.0, 1.0, -2.9), (2, 4, 1), "A", 2, "knit", 37342)
    ribbing(tail.front, "A", 2), tail.front.hline(0, 1, 3, "A1")
    # The rope: across the chest from the left shoulder, then a big coil hung on the back.
    jacket = g.part("jacket")
    baldric(jacket.front, jacket.back, from_left=True, key="S3", edge="S1")
    for x in (1, 6):
        jacket.top.set(x, 0, "S3"), jacket.top.set(x, 1, "S2")
    for i, (size, rz, dz) in enumerate(((8, 0, 3.1), (7, 10, 4.1))):
        coil(g, f"rope_coil_{i}", (0, 5.0, dz), size=size, thick=1, depth=1, role="S", base=2 + i % 2,
             rotation=(0, 0, rz))
    tie = blk(g, "rope_tie", (0, 1.4, 3.7), (2, 2, 2), "S", 2, "plain", 37343, edge=False)
    rope(tie, "S", 1)
    belt(g, "belt", 9.4, height=1)
    # A piton hammer tucked slantwise through the belt at the right hip.
    haft = blk(g, "piton_hammer_haft", (-2.6, 8.6, -3.4), (1, 5, 1), "L", 3, "plain", 37344, rotation=(0, 0, 32),
               motion="flap_front", edge=False)
    haft.strip.hline(0, 3, 4, "L1")
    head = blk(g, "piton_hammer_head", (-2.6, 8.6, -3.4), (4, 1, 1), "M", 2, "smooth", 37345, rotation=(0, 0, 32),
               motion="flap_front", origin=(-1.5, -1, -.5), edge=False)
    head.front.set(0, 0, "M4"), head.front.set(3, 0, "M1"), head.back.set(3, 0, "M4"), head.back.set(0, 0, "M1")
    for face in flaps(g, "jacket_skirt", 3, "P", "weave", 37348, top=10.6):
        face.hline(0, 8, 2, k("P", 1))
