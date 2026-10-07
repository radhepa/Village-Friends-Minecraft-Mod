"""Coin Dancer's Bodice: a short sweetheart bodice fringed with coins over a bare midriff, banded sleeves and coin cuffs."""
from kit_female import arm_rings, neck, trim
from paint import fabric, solid, strip_fabric

META = {
    "name": "Coin Dancer's Bodice",
    "gender": "female",
    "description": "A short sweetheart bodice fringed with coins, a bare midriff, light banded sleeves and jingling coin cuffs.",
    "tags": ["fancy", "whimsical"],
    "locked_to": "bf031_coin_dancer_skirt",
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "A", "velvet", 13101, 2, 0, 6)
    fabric(b.top, "A", "velvet", 13101, 3)
    neck(b.front, "sweetheart", "A", 2)
    trim(b.front, 2, "pearls", "M3", "M4", x0=1, x1=6)
    for face in b.sides:
        face.hline(0, face.w - 1, 6, "M2")
    j = g.part("jacket")
    for face in j.sides:
        for x in range(face.w):
            if x % 2 == 0:
                face.set(x, 7, "M4" if (x // 2) % 2 else "M3")      # coins hanging over the midriff
            face.set(x, 6, "M2")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "plain", 13102, 4, 0, 9)
        fabric(arm.top, "S", "plain", 13102, 4)
        arm.strip.hline(0, 15, 1, "A2"), arm.strip.hline(0, 15, 2, "M3")
        for x in range(0, 16, 3):
            arm.strip.vline(x, 3, 8, "S3")
    for box in arm_rings(g, "coin_cuff", 6.8, 2, 6, inflate=.05):
        solid(box, "A", "velvet", 13103, 2)
        for face in box.sides:
            for x in range(face.w):
                face.set(x, 1, "M4" if x % 2 else "M2")
        box.bottom.fill("S3")
