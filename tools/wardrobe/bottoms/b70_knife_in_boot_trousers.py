"""Knife-in-Boot Trousers: wool trousers tucked into tall soft boots, a sheath knife's hilt jutting from the right boot top."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from paint import solid

META = {
    "name": "Knife-in-Boot Trousers",
    "gender": "male",
    "description": "Wool trousers tucked into tall soft boots, a sheath knife's horn hilt jutting from the top of the right boot.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 7011, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 7012)
    footwear(g, "boot", top=4, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 4, "L4")
        pants.front.vline(1 if side == "right" else 2, 5, 9, "L1")
    bone = leg_bone("right")
    sheath = g.piece("boot_sheath", bone, (-.5, 0, -1), (1, 3, 2), pivot=(-2.35, 4.6, .4))
    solid(sheath, "L", "leather", 7013, 1)
    grip = g.piece("boot_knife_grip", bone, (-.5, 0, -.5), (1, 2, 1), pivot=(-2.35, 2.6, .4))
    solid(grip, "S", "plain", 7014, 3)
    grip.strip.hline(0, grip.strip.w - 1, 1, "M3")
    pommel = g.piece("boot_knife_pommel", bone, (-.5, 0, -.5), (1, 1, 1), pivot=(-2.35, 1.9, .4))
    solid(pommel, "M", "smooth", 7015, 3, edge=False)
