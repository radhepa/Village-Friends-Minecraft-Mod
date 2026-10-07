"""Shieldmaiden's War Skirt: a knee-length wool skirt split for striding, studded leather strips, trousers and fur-topped boots."""
from kit import SIDES, legs
from kit_female import fur_box, leg_rings, shoes, skirt
from paint import solid

META = {
    "name": "Shieldmaiden's War Skirt",
    "gender": "female",
    "description": "A knee-length wool skirt split at the sides with studded leather strips, over trousers and fur-topped boots.",
    "tags": ["martial", "rugged", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 11911, top=9.6, length=7, sides=False, folds=False)
    for f in s.wide_faces:
        for x in (1, 4, 5, 8):
            f.vline(x, 1, 6, "L2")
            f.set(x, 2, "M3"), f.set(x, 5, "M3")
        f.hline(0, f.w - 1, 6, "P1")
    legs(g, "S", "twill", 11912, rows=(3, 7), crease=False)
    shoes(g, "boot", "L", 2, top=8)
    for ring in leg_rings(g, "fur_top", 7.4, 2):
        fur_box(ring, "S", 11913, 3)
    for side, x in (("right", -4.5), ("left", 4.5)):
        strap = g.piece(f"waist_hip_strap_{side}", "TORSO", (-.5, 0, -1), (1, 5, 2), pivot=(x * 1.12, 9.6, 0))
        solid(strap, "L", "leather", 11914, 2)
        (strap.right if side == "right" else strap.left).set(1, 2, "M3")
