"""Ranger's Mottled Cloak: a long cloak dappled like leaf-shade, fastened with an antler toggle, over a plain forest tunic."""
from kit import belt, body, neckline, sleeves
from kit_male import back_drape, blk, hood_down, shoulder_cape
from paint import rnd

META = {
    "name": "Ranger's Mottled Cloak",
    "gender": "male",
    "description": "A forest warden's long cloak dappled like leaf-shade, its hood thrown back, fastened with an antler toggle over a plain tunic.",
    "tags": ["rugged", "martial"],
    "covers_waist": True,
}


def dapple(face, seed):
    for y in range(face.h):
        for x in range(face.w):
            r = rnd((x + face.x0) // 2, (y + face.y0) // 2, seed)
            face.set(x, y, "P1" if r < .3 else "P3" if r > .82 else "P2")


def build(g):
    b = body(g, "S", "weave", 7901, base=2)
    neckline(b.front, "round", "S")
    sleeves(g, "S", "weave", 7902, rows=(0, 10), cuff="S1")
    belt(g, "belt", 9.4, height=1)
    cape = shoulder_cape(g, "cloak_shoulders", "P", "weave", 7903, length=3, width=12)
    for face in cape.faces:
        dapple(face, 7904)
    cape.front.vline(6, 0, 2, "P0")
    hood = hood_down(g, "P", "weave", 7905, y=-1.0, z=3.1)
    for face in hood.sides:
        dapple(face, 7906)
    for name, length, y, motion in (("cloak_back", 11, 1.4, "none"), ("cloak_hem", 5, 12.2, "flap_back")):
        drape = back_drape(g, name, "P", length, "weave", 7907, width=10, y=y, z=3.1 if motion == "none" else 3.4,
                           tilt=4, motion=motion)
        for face in drape.faces:
            dapple(face, 7908 + length)
    toggle = blk(g, "antler_toggle", (0, .4, -3.3), (3, 1, 1), "S", 3, "plain", 7909, edge=False)
    toggle.front.set(0, 0, "S4"), toggle.front.set(2, 0, "S2")
