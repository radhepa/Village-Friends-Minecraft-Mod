"""Captain's Turned-Down Boots: close velvet breeches and tall boots whose wide tops are turned down to the shin,
pale flesh side out, with the lace frill of the boot hose spilling over the fold and square toes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings, toe_pieces

META = {
    "name": "Captain's Turned-Down Boots",
    "gender": "male",
    "description": "Close velvet breeches and tall boots with wide tops turned down to the shin, pale flesh side out, the "
                   "lace frill of the boot hose spilling over the fold, and square toes.",
    "tags": ["fancy", "sturdy", "sea"],
}


def build(g):
    legs(g, "P", "velvet", 33420, rows=(0, 3), crease=False)
    body = waistband(g, "P", "velvet", 33421)
    body.front.vline(4, 9, 11, "P1")
    footwear(g, "boot", top=4, base=1, sole="K0")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.vline(1 if side == "right" else 2, 7, 10, "L2")     # polished shin
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L0")
    # The boot hose: a lace frill standing above the fold.
    for ring in leg_rings(g, "boot_hose_lace", 2.6, "S", (5, 1, 5), 4, "plain", 33422, inflate=.32):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S4" if (x + face.x0) % 2 else "S2")
        ring.bottom.fill("S2")
    # The turned-down top: a broad flared cuff of pale flesh-side leather with a scalloped lower edge.
    for ring in leg_rings(g, "boot_turn", 3.4, "L", (5, 3, 5), 3, "smooth", 33424, inflate=.26):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4")
            for x in range(face.w):
                face.set(x, 2, "L1" if (x + face.x0) % 3 == 0 else "L2")
        ring.top.fill("L1")
    for toe in toe_pieces(g, "square_toe", (3, 1, 1), "L", base=1, y=11.0, z=-2.0):
        toe.front.hline(0, 2, 0, "L2")
