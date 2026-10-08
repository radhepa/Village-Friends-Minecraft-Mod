"""Seed Sower's Seed-Lip Tunic: a hooded sowing tunic with a kidney-shaped wicker seedlip slung at the left hip on a broad strap, heaped with grain."""
from kit import body, flaps, neckline, sleeves
from kit_m01 import wicker
from kit_male import blk, hood_down
from paint import k, line, solid

META = {
    "name": "Seed Sower's Seed-Lip Tunic",
    "gender": "male",
    "description": "A plain sowing tunic with its hood thrown back and a broad linen strap over the right shoulder carrying a kidney-shaped wicker seedlip at the left hip, heaped with grain.",
    "tags": ["work", "casual", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 31650)
    neckline(b.front, "keyhole", "P")
    for face in (b.right, b.left):
        face.vline(1, 2, 11, "P1")
    sleeves(g, "P", "twill", 31651, rows=(0, 10), cuff="P1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3")
        for face in arm.sides:
            face.vline(1, 2, 8, "P1")
    hood_down(g, "P", "twill", 31652, width=7, y=-.9, z=2.9, tilt=16, lining="S2")
    # The seedlip's strap: right shoulder across the chest to the left hip, and across the back.
    jacket = g.part("jacket")
    for face, pts in ((jacket.front, (0, 0, 6, 8)), (jacket.back, (7, 0, 1, 8))):
        line(face, *pts, "S3")
        line(face, pts[0] + (1 if face is jacket.front else -1), pts[1], pts[2] + (1 if face is jacket.front else -1),
             pts[3], "S2")
    jacket.top.vline(1, 0, 3, "S3")
    belt = g.piece("belt", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.05)
    solid(belt, "L", "leather", 31653, 2, edge=False)
    belt.front.set(4, 0, "M3")
    # The seedlip: a kidney-shaped wicker basket riding the left hip, grain heaped in its mouth.
    lip = g.piece("seedlip", "TORSO", (-2, 0, -1.5), (4, 3, 3), pivot=(1.6, 7.8, -4.0), rotation=(0, -12, 0))
    for face in lip.sides:
        wicker(face, "L", 2, face.x0)
    lip.top.fill("S3")
    for x in range(4):
        lip.top.set(x, 0, "L4"), lip.top.set(x, 2, "L4")                  # the lip's rim
    lip.top.set(1, 1, "S4"), lip.top.set(2, 1, "S2")
    lip.bottom.fill("L1")
    bulge = g.piece("seedlip_bulge", "TORSO", (-1.5, 0, -1), (3, 2, 1), pivot=(1.6, 8.3, -5.4), rotation=(0, -12, 0))
    for face in bulge.sides:
        wicker(face, "L", 2, face.x0 + 1, rim=False)
    bulge.top.fill("L4"), bulge.bottom.fill("L1")
    heap = blk(g, "seedlip_grain", (1.6, 7.2, -4.0), (2, 1, 2), "S", 3, "plain", 31654, rotation=(0, -12, 0),
               edge=False)
    heap.top.fill("S4"), heap.top.set(0, 0, "S2")
    for face in flaps(g, "tunic_skirt", 4, "P", "twill", 31656, top=10.8, slit=True):
        face.hline(0, 8, 3, k("P", 1))
        for x in range(1, 9, 3):
            face.set(x, 2, "S3")                                          # a few spilled seeds caught in the cloth
