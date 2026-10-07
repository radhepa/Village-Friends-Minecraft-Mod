"""Fur Surcote with Hanging Sleeves: a fur-lined surcote whose open sleeves hang from the shoulders behind the arms."""
from kit import body, sleeves
from kit_female import fur, fur_box, neck, over_flaps, sub
from paint import fabric, solid

META = {
    "name": "Fur Surcote with Hanging Sleeves",
    "gender": "female",
    "description": "A merchant wife's fur-lined surcote with a wide fur collar and open sleeves hanging from the shoulders.",
    "tags": ["fancy", "robe"],
    "covers_waist": True,
}


def build(g):
    body(g, "S", "weave", 15601, base=2)
    sleeves(g, "S", "weave", 15602, base=2, rows=(0, 11))
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 11, "S1")
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "P", "twill", 15603, 2)
    fabric(j.top, "P", "twill", 15603, 3)
    neck(j.front, "v", "P", 2)
    fur(sub(j.front, 3, 3, 2, 9), "S", 15604, 4)
    collar = g.piece("fur_collar", "TORSO", (-5, -1.0, -3), (10, 2, 6), inflate=.06)
    fur_box(collar, "S", 15605, 3)
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        x = -3.0 if side == "right" else -1.0
        hang = g.piece(f"{side}_hanging_sleeve", bone, (x, -1.5, 2.1), (4, 12, 1), motion="sway")
        solid(hang, "P", "twill", 15606, 2)
        hang.back.vline(0, 0, 11, "S4"), hang.back.vline(3, 0, 11, "S4")
        hang.back.hline(0, 3, 11, "S4")
        hang.front.fill("S3")
    f, bk = over_flaps(g, "surcote", 12, "P", "twill", 15607, width=10, top=9.0)
    fur(sub(f, 4, 0, 2, 12), "S", 15608, 4)
    bk.hline(0, 9, 11, "S3")
