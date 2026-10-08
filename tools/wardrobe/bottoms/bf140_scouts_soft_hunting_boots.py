"""Scout's Soft Hunting Boots: close breeches over knee-high suede boots that slouch in soft folds, a fringed
turned-down top and a side flap tied shut with two thongs."""
from kit import SIDES, leg_bone, legs, waistband
from kit_female import leg_ring_fold, shoes, waist_belt
from paint import solid

META = {
    "name": "Scout's Soft Hunting Boots",
    "gender": "female",
    "description": "Close breeches over knee-high suede boots slouching in soft folds, with fringed turned-down "
                   "tops and side flaps tied with thongs.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 54181, rows=(0, 4), crease=False)
    body = waistband(g, "P", "twill", 54182)
    body.front.vline(4, 9, 11, "P1")
    shoes(g, "boot", "L", 3, top=4, sole="L0")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L4"), face.hline(0, face.w - 1, 10, "L2")   # the slouch at the ankle
        pants.front.vline(1 if side == "right" else 2, 5, 8, "L2")                     # front seam
        pants.front.hline(0, 3, 11, "L1")
    for box in leg_ring_fold(g, "boot_fold", 3.4, "L", 2):
        for face in box.sides:
            for x in range(face.w):
                face.set(x, 1, "L1" if x % 2 else "L3")              # the fringe
    for side, x in (("right", -2.3), ("left", 2.3)):
        flap = g.piece(f"{side}_boot_flap", leg_bone(side), (-.5, 0, -1.5), (1, 5, 3), pivot=(x, 5.6, .3))
        solid(flap, "L", "leather", 54183, 3)
        out = flap.right if side == "right" else flap.left
        for y in (1, 3):
            out.hline(0, 2, y, "S4")                                  # thong ties
            out.set(1, y + 1, "S3")
    waist_belt(g, "waist_belt", 9.4, height=1)
    pouch = g.piece("waist_pouch", "TORSO", (-1, 0, -1), (2, 3, 2), pivot=(2.6, 10.4, -3.1))
    solid(pouch, "L", "leather", 54184, 2)
    pouch.front.set(0, 0, "L3"), pouch.front.set(1, 0, "L3"), pouch.front.set(1, 1, "M3")
