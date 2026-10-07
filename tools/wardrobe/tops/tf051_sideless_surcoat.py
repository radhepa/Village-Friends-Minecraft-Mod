"""Sideless Surcoat: a surcoat cut away at the sides to show the kirtle, with a fur plackard buttoned down the front."""
from kit import body, sleeves
from kit_female import buttons, fur, neck, over_flaps, sub
from paint import fabric

META = {
    "name": "Sideless Surcoat",
    "gender": "female",
    "description": "A surcoat cut away into deep armholes to show the kirtle, with a fur plackard buttoned down the front.",
    "tags": ["fancy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 15101, base=3)
    neck(b.front, "round", "S", 3)
    sleeves(g, "S", "weave", 15102, base=3, rows=(0, 11))
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 11, "A2")
    j = g.part("jacket")
    for face in (j.front, j.back):
        fabric(face, "P", "velvet", 15103, 2, 2, 0, 4, 12)
        fabric(face, "P", "velvet", 15103, 2, 0, 9, 8, 3)
        for y in range(1, 9):
            face.set(1, y, "P1" if y > 3 else None), face.set(6, y, "P1" if y > 3 else None)
    fur(sub(j.front, 2, 0, 4, 9), "S", 15104, 3)                      # the fur plackard
    buttons(j.front, 3, 1, 8, "M3", step=2)
    buttons(j.front, 4, 2, 8, "M4", step=2)
    for face in (j.right, j.left):
        fabric(face, "P", "velvet", 15105, 2, 0, 9, 4, 3)
    fabric(j.top, "P", "velvet", 15106, 3, 2, 0, 4, 4)
    f, bk = over_flaps(g, "surcoat_skirt", 12, "P", "velvet", 15107, width=8, top=9.0)
    for face in (f, bk):
        face.vline(0, 0, 11, "S3"), face.vline(7, 0, 11, "S3")       # fur edges
        face.vline(3, 1, 10, "P1"), face.vline(4, 2, 10, "P3")
