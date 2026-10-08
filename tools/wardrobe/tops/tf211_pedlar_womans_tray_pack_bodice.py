"""Pedlar Woman's Tray-Pack Bodice: a laced bodice with a pedlar's tray of small wares slung from the neck
and a canvas pack on her back."""
from kit_f07 import prop, strap
from kit_female import bodice, chemise, lacing
from paint import fabric

META = {
    "name": "Pedlar Woman's Tray-Pack Bodice",
    "gender": "female",
    "description": "A laced bodice with a wooden pedlar's tray of ribbons, pots and combs slung from the neck, "
                   "and a strapped canvas pack on her back.",
    "tags": ["casual", "rugged"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 57001, neckline="scoop", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2"), arm.strip.hline(0, 15, 10, "S4")
        arm.front.vline(2, 1, 8, "S2")
    b = bodice(g, "P", "weave", 57002, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "ladder", lace="S4", under="P1", eyelet="M3")
    j = g.part("jacket")
    # The tray's neck strap: from the tray's back corners up over the shoulders, round behind the neck.
    strap(j.front, 1, 6, 2, 0, "L2"), strap(j.front, 6, 6, 5, 0, "L2")
    for x in (2, 5):
        j.top.vline(x, 0, 3, "L2")
    j.back.hline(2, 5, 0, "L2")
    # Pack straps over the shoulders and round under the arms on the back.
    for x in (1, 6):
        j.back.vline(x, 0, 7, "L1")
    for face in (j.right, j.left):
        fabric(face, "L", "leather", 57003, 1, 0, 6, 4, 1)

    # The pedlar's tray: a shallow wooden box held out at the belly, with little partitions.
    tray = prop(g, "tray", "TORSO", (-3.5, 0, -4), (7, 2, 4), pivot=(0, 6.4, -2.35), role="L", seed=57004, base=3)
    tray.top.fill("L1")
    tray.top.vline(3, 0, 3, "L3"), tray.top.hline(0, 6, 2, "L3")
    for face in tray.sides:
        face.hline(0, face.w - 1, 0, "L4")
    tray.front.set(0, 1, "L1"), tray.front.set(6, 1, "L1")
    # Wares: two ribbon rolls, a little lidded pot and a comb.
    for i, (z, role) in enumerate(((-6.0, "A"), (-4.6, "S"))):
        spool = prop(g, f"ribbon_roll_{i}", "TORSO", (0, 0, 0), (2, 1, 1), pivot=(-3.1, 5.4, z), role=role,
                     texture="plain", seed=57005 + i, base=2, edge=False)
        spool.front.set(0, 0, f"{role}3"), spool.front.set(1, 0, f"{role}1")
        spool.top.fill(f"{role}3"), spool.right.fill(f"{role}4"), spool.left.fill(f"{role}4")
    pot = prop(g, "ware_pot", "TORSO", (0, 0, 0), (2, 2, 2), pivot=(.8, 4.4, -5.9), role="M", seed=57007, base=2)
    pot.top.fill("M3"), pot.top.set(0, 0, "M4")
    for face in pot.sides:
        face.hline(0, 1, 0, "M3")
    comb = prop(g, "ware_comb", "TORSO", (0, 0, 0), (2, 1, 1), pivot=(-.6, 5.4, -3.6), role="S", seed=57008,
                base=4, edge=False)
    comb.front.set(0, 0, "S2")

    # The canvas pack on her back, a leather flap buckled shut.
    pack = prop(g, "pack", "TORSO", (-3, 0, 0), (6, 6, 3), pivot=(0, 1.6, 2.35), role="S", texture="twill",
                seed=57009, base=2)
    pack.back.hline(0, 5, 0, "S3")
    fabric(pack.back, "L", "leather", 57010, 2, 0, 0, 6, 3)
    pack.back.hline(0, 5, 2, "L1")
    pack.back.vline(1, 3, 5, "L2"), pack.back.vline(4, 3, 5, "L2")
    pack.back.set(1, 3, "M3"), pack.back.set(4, 3, "M3")
    fabric(pack.top, "L", "leather", 57011, 3)
    roll = prop(g, "pack_roll", "TORSO", (-3.5, 0, 0), (7, 2, 2), pivot=(0, 0.0, 2.7), role="P", texture="weave",
                seed=57012, base=1)
    for face in (roll.front, roll.back):
        face.vline(1, 0, 1, "L2"), face.vline(5, 0, 1, "L2")
    roll.right.fill("P2"), roll.left.fill("P2")
    roll.right.set(0, 0, "P0"), roll.left.set(1, 1, "P0")
