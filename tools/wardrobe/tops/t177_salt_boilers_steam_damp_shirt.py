"""Salt Boiler's Steam-Damp Shirt: an open-necked linen shirt clinging dark with steam, sleeves rolled into crusts of
white salt, and the long wooden rake of the salt pans slung across the back."""
from kit import body, neckline, sleeves
from kit_male import arm_blk, blk
from paint import grid, line

META = {
    "name": "Salt Boiler's Steam-Damp Shirt",
    "gender": "male",
    "description": "An open-necked linen shirt clinging dark with steam from the pans, sleeves rolled into crusts of white "
                   "salt, and the long wooden salt rake slung across the back.",
    "tags": ["work", "sea", "relaxed"],
    "tucked": True,
}

# Damp patches where the shirt clings: down the breastbone, under the arms, and a broad patch on the back.
CHEST = ["..dd..",
         "..dd..",
         "...d..",
         "..dd..",
         "...d.."]
BACK = [".dddd.",
        "dddddd",
        ".dddd.",
        "..dd..",
        "..d..."]
RAKE = (.4, 4.6, 3.15)     # the rake's balance point on the back; handle and board share it


def build(g):
    b = body(g, "S", "weave", 33240, base=3)
    neckline(b.front, "v", "S", base=3)
    b.front.vline(3, 4, 5, "S2")                                         # the open placket
    grid(b.front, 1, 5, CHEST, {"d": "S2"})
    grid(b.back, 1, 2, BACK, {"d": "S2"})
    for face in (b.right, b.left):
        grid(face, 0, 0, ["dddd", ".dd.", ".d.."], {"d": "S2"})
    sleeves(g, "S", "weave", 33241, base=3, rows=(0, 4))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm").strip
        arm.hline(0, 15, 0, "S2")                                         # damp at the shoulder seam
        # The rolled sleeve, stiff and crusted with dried salt.
        cuff = arm_blk(g, f"{side}_salt_cuff", side, 2.6, (5, 2, 5), "S", 3, "weave", 33242 + (side == "left"),
                       dx=-.05 if side == "right" else .05, inflate=.06)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "S4")
            for x in range(face.w):
                face.set(x, 1, "S4" if (x + face.x0) % 3 == 0 else "S2")
        cuff.top.fill("S4")
    # The salt rake: a long ash handle slung across the back, its flat board crusted white along the edge.
    handle = blk(g, "salt_rake_handle", RAKE, (1, 12, 1), "L", 3, "plain", 33244, origin=(-.5, -4.4, -.5),
                 rotation=(0, 0, 14))
    handle.strip.hline(0, handle.strip.w - 1, 0, "L4")
    board = blk(g, "salt_rake_board", RAKE, (4, 2, 1), "L", 2, "plain", 33245, origin=(-2.0, 7.0, -.6),
                rotation=(0, 0, 14))
    for face in (board.front, board.back):
        face.hline(0, 3, 1, "S4"), face.set(1, 0, "L3")
    board.bottom.fill("S4")
    # The rake's sling: a leather strap from the left shoulder across the chest and back.
    line(b.front, 6, 0, 1, 9, "L1"), line(b.back, 1, 0, 6, 9, "L1")
    b.top.vline(6, 0, 3, "L1")
