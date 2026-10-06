"""Peddler's Pack Frame: a road tunic under a wooden pack frame laden with a corded bundle and a hanging tin pot."""
from kit import belt, body, neckline, sleeves
from kit_male import blk

META = {
    "name": "Peddler's Pack Frame",
    "gender": "male",
    "description": "A chapman's road tunic under a wooden pack frame laden with a corded bundle of wares, a tin pot swinging below.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 7001)
    neckline(b.front, "laced", "P")
    sleeves(g, "P", "weave", 7002, rows=(0, 10), cuff="P1")
    jacket = g.part("jacket")
    for face in (jacket.front,):
        face.vline(1, 0, 6, "L2"), face.vline(6, 0, 6, "L2")             # pack straps
    for y in range(4):
        jacket.top.set(1, y, "L2"), jacket.top.set(6, y, "L2")
    belt(g, "rope_belt", 9.4, role="S", base=2, height=1, buckle=None)
    for i, x in enumerate((-3.0, 3.0)):
        pole = blk(g, f"frame_pole_{i}", (x, -2.0, 3.0), (1, 13, 1), "L", 3, "plain", 7003 + i)
        pole.strip.hline(0, pole.strip.w - 1, 0, "L4")
    bar = blk(g, "frame_bar", (0, 9.6, 3.0), (7, 1, 1), "L", 2, "plain", 7005, edge=False)
    bundle = blk(g, "ware_bundle", (0, -.4, 4.6), (5, 7, 3), "S", 2, "weave", 7006)
    for face in bundle.sides:
        face.hline(0, face.w - 1, 2, "L1"), face.hline(0, face.w - 1, 5, "L1")
        face.vline(face.w // 2, 0, 6, "L1")
    bundle.top.fill("S3"), bundle.top.vline(2, 0, 2, "L1")
    pot = blk(g, "tin_pot", (0, 10.8, 3.6), (2, 2, 2), "M", 2, "smooth", 7007, motion="sway")
    pot.top.fill("M0"), pot.front.hline(0, 1, 0, "M3")
