"""Patched-Elbow Wool Coat: a hip-length wool coat with a turned collar, horn buttons, flap pockets and suede elbow patches."""
from kit import SIDES, body, collar, flaps
from kit_casual import collar_points
from kit_male import buttons
from paint import dark_seams, fabric, k, strip_fabric

META = {
    "name": "Patched-Elbow Wool Coat",
    "gender": "male",
    "description": "A well-worn hip-length wool coat with a turned-down collar, four horn buttons, flapped hip pockets and oval suede patches sewn over both elbows.",
    "tags": ["casual", "simple", "rugged"],
    "covers_waist": True,
}

PATCH = [".pp.",
         "pppp",
         "pppp",
         ".pp."]


def build(g):
    shirt = body(g, "S", "weave", 40100, base=3)
    coat = body(g, "P", "twill", 40101, layer="jacket")
    f, bk = coat.front, coat.back
    # Open throat: the shirt shows above the top button.
    for x, y in ((3, 0), (4, 0), (3, 1), (4, 1)):
        f.clear(x, y)
    shirt.front.vline(4, 0, 1, "S2")
    # Front edge lapping right over left, horn buttons beside it.
    f.vline(4, 2, 11, "P1")
    f.vline(5, 2, 11, "P3")
    buttons(f, 3, 3, 9, 2, "L3")
    # Flapped hip pockets.
    for x0 in (0, 5):
        f.hline(x0, x0 + 2, 7, "P3")
        f.hline(x0, x0 + 2, 8, "P1")
    # Back seam and a waist seam behind.
    bk.vline(4, 1, 11, "P1")
    bk.hline(0, 7, 8, "P1")
    dark_seams(coat, faces=("right", "left"))
    # Sleeves to the wrist with a turned cuff.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "twill", 40102 + (side == "left"), 2, 0, 10)
        fabric(arm.top, "P", "twill", 40102, 3)
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3")
        arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
        # Oval suede patch over the elbow, on the sleeve overlay so it stands proud of the cloth.
        sleeve = g.part(f"{side}_sleeve")
        for dy, row in enumerate(PATCH):
            for dx, ch in enumerate(row):
                if ch == "p":
                    sleeve.back.set(dx, 4 + dy, "L2" if (dx + dy) % 3 else "L3")
        sleeve.back.set(0, 5, "L1"), sleeve.back.set(3, 6, "L1")      # running stitches
        sleeve.back.hline(1, 2, 7, "L1")
    # Turned-down collar: a band round the neck and two points on the chest.
    band = collar(g, "coat_collar", "P", "twill", base=3, height=1, y=-.5)
    for face in band.sides:
        face.hline(0, face.w - 1, 0, "P4")
    collar_points(g, "P", base=3, spread=26, y=.1)
    # Coat skirt split at the back.
    front, back = flaps(g, "coat_skirt", 3, "P", "twill", 40104, top=11.0)
    front.vline(4, 0, 2, "P1"), front.vline(5, 0, 2, "P3")
    back.vline(4, 1, 2, "P0")
    for face in (front, back):
        face.hline(0, 8, 2, k("P", 1))
