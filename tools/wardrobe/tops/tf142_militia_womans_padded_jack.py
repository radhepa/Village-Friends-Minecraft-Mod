"""Militia Woman's Padded Jack: a short jack quilted in square puffs, a padded roll round the shoulders, short
puffed sleeves over the shirt, and her iron kettle hat hung on her back by its strap."""
from kit import sleeves
from kit_female import arm_rings, girdle, lacing, over_flaps
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Militia Woman's Padded Jack",
    "gender": "female",
    "description": "A short jack quilted in square puffs, with a padded shoulder roll, puffed half sleeves, and an "
                   "iron kettle hat hung on her back.",
    "tags": ["martial", "sturdy"],
    "covers_waist": True,
}


def squares(face, role="P", base=2, x0=0, y0=0, step=3):
    """Box quilting: stitched seams on a square grid, each square puffed up in the middle."""
    for y in range(y0, face.h):
        for x in range(x0, face.w):
            gx, gy = (x + face.x0) % step, (y - y0) % step
            if gx == 0 or gy == 0:
                face.set(x, y, k(role, base - 1))
            elif gx == 1 and gy == 1:
                face.set(x, y, k(role, base + 1))
            else:
                face.set(x, y, k(role, base))


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "plain", 54241, 2)
    fabric(b.top, "P", "plain", 54241, 3), fabric(b.bottom, "P", "plain", 54241, 1)
    for face in b.sides:
        squares(face, "P", 2, y0=1)
    lacing(b.front, 3, 1, 9, "ladder", lace="L3", under="P0", eyelet=None)
    b.front.vline(2, 1, 10, "P3"), b.front.vline(5, 1, 10, "P1")
    # Shirt sleeves under puffed, quilted half sleeves.
    sleeves(g, "S", "weave", 54242, base=3, rows=(4, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "plain", 54243, 2, 0, 3)
        fabric(arm.top, "P", "plain", 54243, 3)
        arm.strip.hline(0, 15, 11, "S2")
    for box in arm_rings(g, "half_sleeve", -2.2, 6, 5, inflate=.18):
        solid(box, "P", "plain", 54244, 2)
        for face in box.sides:
            squares(face, "P", 2, step=3)
            face.hline(0, face.w - 1, 5, "P1")
        fabric(box.top, "P", "plain", 54244, 3)
    roll = g.piece("shoulder_roll", "TORSO", (-4.5, -1.0, -2.6), (9, 2, 5), inflate=.22)
    solid(roll, "P", "plain", 54245, 2, edge=False)
    for face in roll.sides:
        for x in range(0, face.w, 2):
            face.vline(x, 0, 1, "P1")
        face.hline(0, face.w - 1, 0, "P3")
    girdle(g, "belt", 8.4, role="L", height=1)
    f, bk = over_flaps(g, "jack_skirt", 3, "P", "plain", 54246, width=10, top=9.0)
    for face in (f, bk):
        squares(face, "P", 2, step=3)
        face.hline(0, face.w - 1, 2, "P1")
    f.vline(4, 0, 2, "P0"), f.vline(5, 0, 2, "P0")
    # The kettle hat, hung on her back: a wide iron brim and the domed crown behind it, with its chin strap.
    brim = g.piece("kettle_hat_brim", "TORSO", (-3.5, -3.5, 0), (7, 7, 1), pivot=(0, 5.0, 2.45))
    solid(brim, "M", "smooth", 54247, 2, edge=False)
    f = brim.back
    for i in range(7):
        f.set(i, 0, "M1"), f.set(i, 6, "M1"), f.set(0, i, "M1"), f.set(6, i, "M1")
    f.set(0, 0, "M0"), f.set(6, 0, "M0"), f.set(0, 6, "M0"), f.set(6, 6, "M0")
    crown = g.piece("kettle_hat_crown", "TORSO", (-2, -2, 0), (4, 4, 2), pivot=(0, 5.0, 3.45))
    solid(crown, "M", "smooth", 54248, 3, edge=False)
    crown.back.set(1, 1, "M4"), crown.back.set(2, 1, "M4"), crown.back.hline(0, 3, 3, "M2")
    for face in crown.sides:
        face.set(0, 0, "M2")
    strap = g.piece("kettle_hat_strap", "TORSO", (-.5, 0, 0), (1, 4, 1), pivot=(1.5, -.2, 2.3), rotation=(0, 0, 0))
    solid(strap, "L", "leather", 54249, 2, edge=False)
