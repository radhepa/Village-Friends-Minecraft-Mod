"""Swineherd's Hide Cape: a short rawhide shoulder cape edged in fur, pinned with a bone toggle, and a cow-horn on a cord."""
from kit import belt, body, neckline, sleeves
from kit_male import blk, fur, shoulder_cape
from paint import line

META = {
    "name": "Swineherd's Hide Cape",
    "gender": "male",
    "description": "A short rawhide cape over the shoulders, fur at its edge and a bone toggle at the throat, with a calling horn on a cord.",
    "tags": ["rugged", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 4401)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "weave", 4402, rows=(0, 10), cuff="P1")
    cape = shoulder_cape(g, "hide_cape", "L", "leather", 4403, base=2, length=4, width=12)
    for face in cape.sides:
        for x in range(face.w):
            if x % 3 == 0:
                face.set(x, 3, "L1")                                   # uneven hide edge
    cape.front.vline(6, 0, 3, "L0")
    rim = g.piece("cape_fur_rim", "TORSO", (-6, 3.2, -2.9), (12, 1, 6), inflate=.08)
    fur(rim, "S", 4404, 2)
    toggle = blk(g, "bone_toggle", (0, .3, -3.25), (2, 1, 1), "S", 4, "plain", 4405, edge=False)
    toggle.front.set(1, 0, "S2")
    jf, jb = g.part("jacket").front, g.part("jacket").back
    line(jf, 7, 4, 1, 9, "L1"), line(jb, 0, 4, 6, 9, "L1")           # the horn's cord
    belt(g, "belt", 9.6, height=1)
    horn = blk(g, "calling_horn", (-2.6, 8.6, -2.8), (2, 2, 1), "S", 3, "plain", 4406, rotation=(0, 0, 25))
    horn.front.set(0, 0, "S4"), horn.front.set(1, 1, "S2")
    tip = blk(g, "calling_horn_tip", (-3.6, 10.0, -2.8), (1, 2, 1), "S", 1, "plain", 4407, rotation=(0, 0, 40))
    tip.strip.hline(0, tip.strip.w - 1, 1, "K2")
