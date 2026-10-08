"""Novice's Undyed Habit: a habit of plain undyed wool cut a size too large, its long sleeves folded
back into deep cuffs; a white veil falling down the back over a little white collar, and a hempen cord
tied in a bow at the waist."""
from kit import body, sleeves
from kit_female import arm_rings, collar_flat, girdle, hanging
from paint import fabric, solid

META = {
    "name": "Novice's Undyed Habit",
    "gender": "female",
    "description": "A roomy habit of undyed wool with deep folded-back cuffs, a white collar and veil, and a hempen cord tied in a bow.",
    "tags": ["holy", "simple", "robe"],
}


def build(g):
    b = body(g, "S", "plain", 55201, base=1)
    for face in (b.front, b.back):
        face.vline(2, 2, 11, "S0"), face.vline(5, 3, 11, "S0")       # the habit's loose folds
        face.vline(3, 3, 10, "S2")
    for arm in sleeves(g, "S", "plain", 55202, base=1, rows=(0, 11)):
        arm.strip.vline(1, 2, 7, "S0"), arm.strip.vline(9, 2, 7, "S0")
        arm.strip.hline(0, 15, 11, "S0")
    # Sleeves too long for her, folded back into deep cuffs: the lining shows as a pale band.
    for box in arm_rings(g, "folded_cuff", 6.2, 3, 5, inflate=.08):
        solid(box, "S", "plain", 55203, 3, edge=False)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "S4")
            face.hline(0, face.w - 1, 2, "S1")
            face.set(face.w // 2, 1, "S2")
            face.set(face.w // 2, 2, "S0")
        box.bottom.fill("S0")
    # The novice's white collar and the white veil down her back.
    collar_flat(g, "collar", "S", 4, edge="S3")
    veil = g.piece("veil", "TORSO", (-4, 0, 0), (8, 7, 1), pivot=(0, -.6, 2.5), rotation=(5, 0, 0))
    solid(veil, "S", "plain", 55204, 4)
    veil.back.vline(2, 1, 6, "S3"), veil.back.vline(5, 1, 6, "S3")
    veil.back.hline(0, 7, 6, "S3")
    fabric(veil.top, "S", "plain", 55204, 4)
    # A hempen cord at the waist, tied in a bow, the two ends hanging.
    girdle(g, "cord", 8.0, role="L", base=3, height=1, buckle=None, texture="plain")
    bow = g.piece("cord_bow", "TORSO", (-1.5, -.5, -.5), (3, 1, 1), pivot=(-1.4, 8.5, -2.75))
    solid(bow, "L", "plain", 55205, 3, edge=False)
    bow.front.set(1, 0, "L1")
    for i, (x, n) in enumerate(((-1.8, 5), (-0.8, 4))):
        end = hanging(g, f"cord_end_{i}", x, n, role="L", base=3, top=8.8)
        end.front.set(0, n - 1, "L1")
