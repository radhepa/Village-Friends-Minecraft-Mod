"""Hedge-Layer's Arm-Guard Shirt: a heavy shirt with thick laced leather forearm guards, a hide shoulder pad and a billhook riding at the back of the belt."""
from kit import belt, body, flaps, sleeves
from kit_male import arm_blk, blk, lacing
from paint import k

META = {
    "name": "Hedge-Layer's Arm-Guard Shirt",
    "gender": "male",
    "description": "A heavy twill work shirt with thick leather guards laced over both forearms against the thorns, a hide pad on the right shoulder for stakes, and a billhook riding at the back of the belt.",
    "tags": ["work", "rugged", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 31401)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.hline(2, 5, 1, "P1")
    f.set(2, 0, "P3"), f.set(5, 0, "P1")
    f.vline(4, 2, 5, "P1")                                                # short buttoned placket
    for y in (2, 4):
        f.set(3, y, "L3")
    for face in (b.right, b.left):
        face.vline(1, 2, 11, "P1")
    sleeves(g, "P", "twill", 31402, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            face.vline(2, 1, 3, "P1")
    # Forearm guards: stiff stitched leather from wrist to elbow, laced up the inside.
    for side in ("right", "left"):
        guard = arm_blk(g, f"{side}_arm_guard", side, 3.8, (5, 6, 5), "L", 2, "leather", 31403 + (side == "left"))
        for face in guard.sides:
            face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 5, "L0")
            face.hline(0, face.w - 1, 1, "L1")
            for y in (2, 4):
                for x in range(0, face.w, 2):
                    face.set(x, y, "L3")                                  # quilted stitch rows
        inner = guard.left if side == "right" else guard.right
        lacing(inner, 1, 1, 4, "S3", "S1")
        guard.top.fill("L1")
        guard.bottom.fill("L1")
    # A hide pad on the right shoulder where the cut stakes ride.
    pad = arm_blk(g, "stake_pad", "right", -2.7, (5, 2, 5), "L", 3, "leather", 31405, inflate=.05)
    for face in pad.sides:
        face.hline(0, face.w - 1, 1, "L1")
        face.set(2, 0, "L4")
    pad.top.fill("L3")
    pad.top.hline(0, 4, 2, "L2")
    belt(g, "belt", 9.6)
    # The billhook in a ring at the back of the belt: ash haft and a broad hooked blade.
    haft = blk(g, "billhook_haft", (-2.4, 8.0, 3.4), (1, 4, 1), "L", 3, "plain", 31406, rotation=(0, 0, -10))
    haft.strip.hline(0, haft.strip.w - 1, 0, "L4")
    ring = blk(g, "billhook_ring", (-2.3, 10.0, 3.3), (2, 1, 1), "M", 2, "smooth", 31407, edge=False)
    ring.back.set(0, 0, "M3")
    blade = blk(g, "billhook_blade", (-2.0, 11.6, 3.45), (2, 3, 1), "M", 3, "smooth", 31408, rotation=(0, 0, -10),
                motion="flap_back")
    blade.back.vline(1, 0, 2, "M4"), blade.back.set(0, 2, "M2")
    tip = blk(g, "billhook_hook", (-1.1, 13.6, 3.45), (2, 1, 1), "M", 3, "smooth", 31409, rotation=(0, 0, 20),
              motion="flap_back", edge=False)
    tip.back.set(0, 0, "M4")
    for face in flaps(g, "shirt_tail", 3, "P", "twill", 31410, top=11.2):
        face.hline(0, 8, 2, k("P", 1))
        face.vline(4, 1, 2, "P1")
