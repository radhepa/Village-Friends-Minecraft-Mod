"""Seaweed Gatherer's Hitched Skirt: a long wool skirt hitched high on the left side only and pinned in a
bunched swag at the hip, so the hem steps up over a striped petticoat, with shins bound in leg wraps."""
from kit import SIDES
from kit_female import SKIRT_BACK, SKIRT_FRONT, shoes, stripes, wraps
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Seaweed Gatherer's Hitched Skirt",
    "gender": "female",
    "description": "A long skirt hitched high on the left into a bunched swag, its hem stepping up over a striped petticoat, shins bound in leg wraps.",
    "tags": ["sea", "work", "rugged", "skirt"],
}

SEED = 53255
TOP = 9.8


def cloth(face, seed):
    fabric(face, "P", "weave", seed, 2)
    face.hline(0, face.w - 1, 0, "P3")
    for x in range(1, face.w, 2):
        face.set(x, 1, "P1")
    face.hline(0, face.w - 1, face.h - 1, "P1")


def build(g):
    body = g.part("body")
    strip_fabric(body, "P", "weave", SEED, 2, 9, 11)
    for f in body.sides:
        f.hline(0, f.w - 1, 9, "P3")
    fabric(body.bottom, "P", "plain", SEED, 1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "weave", SEED + 1, 1, 0, 2)
        fabric(leg.top, "P", "plain", SEED, 1)
        stripes(leg.strip, ["S3", "S3", "A2"], 1, y0=3, h=3)          # the petticoat where the skirt rides up
        leg.strip.hline(0, leg.strip.w - 1, 5, "S2")
        for face in pants.sides:
            wraps(face, 6, 9, "L", 2, step=4)                        # shins bound in leg wraps
    shoes(g, "turnshoe", "L", 1)
    # Front and back in halves: the right falls long, the left is hitched up short.
    for name, z, motion, out in (("front", SKIRT_FRONT, "flap_front", "front"), ("back", SKIRT_BACK, "flap_back", "back")):
        for side, x, n in (("right", -2.5, 11), ("left", 2.5, 6)):
            half = g.piece(f"skirt_{name}_{side}", "TORSO", (-2.5, 0, 0), (5, n, 1), pivot=(x, TOP, z), motion=motion)
            solid(half, "P", "weave", SEED + 2, 2)
            face = getattr(half, out)
            cloth(face, SEED + 3 + (side == "left"))
            if side == "right":
                face.vline(1, 3, n - 2, "P1"), face.vline(3, 4, n - 3, "P3")
            else:
                for xx in range(5):
                    face.set(xx, n - 2, k("P", 1 if xx % 2 else 3))     # drawn up into folds
    for side, x, ox, n, rot in (("right", -5.1, 0, 10, 5), ("left", 5.1, -1, 5, -9)):
        panel = g.piece(f"skirt_{side}", "TORSO", (ox, 0, -2.5), (1, n, 5), pivot=(x, TOP, 0), rotation=(0, 0, rot))
        solid(panel, "P", "weave", SEED + 5, 2)
        for f in panel.sides:
            f.hline(0, f.w - 1, 0, "P3"), f.hline(0, f.w - 1, n - 1, "P1")
    # The swag: the hitched cloth bunched and pinned at the left hip.
    swag = g.piece("waist_hitch_swag", "TORSO", (-1.5, -.4, -1.1), (3, 3, 2), pivot=(3.0, TOP, -2.95), inflate=.1,
                   motion="flap_front")
    solid(swag, "P", "weave", SEED + 6, 2)
    for f in swag.sides:
        f.vline(0, 0, 2, "P1"), f.hline(0, f.w - 1, 0, "P3")
        f.set(1, 2, "P1")
    swag.front.set(1, 0, "M3")                                       # the pin
