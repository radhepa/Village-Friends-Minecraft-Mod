"""Coracle Man's Back-Slung Boat: a plain wool shirt under a broad carrying strap, the round tarred-hide coracle slung
upside down on the back like a shell, its willow ribs showing, with a short paddle lashed across it."""
from kit import body, flaps, neckline, sleeves
from kit_male import blk
from paint import k, line

META = {
    "name": "Coracle Man's Back-Slung Boat",
    "gender": "male",
    "description": "A plain wool shirt under a broad carrying strap, the round tarred-hide coracle slung upside down on "
                   "the back like a shell, willow ribs showing, a short paddle lashed across it.",
    "tags": ["sea", "work", "rugged"],
}

BOAT = (0, 6.0, 2.6)         # the middle of the coracle's rim against the back; every boat piece shares it


def hide(face, base=1):
    """Tarred hide stretched over a lattice of willow laths."""
    for y in range(face.h):
        for x in range(face.w):
            rib, band = x % 4 == 1, y % 4 == 2
            face.set(x, y, k("L", 1) if rib or band else k("K", base + 1) if (x + y) % 5 == 0 else k("K", base))
    for x in range(face.w):                                              # the willow rim, lit along its edge
        face.set(x, 0, "L3")


def build(g):
    b = body(g, "P", "weave", 33560)
    neckline(b.front, "laced", "P")
    sleeves(g, "P", "weave", 33561, rows=(0, 10), cuff="P1")
    # The carrying strap: from both shoulders down to a broad band across the chest.
    f = b.front
    f.vline(1, 0, 4, "L2"), f.vline(6, 0, 4, "L2")
    f.hline(0, 7, 5, "L3"), f.hline(0, 7, 6, "L1")
    b.top.vline(1, 0, 3, "L2"), b.top.vline(6, 0, 3, "L2")
    for face in (b.right, b.left):
        face.hline(0, 3, 5, "L3"), face.hline(0, 3, 6, "L1")
    line(b.back, 1, 0, 1, 2, "L2"), line(b.back, 6, 0, 6, 2, "L2")
    # The coracle: a deep round bowl, mouth against the back, its curved bottom facing out.
    shell = blk(g, "coracle_shell", BOAT, (8, 10, 2), "K", 1, "plain", 33562, origin=(-4, -5.0, 0))
    hide(shell.back)
    for face in (shell.right, shell.left):
        for y in range(face.h):
            face.set(0, y, "L3"), face.set(1, y, "L2")
    shell.top.fill("L3"), shell.bottom.fill("L3")
    shell.front.fill("L1")
    for y in range(1, 10, 3):
        shell.front.hline(0, 7, y, "L2")                                   # the inside of the willow frame
    for name, oy in (("coracle_crown_top", -6.0), ("coracle_crown_bottom", 5.0)):
        cap = blk(g, name, BOAT, (6, 1, 2), "K", 1, "plain", 33563 + (oy > 0), origin=(-3, oy, 0))
        hide(cap.back)
        cap.top.fill("L3"), cap.bottom.fill("L3"), cap.front.fill("L1")
        for face in (cap.right, cap.left):
            face.fill("L3")
    boss = blk(g, "coracle_bottom", BOAT, (6, 8, 1), "K", 1, "plain", 33565, origin=(-3, -4.0, 2))
    hide(boss.back, 1)
    for face in (boss.top, boss.bottom, boss.right, boss.left):
        face.fill("K1")
    # The paddle, lashed slantwise across the bottom of the boat.
    shaft = blk(g, "coracle_paddle", BOAT, (1, 9, 1), "L", 3, "plain", 33566, origin=(-.5, -4.5, 3.0),
                rotation=(0, 0, 32))
    shaft.strip.hline(0, shaft.strip.w - 1, 0, "L4")
    blade = blk(g, "coracle_paddle_blade", BOAT, (2, 3, 1), "L", 3, "plain", 33567, origin=(-1.0, 4.5, 3.0),
                rotation=(0, 0, 32))
    blade.back.vline(0, 0, 2, "L2")
    for face in flaps(g, "shirt_hem", 2, "P", "weave", 33568, top=11.0):
        face.hline(0, 8, 1, "P1")
