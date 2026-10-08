"""Gamekeeper's Snare-Belt Coat: a windowpane-check keeper's coat with flapped pockets, brass wire snares on the belt and a netted game bag behind."""
from kit import SIDES, belt, body, collar, flaps, sleeves
from kit_male import blk
from kit_m07 import coil, windowpane
from paint import fabric, k

META = {
    "name": "Gamekeeper's Snare-Belt Coat",
    "gender": "male",
    "description": "A keeper's windowpane-check tweed coat with a turned-down collar and big flapped pockets, brass-wire snares hung at both hips and a netted game bag slung behind his hip.",
    "tags": ["rugged", "work", "sturdy"],
    "covers_waist": True,
}


def wire(box, role="M", base=2):
    for face in box.faces:
        fabric(face, role, "smooth", 37204, base)
    return box


def build(g):
    b = body(g, "P", "twill", 37200)
    for face in b.sides:
        windowpane(face, "P", 2, ox=face.x0 + 2)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.vline(4, 1, 11, "P0")                                              # the coat's front edge
    for y in (3, 6):
        f.set(3, y, "L3")                                                # horn buttons
    sleeves(g, "P", "twill", 37201, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        windowpane(arm.strip, "P", 2, rows=range(0, 9))
        arm.strip.hline(0, arm.strip.w - 1, 9, "L2"), arm.strip.hline(0, arm.strip.w - 1, 10, "L1")   # leather cuffs
        (arm.right if side == "right" else arm.left).rect(0, 4, 4, 2, "L2")   # leather elbow guard
    turn = collar(g, "turned_collar", "P", "twill", base=3, height=1, y=-.5)
    turn.front.set(4, 0, "P1"), turn.front.set(3, 0, "P1")
    # Big pockets with stiff flaps on the chest.
    for i, x in enumerate((-2.4, 2.4)):
        flap = blk(g, f"pocket_flap_{i}", (x, 4.6, -2.45), (3, 1, 1), "P", 3, "twill", 37202 + i, edge=False)
        flap.front.set(1, 0, "L2")
        f.hline(1 if i == 0 else 5, 2 if i == 0 else 6, 7, "P1")
    belt(g, "belt", 9.3, height=1)
    # Running-noose snares of brass wire hung from the belt at each hip.
    for i, x in enumerate((-2.3, 2.3)):
        for bar in coil(g, f"snare_{i}", (x, 10.2, -3.4), size=3, thick=1, depth=1, role="M", base=2, painter=wire,
                        hang=True, motion="flap_front"):
            bar.front.set(0, 0, "M4")
    # The netted game bag behind the right hip, its strap over the left shoulder.
    jacket = g.part("jacket")
    for y in range(0, 9):
        jacket.back.set(min(7, y * 6 // 8), y, "L2")
    jacket.front.set(6, 0, "L2"), jacket.front.set(7, 1, "L2")
    bag = blk(g, "game_bag", (-2.0, 7.4, 3.3), (4, 4, 2), "L", 2, "leather", 37205)
    bag.top.fill("L3")
    for face in bag.sides:
        face.hline(0, face.w - 1, 0, "L3")
        for y in range(1, face.h):
            for x in range(face.w):
                face.set(x, y, "S1" if (x + y) % 2 else "L1")                # knotted netting over the pouch
    bag.back.vline(0, 0, 3, "L2"), bag.back.vline(3, 0, 3, "L2")
    for face in flaps(g, "coat_skirt", 6, "P", "twill", 37206, top=10.4, slit=True):
        windowpane(face, "P", 2, ox=2, rows=range(1, 6))
        face.hline(0, 8, 0, k("P", 3)), face.hline(0, 8, 5, k("P", 1))
        face.vline(4, 1, 5, "P0")
