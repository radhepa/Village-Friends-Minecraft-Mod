"""Cowherd's Mud-Hemmed Skirt: a long work skirt caked with field mud that creeps up from the hem in drips
and splashes, over mud-clotted ankle boots."""
from kit import SIDES
from kit_female import shoes, skirt
from paint import k, rnd

META = {
    "name": "Cowherd's Mud-Hemmed Skirt",
    "gender": "female",
    "description": "A long work skirt caked with mud creeping up from the hem in drips and splashes, over mud-clotted ankle boots.",
    "tags": ["work", "rugged", "skirt"],
}


def mud(face, seed, depth=4):
    """Mud rising from the bottom edge: solid at the hem, ragged drips and splashes above."""
    for x in range(face.w):
        reach = 1 + int(rnd(x + face.x0, 1, seed) * depth)
        for d in range(reach):
            y = face.h - 1 - d
            face.set(x, y, k("L", 0 if d == 0 else 1))
        if rnd(x + face.x0, 2, seed) < .25:
            face.set(x, face.h - 2 - depth - int(rnd(x, 3, seed) * 2), "L1")   # a splash higher up


def build(g):
    s = skirt(g, "P", "twill", 51420, top=9.8, length=12, flare=5)
    s.paint(lambda f: mud(f, 51421 + f.x0 % 5, depth=4 if f.w > 5 else 3))
    shoes(g, "ankle", "L", 2, top=9)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for f in pants.sides:
            for x in range(f.w):
                if rnd(x + f.x0, 4, 51426) < .55:
                    f.set(x, 10, "L0")                                # clods of mud on the boots
            f.set(int(rnd(f.x0, 5, 51427) * 4), 9, "L0")
        g.part(f"{side}_leg").bottom.fill("L0")
