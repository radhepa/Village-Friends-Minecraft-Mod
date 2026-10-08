"""Haymaker's Open-Neck Shirt: a loose linen shirt unlaced to the chest, sleeves rolled, a broad straw hat slung down the back."""
from kit import body, roll, sleeves
from kit_m01 import twist
from kit_male import blk
from paint import k, line, solid

META = {
    "name": "Haymaker's Open-Neck Shirt",
    "gender": "male",
    "description": "A loose linen shirt unlaced deep down the chest with its laces hanging free, sleeves rolled to the elbow and a broad-brimmed straw hat slung down the back.",
    "tags": ["casual", "relaxed", "work"],
    "tucked": True,
}

OPEN = [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2), (3, 3), (4, 3), (4, 4)]


def build(g):
    b = body(g, "S", "weave", 31101, base=3)
    f = b.front
    for x, y in OPEN:
        f.clear(x, y)
    for y in range(0, 5):                                                 # eyelet edges either side
        f.set(2, y, "S2" if y % 2 else "S4")
        f.set(5, y, "S2" if y % 2 else "S1")
    f.set(1, 0, "S4"), f.set(6, 0, "S2"), f.set(3, 4, "S1"), f.set(4, 5, "S1")
    for face in (b.front, b.back):
        face.vline(1, 6, 11, "S2"), face.vline(6, 7, 11, "S2")             # loose folds
    b.back.hline(2, 5, 0, "S2")
    for face in (b.right, b.left):
        face.vline(1, 1, 11, "S2")
    sleeves(g, "S", "weave", 31102, base=3, rows=(0, 5))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for face in arm.sides:
            face.vline(1, 1, 4, "S2")
    roll(g, "S", 2.6, base=3)
    # The untied laces hanging from the open neck.
    for i, (x, rz) in enumerate(((-1.2, 10), (1.2, -14))):
        lace = g.piece(f"neck_lace_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 1.2, -2.45), rotation=(0, 0, rz),
                       motion="sway")
        solid(lace, "L", "plain", 31103 + i, 3, edge=False)
        lace.strip.hline(0, lace.strip.w - 1, 2, "M3")                    # aiglet tips
    # The hat's cord round the throat.
    jacket = g.part("jacket")
    line(jacket.front, 0, 0, 2, 2, "L2"), line(jacket.front, 7, 0, 5, 2, "L2")
    jacket.top.vline(1, 0, 3, "L2"), jacket.top.vline(6, 0, 3, "L2")
    jacket.back.vline(1, 0, 1, "L2"), jacket.back.vline(6, 0, 1, "L2")
    # A broad straw hat hanging flat down the back: a round brim built from three stacked plates
    # (wide, square, tall) so it reads as a disc, plaited in rings, with a crown and band.
    for i, (w, h, dz) in enumerate(((9, 5, 0.0), (7, 7, .08), (5, 9, .16))):
        brim = g.piece(f"straw_hat_brim_{i}", "TORSO", (-w / 2, -h / 2, 0), (w, h, 1), pivot=(0, 5.6, 2.55 + dz),
                       rotation=(-6, 0, 0))
        for face in brim.faces:
            for y in range(face.h):
                for x in range(face.w):
                    if face.name in ("back", "front"):
                        ring = ((x - (face.w - 1) / 2) ** 2 + (y - (face.h - 1) / 2) ** 2) ** .5
                        face.set(x, y, k("S", 3 if int(ring + .5) % 2 else 2))
                    else:
                        face.set(x, y, "S1")
        brim.back.hline(0, w - 1, 0, "S3"), brim.back.hline(0, w - 1, h - 1, "S1")
        brim.back.vline(0, 0, h - 1, "S1"), brim.back.vline(w - 1, 0, h - 1, "S1")
    crown = g.piece("straw_hat_crown", "TORSO", (-2.5, 0, 0), (5, 5, 2), pivot=(0, 3.3, 3.6), rotation=(-6, 0, 0))
    solid(crown, "S", "plain", 31105, 3, edge=False)
    for face in crown.sides:
        twist(face, "S", 3, ox=face.x0)
    for y in range(5):                                                    # plaited crown top, coiled
        for x in range(5):
            ring = max(abs(x - 2), abs(y - 2))
            crown.back.set(x, y, "S4" if ring == 1 else "S3" if ring == 0 else "S2")
    crown.right.vline(1, 0, 4, "A2"), crown.left.vline(0, 0, 4, "A2")    # hat band round the crown's foot
    crown.top.hline(0, 4, 1, "A3"), crown.bottom.hline(0, 4, 1, "A1")
    blk(g, "hat_band_bow", (-2.9, 6.2, 4.1), (1, 2, 1), "A", 2, "plain", 31106, edge=False)
