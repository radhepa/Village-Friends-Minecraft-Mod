"""Gate Warden's Lamellar Vest: a vest of laced lamellae over a rolled-sleeve shirt, small lamellar spaulders and a warning horn."""
from kit import SIDES, body, roll, sleeves
from kit_male import arm_blk
from kit_m04 import hanging, lamellar
from paint import solid

META = {
    "name": "Gate Warden's Lamellar Vest",
    "gender": "male",
    "description": "A sleeveless vest of small plates laced in rows, laced shut down both sides, with lamellar spaulders "
                   "and a skirt of lames over a rolled-sleeve shirt, and an ox-horn on the belt to sound the alarm.",
    "tags": ["armor", "martial", "rugged"],
    "requires": ["sturdy"],
    "covers_waist": True,
}

S = 34320


def build(g):
    body(g, "S", "weave", S)
    jacket = g.part("jacket")
    for face in jacket.sides:
        lamellar(face, rows=range(0, 12), ox=face.x0)
    lamellar(jacket.top, ox=1)
    jacket.front.rect(2, 0, 4, 2, None)                                   # round neck shows the shirt
    jacket.front.set(1, 1, "L2"), jacket.front.set(6, 1, "L2")
    jacket.top.rect(2, 2, 4, 2, None)
    for face in (jacket.right, jacket.left):                               # side lacing
        for y in range(1, 11, 2):
            face.set(1, y, "L3"), face.set(2, y + 1, "L3")
    sleeves(g, "S", "weave", S + 1, rows=(0, 5))
    roll(g, "S", 2.6, base=3)
    for i, side in enumerate(SIDES):
        spaulder = arm_blk(g, f"{side}_spaulder", side, -2.3, (5, 3, 5), "M", 2, "smooth", S + 2 + i, inflate=.14)
        for face in spaulder.sides:
            lamellar(face, ox=face.x0)
            face.hline(0, face.w - 1, 0, "L2")
        spaulder.top.fill("M3")
    belt = g.piece("belt", "TORSO", (-4.6, 9.4, -2.6), (9, 2, 5), inflate=.08)
    solid(belt, "L", "leather", S + 4, 2, edge=False)
    for face in belt.sides:
        face.hline(0, face.w - 1, 0, "L3")
    belt.front.set(4, 1, "M3"), belt.front.set(4, 0, "M3")
    # Ox-horn on a thong at the right hip: mouthpiece, curve, flared bell.
    tip = hanging(g, "horn_tip", -1.8, 10.8, (1, 1, 1), "L", 1, "plain", S + 5, top=10.8, dz=-.1)
    tip.front.fill("L1")
    mid = hanging(g, "horn_body", -2.5, 11.4, (2, 2, 1), "S", 3, "plain", S + 6, top=10.8, dz=-.1)
    mid.front.set(0, 0, "S4"), mid.front.set(1, 1, "S2")
    bell = hanging(g, "horn_bell", -3.3, 12.6, (2, 2, 2), "S", 3, "plain", S + 7, top=10.8, dz=.2)
    bell.front.hline(0, 1, 0, "L2"), bell.bottom.fill("K1")
    # Skirt of lames, laced in two rows.
    for name, z, motion, face_name in (("lame_skirt_front", -2.85, "flap_front", "front"),
                                        ("lame_skirt_back", 1.85, "flap_back", "back")):
        panel = g.piece(name, "TORSO", (-4.5, 0, 0), (9, 5, 1), pivot=(0, 10.8, z), motion=motion)
        solid(panel, "M", "smooth", S + 8, 2)
        for face in panel.sides:
            lamellar(face, ox=face.x0 + 1)
        getattr(panel, face_name).vline(4, 1, 4, "L1")
