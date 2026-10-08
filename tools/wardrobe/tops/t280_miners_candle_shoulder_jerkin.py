"""Miner's Candle-Shoulder Jerkin: a worn leather jerkin with a candle burning in an iron pricket on the left shoulder pad and a pick slung head-down on the back."""
from kit import belt, body, flaps, neckline, roll, sleeves
from kit_male import arm_blk, blk
from paint import fabric, k, strip_fabric

META = {
    "name": "Miner's Candle-Shoulder Jerkin",
    "gender": "male",
    "description": "A worn leather jerkin over a rolled-sleeve shirt, a stub of candle burning in an iron pricket on a leather pad at the left shoulder and a miner's pick slung head-down down his back.",
    "tags": ["work", "rugged", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 37380, base=2)                             # the shirt
    neckline(b.front, "laced", "S")
    sleeves(g, "S", "weave", 37381, rows=(0, 5))
    roll(g, "S", 2.6, base=2)
    jacket = g.part("jacket")                                            # the leather jerkin
    strip_fabric(jacket, "L", "leather", 37383, 2, 0, 11)
    fabric(jacket.top, "L", "leather", 37383, 3)
    fabric(jacket.bottom, "L", "leather", 37384, 1)
    jf = jacket.front
    for x, y in ((2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (4, 2)):
        jf.clear(x, y)
    jf.vline(4, 3, 11, "L0"), jf.vline(3, 3, 11, "L3")                  # the overlapping front
    for y in (4, 7, 10):
        jf.set(4, y, "M2")
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "L1")
    # The candle: a leather pad on the left shoulder, an iron pricket, a stub of tallow and its flame.
    pad = arm_blk(g, "left_shoulder_pad", "left", -2.4, (5, 1, 5), "L", 3, "leather", 37386, inflate=.05)
    pad.top.hline(0, 4, 4, "L4")
    cup = arm_blk(g, "candle_pricket", "left", -3.2, (2, 1, 2), "M", 2, "smooth", 37387, dx=1.0)
    cup.top.fill("M1")
    candle = arm_blk(g, "candle", "left", -5.2, (1, 2, 1), "S", 4, "plain", 37388, dx=1.0)
    candle.strip.hline(0, 3, 1, "S3"), candle.top.fill("S3")
    flame = arm_blk(g, "candle_flame", "left", -6.2, (1, 1, 1), "A", 4, "plain", 37389, dx=1.0)
    flame.bottom.fill("A3"), flame.front.set(0, 0, "A4")
    for face in candle.sides:
        face.set(0, 0, "S4")
    belt(g, "belt", 9.4, height=1)
    # The pick hangs head-down from the shoulders: haft up the spine, double head across the hips.
    haft = blk(g, "pick_haft", (0, .4, 3.2), (1, 8, 1), "L", 3, "plain", 37390, edge=False)
    for face in haft.sides:
        face.set(0, 0, "L4"), face.set(0, 4, "L1")
    head = blk(g, "pick_head", (0, 8.0, 3.4), (7, 1, 1), "K", 3, "smooth", 37391)
    for face in head.sides:
        face.hline(0, face.w - 1, 0, "K3")
    for face in (head.front, head.back):
        face.set(0, 0, "K4"), face.set(6, 0, "K4"), face.hline(2, 4, 0, "K2")   # bright points, dark eye
    head.top.fill("K4"), head.bottom.fill("K2")
    eye = blk(g, "pick_eye", (0, 7.6, 3.4), (2, 2, 1), "K", 2, "smooth", 37392, inflate=.05)
    eye.top.fill("K3")
    for face in flaps(g, "jerkin_skirt", 3, "L", "leather", 37393, top=10.6):
        face.hline(0, 8, 2, k("L", 1))
        face.vline(4, 0, 2, "L0")
