"""Vine Dresser's Pruning Tunic: a short tunic with a vine-leaf border, twine-bound cuffs, a hooked pruning knife sheathed at the hip and a hank of willow ties."""
from kit import belt, body, flaps, neckline, sleeves
from kit_m01 import twist
from kit_male import blk

META = {
    "name": "Vine Dresser's Pruning Tunic",
    "gender": "male",
    "description": "A short pruning tunic bordered with stitched vine leaves, its cuffs bound tight with twine, a hooked pruning knife sheathed at the hip and a hank of willow ties at the belt.",
    "tags": ["work", "casual"],
    "covers_waist": True,
}

def build(g):
    b = body(g, "P", "twill", 31301)
    neckline(b.front, "v", "P")
    f = b.front
    for x, y in ((1, 0), (2, 1), (2, 2), (3, 3), (6, 0), (5, 1), (5, 2), (4, 4)):
        f.set(x, y, "A1")                                                 # stitched neck edge
    for x, y in ((0, 1), (1, 3), (7, 1), (6, 3), (2, 4), (5, 4)):
        f.set(x, y, "A3")                                                 # little leaves along it
    b.back.hline(1, 6, 0, "A1")
    for x in (1, 3, 5):
        b.back.set(x, 1, "A3")
    sleeves(g, "P", "twill", 31302, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for x in range(0, arm.strip.w, 2):                                # cuff gathered tight under twine
            arm.strip.vline(x, 8, 10, "P1")
        for y in (8, 10):
            twist(arm.strip, "L", 3, rows=[y], period=3)                  # two turns of twine
        tendril = blk(g, f"{side}_twine_end", (-1.0 if side == "right" else 1.0, 8.6, -2.3), (1, 2, 1), "L", 3,
                      "plain", 31303 + (side == "left"), bone=f"{side.upper()}_ARM", rotation=(-20, 0, 0), edge=False)
        tendril.strip.hline(0, tendril.strip.w - 1, 1, "L2")
    belt(g, "belt", 9.6, height=1)
    # Pruning knife: a slanted leather sheath at the left hip, the horn handle and its hook peeking out.
    sheath = blk(g, "knife_sheath", (2.7, 9.2, -2.9), (2, 4, 1), "L", 2, "leather", 31305, rotation=(0, 0, -18))
    sheath.front.vline(0, 0, 3, "L3"), sheath.front.hline(0, 1, 3, "L1")
    sheath.front.set(1, 1, "M3")
    handle = blk(g, "knife_handle", (2.3, 7.4, -2.9), (1, 2, 1), "S", 3, "plain", 31306, rotation=(0, 0, -18),
                 edge=False)
    handle.front.set(0, 0, "S4"), handle.front.set(0, 1, "S2")
    hook = blk(g, "knife_hook", (3.4, 8.9, -2.9), (1, 1, 1), "M", 3, "smooth", 31307, edge=False)
    hook.front.fill("M4")
    # A hank of willow ties folded over the belt on the right.
    for i, x in enumerate((-2.9, -2.3, -1.7)):
        withy = blk(g, f"willow_tie_{i}", (x, 9.0, -2.95), (1, 5, 1), "L", 3 + (i == 1), "plain", 31308 + i,
                    rotation=(0, 0, 6 - 6 * i), motion="flap_front", edge=False)
        withy.strip.hline(0, withy.strip.w - 1, 0, "L2")
        withy.strip.hline(0, withy.strip.w - 1, 4, "L2")
    knot = blk(g, "willow_tie_band", (-2.3, 9.9, -3.05), (3, 1, 1), "S", 2, "plain", 31311, motion="flap_front",
               edge=False)
    knot.front.set(1, 0, "S3")
    for face in flaps(g, "hem", 3, "P", "twill", 31312, top=10.8):
        face.hline(0, 8, 2, "A1")                                         # the vine's stem along the hem
        for x in (1, 4, 7):
            face.set(x, 1, "A3"), face.set(x + 1, 1, "A2")                # paired leaves
